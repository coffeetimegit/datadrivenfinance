import quandl
import pandas as pd
from pylab import plt
from PIL import Image
from Static import ISO3
import os


quandl.ApiConfig.api_key = '-kw-n8eEQg3ZaUP8tUsr'

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

    country = []
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
    elif data_type == 'export':
        suffix = '_TX_RPCH'

    message = 'Clear country list.'

    for i in select:
        country.append('ODA/' + ISO3[i] + suffix)
    try:
        data = quandl.get(country)
        data = pd.DataFrame(data)
    except:
        return ['error', message]


    unfound = []
    for na in range(len(data.columns)):
        if 'Not Found' in data.columns[na]:
            unfound.append(data.columns[na])

    key_list = list(ISO3.keys())
    val_list = list(ISO3.values())

    for filter in unfound:
        select.remove(key_list[val_list.index(filter[4:7])])

    error = []
    if len(unfound) > 0:
        for drop in unfound:
            error.append(key_list[val_list.index(drop[4:7])])
            data.drop(drop, axis = 1, inplace=True)

    if error:
        message = 'Quandl API cannot load ' + data_type + ' data for \n' + '\n'.join(error)
    else:
        message = None

    if len(data.columns) == 0:
        return ['error', message]


    for j in range(len(select)):
        data.rename(columns={'ODA/' + ISO3[select[j]] + suffix + ' - Value': select[j]}, inplace=True)

    data.plot(figsize=(10, 10))
    plt.xlabel('Years')

    if data_type == 'population':
        plt.ylabel('Population in Millions')
    elif data_type == 'gdp':
        plt.ylabel('GDP in USD Billions')
    elif data_type == 'govspending':
        plt.ylabel('Government Expenditure in USD Billions')
    elif data_type == 'debt':
        plt.ylabel('Net Debt in USD Billions')
    elif data_type == 'unemployment':
        plt.ylabel('Unemployment Rate in percentage')
    elif data_type == 'import':
        plt.ylabel('Percentage change in Imports')
    elif data_type == 'export':
        plt.ylabel('Percentage change in Exports')



    if abs == True:

        dir = os.environ["HOME"] + '/macrograph.png'
        plt.savefig(dir)

        image = Image.open(dir)
        width, height = image.size
        left = width/17
        top = height/17
        right = width
        bottom = height
        image = image.crop((left, top, right, bottom))
        image.rotate(270).save(dir)
        return [dir, message]

    else:

        data_relative = data.dropna()


        for k in range(len(select)):
            res = []
            ind = data_relative[select[k]][0]
            for l in range(len(data_relative)):
                res.append(((data_relative[select[k]][l] / ind) - 1) * 100)
            data_relative[select[k]] = res
        data_relative.plot(figsize=(10, 10))
        plt.plot(data_relative)
        plt.xlabel('Years')

        if data_type == 'population':
            plt.ylabel('Percentage change in Population')
        elif data_type == 'gdp':
            plt.ylabel('Percentage change in GDP')
        elif data_type == 'govspending':
            plt.ylabel('Percentage change in Government Expenditure')
        elif data_type == 'debt':
            plt.ylabel('Percentage change in Net Debt')
        elif data_type == 'unemployment':
            plt.ylabel('Percentage change in Unemployment Rate')
        elif data_type == 'import':
            plt.ylabel('Percentage change in Import')
        elif data_type == 'export':
            plt.ylabel('Percentage change in Export')

        dir = os.environ["HOME"] + '/macrograph.png'
        plt.savefig(dir)

        image = Image.open(dir)

        width, height = image.size
        left = width/17
        top = height/17
        right = width
        bottom = height
        image = image.crop((left, top, right, bottom))

        image.rotate(270).save(dir)

        return [dir, message]