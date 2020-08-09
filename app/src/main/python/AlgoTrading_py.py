import numpy as np
import pandas as pd
from matplotlib.figure import Figure
from pylab import plt
from PIL import Image
import requests
from bs4 import BeautifulSoup
import json
import os
from Static import SP500


def SMA(select):

    ticker = SP500.get(select)

    try:
        url_prefix = 'https://sandbox.iexapis.com/stable/stock/'
        url_suffix = '/chart/max?token=Tsk_d536dffef19e4ae4941ea4ac530d6133'
        full_url = '{}{}{}'.format(url_prefix, ticker.lower(), url_suffix)
        source = requests.get(full_url, timeout=20)
        soup = BeautifulSoup(source.text, 'html.parser')
        data = json.loads(str(soup))
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        return ['error', 'Error: Internet connection failure.']
    except (ValueError, requests.exceptions.HTTPError):
        return ['error', 'Error: {}'.format(full_url) + '\ndoes not exist.']
    except:
        return ['error', 'Error parsing IEX API. Please contact the creator for its resolution.']


    if not data:
        error_msg = 'Error: IEX API cannot load price data for {}.'.format(select)
        return ['error', error_msg]


    temp_date = []
    temp_price = []
    for item in data:
        temp_date.append(item['date'])
        temp_price.append(item['close'])
    data = pd.DataFrame({'Date': temp_date, select: temp_price})
    data = data.set_index('Date')


    SMAs_Short = 12
    SMAs_Long = 52

    df = Figure()
    df = data

    df['SMAs_Short'] = df[select].rolling(SMAs_Short).mean()
    df['SMAs_Long'] = df[select].rolling(SMAs_Long).mean()
    df.dropna(inplace=True)
    df.plot(figsize=(10, 10), linewidth=0.8)
    plt.ylabel('Price')
    plt.legend(fontsize='large')


    df['Position'] = np.where(df['SMAs_Short'] > df['SMAs_Long'], 1, -1)
    df['Trade'] = np.where(df['Position'] != df['Position'].shift(1), 'Trade', 'Still')

    ax = df.plot(secondary_y='Position', figsize=(10, 10), linewidth=0.8)
    plt.ylabel('Position')
    plt.title('SMAs Trading Strategy: ' + select)


    df = df[df['Trade'] == 'Trade'].drop(['SMAs_Short', 'SMAs_Long', 'Trade'], axis=1)

    res = []
    for i in range(len(df)):
        if df['Position'][i] == 1:
             res.append('Buy {} on {} Price at {}\n'.format(ticker, str(df.index[i]), str(format(df[select][i], ','))))
        else:
            res.append('Sell {} on {} Price at {}\n'.format(ticker, str(df.index[i]), str(format(df[select][i], ','))))


    dir = '{}{}'.format(os.environ["HOME"], '/smagraph.png')
    plt.savefig(dir)

    image = Image.open(dir)

    width, height = image.size
    left = width/17
    top = height/17
    right = width
    bottom = height
    image = image.crop((left, top, right, bottom))

    image.rotate(270).save(dir)


    return [dir, 'Simple Moving Averages Trading Strategy for {} (Ticker: {}).{}{}'.format(str(select), ticker, '\n'*2, str(''.join(res)))]