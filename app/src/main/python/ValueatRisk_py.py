import numpy as np
import pandas as pd
import scipy.stats as scs
import matplotlib.pyplot as plt
from PIL import Image
import requests
from bs4 import BeautifulSoup
import json
from Static import SP500
import os


def VAR(select):

    ticker = SP500.get(select)

    try:
        url_prefix = 'https://sandbox.iexapis.com/stable/stock/'
        url_suffix = '/chart/max?token=Tsk_d536dffef19e4ae4941ea4ac530d6133'
        source = requests.get(url_prefix + ticker.lower() + url_suffix)
        soup = BeautifulSoup(source.text, 'html.parser')
        data = json.loads(str(soup))

        temp_date = []
        temp_price = []
        for item in data:
            temp_date.append(item['date'])
            temp_price.append(item['close'])
        data = pd.DataFrame({'Date': temp_date, select: temp_price})

    except json.decoder.JSONDecodeError:
        error_msg = 'IEX API cannot load price data for ' + select
        return ['error', error_msg]


    plt.figure(figsize=(10, 10))
    data = pd.DataFrame(data)

    latest_date = data.values[-1][0]
    latest_price = data.values[-1][1]
    simulation = 10000

    percs = np.linspace(0, 100, num=simulation)[1:-1]
    percs_display = [0.01, 0.1, 1, 2.5, 5, 10, 20, 30, 40, 50]


    risk = np.log(data[select] / data[select].shift(1))

    VaR = scs.scoreatpercentile(latest_price * risk, percs)

    _, _, bars = plt.hist(VaR, bins=500)
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

    title = '%16s %16s' % ('Confidence Level', 'Value at Risk')
    line = '-----' * 11

    res = []
    for pair in zip(percs_display, VaR):
        res.append('%14f %19f' % (100 - pair[0], -pair[1]))

    return [dir, result + description + title + '\n' + line + '\n' + '\n'.join(res)]

