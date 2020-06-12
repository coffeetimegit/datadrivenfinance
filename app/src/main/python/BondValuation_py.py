import requests
from bs4 import BeautifulSoup
import numpy as np
from pylab import plt
from datetime import datetime, date
from PIL import Image
import os



def FIV(product, bondDetails):

    print(product)
    product_details = bondDetails[bondDetails.index(product) - 1: bondDetails.index(product) + 40]
    print(product_details)

    cpn_details = product_details[product_details.index('['):product_details.index(',')]
    cpn = ''
    for cpn_text in cpn_details:
        if cpn_text != '[' and cpn_text != "'" and cpn_text != ",":
            cpn += cpn_text
    cpn = round(float(cpn)/100, 7)

    mat_details = product_details[product_details.index(','):product_details.index(']')]
    mat = ''
    for mat_text in mat_details:
        if mat_text != ' ' and mat_text != ',' and mat_text != "'" and mat_text != ']':
            mat += mat_text
    mat = datetime.strptime(mat, '%m/%d/%Y').date()
    today = date.today()

    payment = int((mat - today).days / 365)
    print('Payment ', payment)
    #print('Remainder ', remainder)

    face = 100
    yld = cpn
    #tenor = payment + remainder

    def BondPrice(face, cpn, yld, pymt):
        Price = ((face + cpn * 100) * pymt) * face / ((face + yld * 100) * pymt)
        return Price

    duration_price = BondPrice(face, cpn, yld, payment)

    def MacaulayDuration(face, cpn, yld, pymt):
        CashFlow = []
        CashFlowPV = []
        TimeWeightedCashFlowPV = []

        for cnt in range(pymt - 1):

            CashFlow.append(face * cpn)
            CashFlowPV.append(CashFlow[-1] / (1 + yld) ** (cnt + 1))
            TimeWeightedCashFlowPV.append((cnt + 1) * CashFlowPV[-1])
            print('CashFlow ', CashFlow[-1], 'CashFlowPV ', CashFlowPV[-1], 'TimeWeightedCashFlowPV ', TimeWeightedCashFlowPV[-1])

        #Make sure to also create a condition if maturity within a year later
        CashFlow.append(face + (face * cpn))
        CashFlowPV.append(CashFlow[-1] / (1 + yld) ** (pymt))
        TimeWeightedCashFlowPV.append((pymt) * CashFlowPV[-1])
        print('CashFlow ', CashFlow[-1], 'CashFlowPV ', CashFlowPV[-1], 'TimeWeightedCashFlowPV ', TimeWeightedCashFlowPV[-1])
        Macaulay = sum(TimeWeightedCashFlowPV) / sum(CashFlowPV)

        return Macaulay

    coupon_frequency = 1
    yield_change = 0.001
    ModD = MacaulayDuration(face, cpn, yld, payment) / (1 + (yld / coupon_frequency)) * yield_change
    print('Modified Duration below')
    print(ModD)

    yld_perm = []
    prices = []
    duration_line_pos = []
    duration_line_neg = []
    res = []


    permutations = np.linspace(yld-0.5, yld+0.5, 10001)
    #permutations = permutations[4500:5500]
    for i in permutations:
        yld_perm.append(round(i, 4))
        prices.append(BondPrice(face, cpn, yld_perm[-1], payment))

    yld_perm = yld_perm[1:]
    prices = prices[1:]
    print(yld_perm[int(len(yld_perm)/2)])
    print(yld_perm) # Good to go
    print(len(yld_perm))

    print(prices) # Good to go
    print('Actual Price in the middle: ', prices[int(len(prices)/2)])
    print(len(prices))


    duration_line_pos = [duration_price]
    for j in range(int(len(permutations)/2)):
        duration_line_pos.append(duration_price + ModD * j)
        duration_line_neg.append(duration_price - ModD * j)

    duration_line_pos.sort(reverse=True)
    duration_line = duration_line_pos + duration_line_neg
    duration_line = duration_line[:-1]
    print(duration_line) # Good to go

    plt.figure(figsize=(10, 10))
    plt.plot(yld_perm, duration_line, 'g', label='Duration')
    plt.plot(yld_perm, prices, 'c', label='Actual Price')
    plt.plot(yld, duration_price, 'y*', markersize=10)
    plt.title('Bond Duration and Convexity for ' + product)
    plt.xlabel('Yield')
    plt.ylabel('Bond Price')
    plt.legend()
    #plt.show()

    dir = os.environ["HOME"] + '/bondgraph.png'
    plt.savefig(dir)

    image = Image.open(dir)

    width, height = image.size
    left = width/19
    top = height/19
    right = width
    bottom = height
    image = image.crop((left, top, right, bottom))

    image.rotate(270).save(dir)

    def Convexity(increase, decrease, initial, yld_perm):
        res = []
        for i in range(int(len(yld_perm)/2)):
            res.append()

    return [dir, 'Convexity Result']




def JGBISIN():

    r = requests.get('https://www.solactive.com/Indices/?indexmembers=DE000SLA6QX8')
    soup = BeautifulSoup(r.text, 'html.parser')
    data_table = soup.find('tbody')

    JGBs = {}

    for jgb in range(len(data_table) - 1):

        try:
            if 'YEAR ISSUE' in str(data_table.find_all(class_='name')[jgb].text.strip()):
                JGBs[data_table.find_all(class_='isin')[jgb].text.strip()] = [data_table.find_all('tr')[jgb].find_all(class_='shares')[0].text.strip(),
                                                                              data_table.find_all('tr')[jgb].find_all(class_='shares')[1].text.strip()]

        except IndexError:
            break


    JGBList = list(JGBs.keys())
    JGBList.sort()

    return [JGBList, JGBs]


