import numpy as np
import pandas as pd
import scipy.optimize as sco
import matplotlib.pyplot as plt
from PIL import Image
import requests
from bs4 import BeautifulSoup
import json
import concurrent.futures
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


    consolidated = pd.DataFrame()

    unfound = []

    check = products
    key_list = list(SP500.keys())
    val_list = list(SP500.values())

    def serialize(url, attempt):
        if attempt > 10:
            position = val_list.index(url)
            unfound.append(key_list[position])
            check.remove(url)
            return None
        else:
            try:
                attempt += 1
                full_url = '{}{}{}'.format(url_prefix, url.lower(), url_suffix)
                source = requests.get(full_url)
                soup = BeautifulSoup(source.text, 'html.parser')
                data = json.loads(str(soup))
                consolidated = pd.DataFrame(data, columns=['date', 'close'])
                consolidated.rename(columns={'date': 'Date', 'close': url}, inplace=True)
                consolidated = consolidated.set_index('Date')
                return consolidated

            except (ValueError, requests.exceptions.HTTPError, json.JSONDecodeError):
                serialize(url, attempt)

            except:
                return 'error'


    result = []
    iterator = [1] * len(check)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while check:
            if not temp:
                temp = list(executor.map(serialize, check, iterator))

            else:
                temp = list(executor.map(serialize, check, iterator))

            try:
                if temp[0] == 'error':
                    error_msg = 'Error: Internet connection failure.'
                    return ['error', stocks, error_msg]
            except:
                pass

            temp = [t for t in temp if t is not None]
            result += temp
            result = [res for res in result if res is not None]

            for i in temp:
                check.remove(i.columns[-1])


    for i in result:
        if len(consolidated) == 0:
            consolidated = i
        else:
            consolidated = pd.merge(consolidated, i, on="Date")

    select = [sel for sel in select if sel not in unfound]

    products = []
    for col in consolidated.columns:
        products.append(col)


    if unfound:
        unfound_stock = []
        for filter in unfound:
            unfound_stock.append(filter)

        message = 'Error: IEX API cannot load price data for\n{}.'.format('\n'.join(unfound_stock))


    if len(products) < 2:
        return ['error', stocks, message]


    noa = len(products)
    consolidated = consolidated[products]
    rets = np.log(consolidated / consolidated.shift(1))

    def Return(weights):
        return np.sum(rets.mean() * weights) * 252 * 100

    def Volatility(weights):
        return np.sqrt(np.dot(weights.T, np.dot(rets.cov() * 252, weights))) * 100

    prets = []
    pvols = []


    for _ in range(simulation):
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
    MXS_SR = 'Sharpe Ratio: {}'.format(str(format((Return(opts['x']) / Volatility(opts['x'])), '.3%')))
    MXS_VOL = 'Volatility: {}'.format(str(format(Volatility(opts['x']) / 100, '.3%')))
    MXS_PR = 'Portfolio Return: {}'.format(str(format(Return(opts['x']) / 100, '.3%')))
    MXS_Alloc_Title = 'Allocation details:'
    MXS_Alloc = []

    for allocation in range(len(opts['x'])):
        MXS_Alloc.append('Allocate {} to {}'.format(str(format(opts['x'][allocation], '.3%')), str(select[allocation])))

    optv = sco.minimize(Volatility, eweights, method='SLSQP', bounds=bnds, constraints=cons)
    MXV_Title = ('Minimum Volatility details:')
    MXV_VOL = 'Volatility: {}'.format(str(format(Volatility(optv['x']) / 100, '.3%')))
    MXV_SR = 'Sharpe Ratio: {}'.format(str(format((Return(optv['x']) / Volatility(optv['x'])), '.3%')))
    MXV_PR = 'Portfolio Return: {}'.format(str(format(Return(optv['x']) / 100, '.3%')))
    MXV_Alloc_Title = ('Allocation details:')
    MXV_Alloc = []

    for allocation in range(len(optv['x'])):
        MXV_Alloc.append('Allocate {} to {}'.format(str(format(optv['x'][allocation], '.3%')), str(select[allocation])))

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
    plt.scatter(pvols, prets, c=(prets/pvols)*100, marker='.', alpha=0.8, cmap='coolwarm_r')
    plt.plot(tvols, trets, 'b', lw=2.5)
    plt.plot(Volatility(optv['x']), Return(optv['x']),
             'r*', markersize=15)
    plt.plot(Volatility(opts['x']), Return(opts['x']),
             'y*', markersize=15)
    plt.xlabel('Expected Volatility in percentage')
    plt.ylabel('Expected Return in percentage')
    plt.colorbar(label='Sharpe ratio in percentage')
    plt.title('Portfolio Optimization')


    dir = '{}{}'.format(os.environ["HOME"], '/mptgraph.png')
    plt.savefig(dir)

    image = Image.open(dir)

    width, height = image.size
    left = width/19
    top = height/19
    right = width
    bottom = height
    image = image.crop((left, top, right, bottom))

    image.rotate(270).save(dir)

    title = '{} simulations generated.\n\nInvestment Universe:\n{}\n\n'.format(str(format(simulation, ',')), str(select))
    MXS_desc = '{}\n\n{}\n{}\n{}\n'.format(str(MXS_Title), str(MXS_SR), str(MXS_VOL), str(MXS_PR))
    MXS_alloc = '{}\n{}\n\n'.format(str(MXS_Alloc_Title), str('\n'.join(MXS_Alloc)))
    MXV_desc = '{}\n\n{}\n{}\n{}\n'.format(str(MXV_Title), str(MXV_VOL), str(MXV_SR), str(MXV_PR))
    MXV_alloc = '{}\n{}'.format(str(MXV_Alloc_Title), str('\n'.join(MXV_Alloc)))

    return [dir, '{}{}{}{}{}'.format(title, MXS_desc, MXS_alloc, MXV_desc, MXV_alloc), message]
