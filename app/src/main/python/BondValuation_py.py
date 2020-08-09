from datetime import datetime, date
import numpy as np
from pylab import plt
from PIL import Image
import os



def FIV(product, coupon, maturity):

    cpn = round(float(coupon)/200, 7)

    mat = datetime.strptime(maturity, '%m/%d/%Y').date()
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

        CashFlow.append(face + (face * cpn))
        CashFlowPV.append(CashFlow[-1] / (1 + yld) ** (pymt))
        TimeWeightedCashFlowPV.append((pymt) * CashFlowPV[-1])
        Macaulay = sum(TimeWeightedCashFlowPV) / sum(CashFlowPV)

        return Macaulay

    coupon_frequency = 1
    yield_change = 0.01


    if payment <= 1:
        error_msg = 'Error: Sorry unable to perform valuation on JGB maturing within 1 year.'
        return ['error', error_msg]

    else:
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
        product_name = 'JN{}'.format(str(int(product[5:8])))
        product_fullname = '- Product Name:\n  2 Year Japanese Govt Bond ({}).\n\n'.format(product_name)
    elif product[:5] == 'JP105':
        product_name = 'JS{}'.format(str(int(product[5:8])))
        product_fullname = '- Product Name:\n  5 Year Japanese Govt Bond ({}).\n\n'.format(product_name)
    elif product[:5] == 'JP110':
        product_name = 'JB{}'.format(str(int(product[5:8])))
        product_fullname = '- Product Name:\n  10 Year Japanese Govt Bond ({}).\n\n'.format(product_name)
    elif product[:5] == 'JP120':
        product_name = 'JL{}'.format(str(int(product[5:8])))
        product_fullname = '- Product Name:\n  20 Year Japanese Govt Bond ({}).\n\n'.format(product_name)
    elif product[:5] == 'JP130':
        product_name = 'JX{}'.format(str(int(product[5:8])))
        product_fullname = '- Product Name:\n  30 Year Japanese Govt Bond ({}).\n\n'.format(product_name)
    elif product[:5] == 'JP140':
        product_name = 'JU{}'.format(str(int(product[5:8])))
        product_fullname = '- Product Name:\n  40 Year Japanese Govt Bond ({}).\n\n'.format(product_name)
    else:
        product_name = 'JBI{}'.fomrat(str(int(product[5:8])))
        product_fullname = '- Product Name:\n  CPI Linked Japanese Govt Bond ({}).\n\n'.format(product_name)


    cpn_msg = '- Coupon Rate:\n  {} per year.\n\n'.format(str(format(cpn/2, '.2%')))
    cpn_freg_msg = '- Coupon Payment Frequency:\n  2 times per year.\n\n'
    mat_msg = '- Maturity Date:\n  {}.\n\n'.format(str(mat))
    mac_duration_msg = '- Macaulay Duration:\n  {} years.\n\n'\
        .format(str(round(MacD/2, 2)))
    mod_duration_msg = '- Modified Duration:\n  JPY {} for 1bp change in yield.\n\n'\
        .format(str(round(ModD, 5)))
    convexity_msg = '- Convexity Adjustment:\n  {} for 1.00% change in yield.\n\n'\
        .format(str(format(Convexity(increase, decrease, duration_price, yld_delta) / 100, '.5%')))


    plt.figure(figsize=(10, 10))
    plt.plot(yld_perm_adjusted, duration_line, 'g', label='Duration', linewidth=2)
    plt.plot(yld_perm_adjusted, prices, 'c', label='Price-Yield Curve', linewidth=2)
    plt.plot(yld * 2, duration_price, 'y*', markersize=20)
    plt.title('Bond Duration and Price-Yield Curve: {}'.format(product))
    plt.xlabel('Yield')
    plt.ylabel('Bond Price')
    plt.legend(fontsize='large')

    dir = '{}{}'.format(os.environ["HOME"], '/bondgraph.png')
    plt.savefig(dir)

    image = Image.open(dir)

    width, height = image.size
    left = width/19
    top = height/19
    right = width
    bottom = height
    image = image.crop((left, top, right, bottom))

    image.rotate(270).save(dir)

    return [dir, '{}{}{}{}{}{}{}'.format(product_fullname, cpn_msg, cpn_freg_msg,
            mat_msg, mac_duration_msg, mod_duration_msg, convexity_msg)]