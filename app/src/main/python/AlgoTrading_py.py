import quandl
import numpy as np
from matplotlib.figure import Figure
from pylab import plt
from PIL import Image
import os
from Static import SP500


quandl.ApiConfig.api_key = '-kw-n8eEQg3ZaUP8tUsr'


def SMA(select):

    error_msg = 'Quandl API cannot load price data for ' + select

    ticker = SP500.get(select)
    data = quandl.get_table('WIKI/PRICES', qopts={'columns': ['date', 'close', 'ticker']}, ticker=ticker, paginate=True)
    data.rename(columns={'date': 'Date'}, inplace=True)

    if data.empty:
        return ['error', error_msg]

    data = data.sort_values(by=['Date'])
    data = data.set_index('Date')


    SMAs_Short = 42
    SMAs_Long = 252

    df = Figure()
    df = data[data['ticker'] == ticker]
    df['SMAs_Short'] = df['close'].rolling(SMAs_Short).mean()
    df['SMAs_Long'] = df['close'].rolling(SMAs_Long).mean()
    df.rename(columns={'ticker': 'Ticker'}, inplace=True)
    df.dropna(inplace=True)
    df.rename(columns={'close': select}, inplace=True)
    df.plot(figsize=(10, 10), linewidth=0.8)
    plt.ylabel('Price')
    df['Position'] = np.where(df['SMAs_Short'] > df['SMAs_Long'], 1, -1)
    df['Trade'] = np.where(df['Position'] != df['Position'].shift(1), 'Trade', 'Still')
    ax = df.plot(secondary_y='Position', figsize=(10, 10), linewidth=0.8)
    plt.ylabel('Position')
    df.rename(columns={select: 'Close'}, inplace=True)
    df = df[df['Trade'] == 'Trade'].drop(['Ticker', 'SMAs_Short', 'SMAs_Long', 'Trade'], axis=1)
    res = []
    for i in range(len(df)):
        if df['Position'][i] == 1:
            res.append('Buy ' + ticker + ' on ' + str(df.index[i].date().strftime("%b %d, %Y")) + ' Price at ' + str(df['Close'][i]) + '\n')
        else:
            res.append('Sell ' + ticker + ' on ' + str(df.index[i].date().strftime("%b %d, %Y")) + ' Price at ' + str(df['Close'][i]) + '\n')


    dir = os.environ["HOME"] + '/smagraph.png'
    plt.savefig(dir)


    image = Image.open(dir)

    width, height = image.size
    left = width/17
    top = height/17
    right = width
    bottom = height
    image = image.crop((left, top, right, bottom))

    image.rotate(270).save(dir)


    return [dir, 'Simple Moving Averages Trading Strategy for ' + str(select) + ' (Ticker: ' + ticker + ')' +\
           '\n'*2 + str(''.join(res))]