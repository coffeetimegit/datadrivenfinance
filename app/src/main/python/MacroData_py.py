import pandas as pd
from pylab import plt
from PIL import Image
import requests
from bs4 import BeautifulSoup
import json
from Static import ISO3
import os


def MacroData(raw, data_type, abs):

    select = []
    temp = []
    for i in range(1, len(raw)):
        if raw[i] != ',' and raw[i] != ']':
            temp.append(raw[i])
        else:
            if len(select) > 0:
                select.append(''.join(temp)[1:])
                temp = []
            else:
                select.append(''.join(temp))
                temp = []

    percentage = False
    if data_type == 'population':
        suffix = '_LP'
    elif data_type == 'gdp':
        suffix = '_NGDPD'
    elif data_type == 'govspending':
        suffix = '_GGX'
    elif data_type == 'debt':
        suffix = '_GGXWDN'
    elif data_type == 'unemployment':
        suffix = '_LUR'
    elif data_type == 'import':
        suffix = '_TM_RPCH'
        percentage = True
    elif data_type == 'export':
        suffix = '_TX_RPCH'
        percentage = True


    try:
        url_prefix = 'https://www.quandl.com/api/v3/datasets/ODA/'
        url_suffix = '?api_key=-kw-n8eEQg3ZaUP8tUsr'

        country_list = {}
        unfound = []
        for i in select:
            temp = {}
            full_url = '{}{}{}{}'.format(url_prefix, ISO3[i], suffix, url_suffix)
            source = requests.get(full_url)
            soup = BeautifulSoup(source.text, 'html.parser')
            data_raw = json.loads(str(soup))
            if 'quandl_error' in data_raw:
                unfound.append(i)
                continue

            for val in reversed(data_raw['dataset']['data']):
                temp[val[0]] = val[1]

            if data_raw['dataset']['data'][-1][1] == 0:
                del temp[data_raw['dataset']['data'][-1][0]]

            country_list[i] = pd.Series(temp)

        data = pd.DataFrame(country_list).dropna()

    except:
        message = 'Error: Internet connection failure.'
        return ['error', message]

    if unfound:
        for na in unfound:
            select.remove(na)

    if unfound:
        message = 'Error: Quandl API cannot load {} data for \n{}.'.format(data_type, '\n'.join(unfound))
    else:
        message = None

    if len(data.columns) == 0:
        return ['error', message]

    data.plot(figsize=(10, 10), linewidth=2)
    plt.xlabel('Years')


    if data_type == 'population':
        plt.title('Population in Millions')
    elif data_type == 'gdp':
        plt.title('GDP in USD Billions')
    elif data_type == 'govspending':
        plt.title('Government Expenditure in USD Billions')
    elif data_type == 'debt':
        plt.title('National Net Debt in USD Billions')
    elif data_type == 'unemployment':
        plt.title('Unemployment Rate in percentage')
    elif data_type == 'import':
        plt.title('Percentage change in Imports')
    elif data_type == 'export':
        plt.title('Percentage change in Exports')

    plt.legend(fontsize='large')


    if abs:

        dir = '{}{}'.format(os.environ["HOME"], '/macrograph.png')
        plt.savefig(dir)

        image = Image.open(dir)
        width, height = image.size
        left = width/25
        top = height/25
        right = width
        bottom = height
        image = image.crop((left, top, right, bottom))
        image.rotate(270).save(dir)
        return [dir, message]

    else:

        data_relative = data.dropna()

        if percentage:
            for k in range(len(select)):
                res = [100]
                for l in range(1, len(data_relative)):
                    res.append((1 + data_relative[select[k]][l]/100) * (res[-1]))

                data_relative[select[k]] = res
            data_relative.plot(figsize=(10, 10))
            plt.plot(data_relative, linewidth=2, ls='')
            plt.xlabel('Years')
            plt.legend(fontsize='large')

        else:
            for k in range(len(select)):
                res = []
                ind = data_relative[select[k]][0]
                for l in range(len(data_relative)):
                    res.append(((data_relative[select[k]][l] / ind) - 1) * 100)
                data_relative[select[k]] = res
            data_relative.plot(figsize=(10, 10))
            plt.plot(data_relative, linewidth=2, ls='')
            plt.xlabel('Years')
            plt.legend(fontsize='large')


        if data_type == 'population':
            plt.title('Percentage change in Population')
        elif data_type == 'gdp':
            plt.title('Percentage change in GDP')
        elif data_type == 'govspending':
            plt.title('Percentage change in Government Expenditure')
        elif data_type == 'debt':
            plt.title('Percentage change in Net Debt')
        elif data_type == 'unemployment':
            plt.title('Percentage change in Unemployment Rate')
        elif data_type == 'import':
            plt.title('Cumulative change in Import')
        elif data_type == 'export':
            plt.title('Cumulative change in Export')


        dir = '{}{}'.format(os.environ["HOME"], '/macrograph.png')
        plt.savefig(dir)

        image = Image.open(dir)

        width, height = image.size
        left = width/25
        top = height/25
        right = width
        bottom = height
        image = image.crop((left, top, right, bottom))

        image.rotate(270).save(dir)

        return [dir, message]