import numpy as np
import pandas as pd
import scipy.optimize as sco
import matplotlib.pyplot as plt
from PIL import Image
import requests
from bs4 import BeautifulSoup
import json
from Static import SP500
import os



def MPT(stocks, simulation):

    select = []
    temp = []
    for stock in range(1, len(stocks)):
        if stocks[stock] != ',' and stocks[stock] != ']':
            temp.append(stocks[stock])
        else:
            if len(select) > 0:
                select.append(''.join(temp)[1:])
                temp = []
            else:
                select.append(''.join(temp))
                temp = []


    message = 'load success'

    simulation = int(simulation[1:-1])

    products = []
    for item in select:
        products.append(SP500.get(item))

    url_prefix = 'https://sandbox.iexapis.com/stable/stock/'
    url_suffix = '/chart/max?token=Tsk_d536dffef19e4ae4941ea4ac530d6133'

    start = None
    end = None
    consolidated = pd.DataFrame()

    unfound = []
    for product in products:

        try:
            source = requests.get(url_prefix + product.lower() + url_suffix)
            soup = BeautifulSoup(source.text, 'html.parser')
            data = json.loads(str(soup))

            temp_date = []
            temp_price = []
            for item in data:
                temp_date.append(item['date'])
                temp_price.append(item['close'])

            if start:
                if list(temp_date)[0] > start:
                    start = list(temp_date)[0]
            else:
                start = list(temp_date)[0]

            if end:
                if list(temp_date)[-1] < end:
                    end = list(temp_date)[-1]
            else:
                end = list(temp_date)[-1]

            if len(consolidated) == 0:
                consolidated = pd.DataFrame({'Date': temp_date, product: temp_price})

            else:
                consolidated = pd.merge(consolidated, pd.DataFrame({'Date': temp_date, product: temp_price})).dropna()


        except json.decoder.JSONDecodeError:
            unfound.append(product)


    if unfound:
        key_list = list(SP500.keys())
        val_list = list(SP500.values())
        unfound_stock = []
        for filter in unfound:
            products.remove(filter)
            select.remove(key_list[val_list.index(filter)])
            unfound_stock.append(key_list[val_list.index(filter)])

        message = 'IEX API cannot load price data for\n' + '\n'.join(unfound_stock)


    if len(products) < 2:
        return ['error', stocks, message]


    noa = len(products)
    consolidated = consolidated[products]
    consolidated = consolidated.dropna()
    rets = np.log(consolidated / consolidated.shift(1))

    def Return(weights):
        return np.sum(rets.mean() * weights) * 252 * 100

    def Volatility(weights):
        return np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights))) * 100

    prets = []
    pvols = []


    for p in range(simulation):
        weights = np.random.random(noa)
        weights /= np.sum(weights)
        prets.append(Return(weights))
        pvols.append(Volatility(weights))
    prets = np.array(prets)
    pvols = np.array(pvols)


    def Minimum_Sharpe_Ratio(weights):
        return -Return(weights) / Volatility(weights)

    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bnds = tuple((0, 1) for x in range(noa))
    eweights = np.array(noa * [1 / noa])

    opts = sco.minimize(Minimum_Sharpe_Ratio, eweights, method='SLSQP', bounds=bnds, constraints=cons)
    MXS_Title = 'Maximum Sharpe Ratio details:'
    MXS_SR = 'Sharpe Ratio: ' + str(format((Return(opts['x']) / Volatility(opts['x'])), '.3%'))
    MXS_VOL = 'Volatility: ' + str(format(Volatility(opts['x']) / 100, '.3%'))
    MXS_PR = 'Portfolio Return: ' + str(format(Return(opts['x']) / 100, '.3%'))
    MXS_Alloc_Title = 'Allocation details:'
    MXS_Alloc = []

    for allocation in range(len(opts['x'])):
        MXS_Alloc.append('Allocate ' + str(format(opts['x'][allocation], '.3%')) +  ' to ' +
                         str(select[allocation]))

    optv = sco.minimize(Volatility, eweights, method='SLSQP', bounds=bnds, constraints=cons)
    MXV_Title = ('Minimum Volatility details:')
    MXV_VOL = 'Volatility: ' + str(format(Volatility(optv['x']) / 100, '.3%'))
    MXV_SR = 'Sharpe Ratio: ' + str(format((Return(optv['x']) / Volatility(optv['x'])), '.3%'))
    MXV_PR = 'Portfolio Return: ' + str(format(Return(optv['x']) / 100, '.3%'))
    MXV_Alloc_Title = ('Allocation details:')
    MXV_Alloc = []

    for allocation in range(len(optv['x'])):
        MXV_Alloc.append('Allocate ' + str(format(optv['x'][allocation], '.3%')) + ' to ' +
                         str(select[allocation]))

    cons = ({'type': 'eq', 'fun': lambda x: Return(x) - tret},
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bnds = tuple((0, 1) for x in weights)

    trets = np.linspace(Return(optv['x']), Return(opts['x']), 50)
    tvols = []
    for tret in trets:
        res = sco.minimize(Volatility, eweights, method='SLSQP',
                           bounds=bnds, constraints=cons)
        tvols.append(res['fun'])
    tvols = np.array(tvols)

    plt.figure(figsize=(10, 10))
    plt.scatter(pvols, prets, c=(prets/pvols)*100, marker='.', alpha=0.8, cmap='coolwarm')
    plt.plot(tvols, trets, 'b', lw=2.5)
    plt.plot(Volatility(optv['x']), Return(optv['x']),
             'r*', markersize=15)
    plt.plot(Volatility(opts['x']), Return(opts['x']),
             'y*', markersize=15)
    plt.xlabel('Expected Volatility in percentage')
    plt.ylabel('Expected Return in percentage')
    plt.colorbar(label='Sharpe ratio in percentage')


    dir = os.environ["HOME"] + '/mptgraph.png'
    plt.savefig(dir)

    image = Image.open(dir)

    width, height = image.size
    left = width/19
    top = height/19
    right = width
    bottom = height
    image = image.crop((left, top, right, bottom))

    image.rotate(270).save(dir)


    return [dir, str(format(simulation, ',')) + ' simulations generated.\n\n' + 'Investment Universe:\n' + str(select) + '\n' * 2 + \
           str(MXS_Title) + '\n' * 2 + str(MXS_SR) + '\n' + str(MXS_VOL) + '\n' + \
           str(MXS_PR) + '\n' + str(MXS_Alloc_Title) + '\n' + str('\n'.join(MXS_Alloc)) + '\n' * 2 + \
           str(MXV_Title) + '\n' * 2 + str(MXV_VOL) + '\n' + str(MXV_SR) + '\n' + \
           str(MXV_PR) + '\n' + str(MXV_Alloc_Title) + '\n' + str('\n'.join(MXV_Alloc)), message]