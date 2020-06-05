import numpy as np
import pandas as pd
import scipy.stats as scs
import matplotlib.pyplot as plt
from PIL import Image
import quandl
from Static import SP500
import os


quandl.ApiConfig.api_key = '-kw-n8eEQg3ZaUP8tUsr'


def VAR(select):

    error_msg = 'Quandl API cannot load price data for ' + select

    ticker = SP500.get(select)
    data = quandl.get_table('WIKI/PRICES', qopts={'columns': ['date', 'close']}, ticker=ticker,
                            paginate=True).dropna()

    if data.empty:
        return ['error', error_msg]

    plt.figure(figsize=(10, 10))
    data = pd.DataFrame(data)

    latest_date = data.values[0][0]
    latest_price = data.values[0][1]
    simulation = 10000

    percs = np.linspace(0, 100, num=simulation)[1:-1]
    percs_display = [0.01, 0.1, 1, 2.5, 5, 10, 20, 30, 40, 50]

    data.sort_values('date', ascending=True, inplace=True)

    risk = np.log(data['close'] / data['close'].shift(1))

    VaR = scs.scoreatpercentile(latest_price * risk, percs)

    _, _, bars = plt.hist(VaR, bins=200)
    for bar in bars:
        if bar.get_x() > 0:
            bar.set_facecolor("cornflowerblue")
        else:
            bar.set_facecolor("tomato")


    plt.title(select)
    plt.xlabel('Return')
    plt.ylabel('Frequency')


    dir = os.environ["HOME"] + '/vargraph.png'
    plt.savefig(dir)


    image = Image.open(dir)

    width, height = image.size
    left = width / 18
    top = height / 18
    right = width
    bottom = height
    image = image.crop((left, top, right, bottom))

    image.rotate(270).save(dir)

    result = str(format(simulation, ',')) + ' simulations generated.\n\n'
    description = 'Value at Risk profile for ' + select + ' that is trading at ' + str(latest_price) + ' on ' + str(latest_date) + '.\n\n'
    note = '*Note: Free version of Quandl API cannot load the most up-to-date price data.\n\n'

    title = '%16s %16s' % ('Confidence Level', 'Value at Risk')
    line = '-----' * 11

    res = []
    for pair in zip(percs_display, VaR):
        res.append('%14f %19f' % (100 - pair[0], -pair[1]))

    return [dir, result + description + note + title + '\n' + line + '\n' + '\n'.join(res)]

