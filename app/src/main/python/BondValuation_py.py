import requests
from bs4 import BeautifulSoup
import numpy as np
from pylab import plt
from datetime import datetime, date
from PIL import Image
import os



def FIV(product, bondDetails):

    product_details = bondDetails[bondDetails.index(product) - 1: bondDetails.index(product) + 40]

    cpn_details = product_details[product_details.index('['):product_details.index(',')]
    cpn = ''
    for cpn_text in cpn_details:
        if cpn_text != '[' and cpn_text != "'" and cpn_text != ",":
            cpn += cpn_text
    cpn = round(float(cpn)/200, 7)

    mat_details = product_details[product_details.index(','):product_details.index(']')]
    mat = ''
    for mat_text in mat_details:
        if mat_text != ' ' and mat_text != ',' and mat_text != "'" and mat_text != ']':
            mat += mat_text
    mat = datetime.strptime(mat, '%m/%d/%Y').date()
    today = date.today()

    payment, remainder = divmod(int((mat - today).days / 365 * 2), 1)
    payment = int(payment)

    face = 100
    yld = cpn

    def BondPrice(face, cpn, yld, pymt, remainder):
        res = [(face * cpn * remainder) / ((1 + yld) ** 1)]
        for i in range(pymt - 1):
            res.append((face * cpn) / ((1 + yld) ** (i+1)))
        res.append((face + (face * cpn)) / (1 + yld) ** pymt)
        return sum(res)


    duration_price = BondPrice(face, cpn, yld, payment, remainder)


    def MacaulayDuration(face, cpn, yld, pymt):
        CashFlow = [face * cpn * remainder]
        CashFlowPV = [CashFlow[-1] / (1 + yld)]
        TimeWeightedCashFlowPV = [CashFlowPV[-1]]


        for cnt in range(pymt - 1):

            CashFlow.append(face * cpn)
            CashFlowPV.append(CashFlow[-1] / (1 + yld) ** (cnt + 1))
            TimeWeightedCashFlowPV.append((cnt + 1) * CashFlowPV[-1])

        #Make sure to also create a condition if maturity within a year later
        CashFlow.append(face + (face * cpn))
        CashFlowPV.append(CashFlow[-1] / (1 + yld) ** (pymt))
        TimeWeightedCashFlowPV.append((pymt) * CashFlowPV[-1])
        Macaulay = sum(TimeWeightedCashFlowPV) / sum(CashFlowPV)

        return Macaulay

    coupon_frequency = 1
    yield_change = 0.01

    MacD = MacaulayDuration(face, cpn, yld, payment)
    ModD = MacD / (1 + (yld / coupon_frequency)) * yield_change


    yld_perm = []
    prices = []


    permutations = np.linspace(yld-0.05, yld+0.05, 1001)
    for i in permutations:
        yld_perm.append(round(i, 4))
        prices.append(BondPrice(face, cpn, yld_perm[-1], payment, remainder))


    prices = prices[1:]
    yld_perm = yld_perm[1:]
    yld_perm_adjusted = []
    for yd in yld_perm:
        yld_perm_adjusted.append(yd + yld)


    duration_line_pos = [duration_price]
    duration_line_neg = []
    for j in range(int(len(permutations)/2)):
        duration_line_pos.append(duration_price + ModD * j)
        duration_line_neg.append(duration_price - ModD * j)

    duration_line_pos.sort(reverse=True)
    duration_line = duration_line_pos + duration_line_neg
    duration_line = duration_line[:-1]


    def Convexity(increase, decrease, initial, yld_delta):
        return yld_delta ** 2 * ((increase + decrease) - (2 * initial)) / (2 * initial * (yld_delta ** 2))

    increase = prices[int(len(prices) / 2 - (1 * 100))]
    decrease = prices[int(len(prices) / 2 + (1 * 100))]
    yld_delta = 0.01


    if product[:5] == 'JP102':
        product_name = 'JN' + str(int(product[5:8]))
        product_fullname = '- Product Name:\n  2 Year Japanese Govt Bond (' + product_name + ').\n\n'
    elif product[:5] == 'JP105':
        product_name = 'JS' + str(int(product[5:8]))
        product_fullname = '- Product Name:\n  5 Year Japanese Govt Bond (' + product_name + ').\n\n'
    elif product[:5] == 'JP110':
        product_name = 'JB' + str(int(product[5:8]))
        product_fullname = '- Product Name:\n  10 Year Japanese Govt Bond (' + product_name + ').\n\n'
    elif product[:5] == 'JP120':
        product_name = 'JL' + str(int(product[5:8]))
        product_fullname = '- Product Name:\n  20 Year Japanese Govt Bond (' + product_name + ').\n\n'
    elif product[:5] == 'JP130':
        product_name = 'JX' + str(int(product[5:8]))
        product_fullname = '- Product Name:\n  30 Year Japanese Govt Bond (' + product_name + ').\n\n'
    elif product[:5] == 'JP140':
        product_name = 'JU' + str(int(product[5:8]))
        product_fullname = '- Product Name:\n  40 Year Japanese Govt Bond (' + product_name + ').\n\n'
    else:
        product_name = 'JBI' + str(int(product[5:8]))
        product_fullname = 'CPI Linked Japanese Govt Bond (' + product_name + ').\n\n'


    cpn_msg = '- Coupon Rate:\n  ' + str(format(cpn/2, '.2%')) + ' per year.\n\n'
    cpn_freg_msg = '- Coupon Payment Frequency:\n  2 times per year.\n\n'
    mat_msg = '- Maturity Date:\n  ' + str(mat) + '.\n\n'
    mac_duration_msg = '- Macaulay Duration:\n  ' + str(round(MacD/2, 2)) + ' years' + '.\n\n'
    mod_duration_msg = '- Modified Duration:\n  JPY ' + str(round(ModD, 5)) + ' for 1bp change in yield.\n\n'
    convexity_msg = '- Convexity Adjustment:\n  ' + str(format(Convexity(increase, decrease, duration_price, yld_delta) / 100, '.5%')) + ' for 1.00% change in yield.\n\n'


    plt.figure(figsize=(10, 10))
    plt.plot(yld_perm_adjusted, duration_line, 'g', label='Duration', linewidth=2)
    plt.plot(yld_perm_adjusted, prices, 'c', label='Price-Yield Curve', linewidth=2)
    plt.plot(yld * 2, duration_price, 'y*', markersize=20)
    plt.title('Bond Duration and Price-Yield Curve: ' + product)
    plt.xlabel('Yield')
    plt.ylabel('Bond Price')
    plt.legend()

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

    return [dir, product_fullname + cpn_msg + cpn_freg_msg +
            mat_msg + mac_duration_msg + mod_duration_msg + convexity_msg]




def JGBISIN():

    try:
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

    except:
        return ['error', None]

    if not JGBs:
        return ['error', None]


    JGBList = list(JGBs.keys())
    JGBList.sort()

    return [JGBList, JGBs]