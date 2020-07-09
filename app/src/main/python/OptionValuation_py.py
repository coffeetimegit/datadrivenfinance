import numpy as np
import numpy.random as npr


def OPV(S0, K, r, T, option_type):

    M = 50
    I = 10000
    sigma = 0.25


    def standard_normal_dist(M, I, anti_paths=True, mo_match=True):
        if anti_paths is True:
            sn = npr.standard_normal((M + 1, int(I / 2)))
            sn = np.concatenate((sn, -sn), axis=1)
        else:
            sn = npr.standard_normal((M + 1, I))
        if mo_match is True:
            sn = (sn - sn.mean()) / sn.std()
        return sn


    def monte_carlo_brownian_motion(S0, K, r, T, option_type):
        try:
            S0 = float(S0)
        except:
            return 'Error: Initial Price needs to be a number!'
        try:
            K = float(K)
        except:
            return 'Error: Strike Price needs to be a number!'
        try:
            if '%' in r:
                r = float(r[:r.index('%')]) / 100
            else:
                r = float(r)
        except:
            return 'Error: Risk Free Interest Rate needs to be a number!'
        try:
            T = float(T)
        except:
            return 'Error: Time Horizon needs to be a number!'
        if option_type == 'Call Option':
            option_type = 'Call'
        else:
            option_type = 'Put'

        dt = T / M
        S = np.zeros((M + 1, I))
        S[0] = S0
        sn = standard_normal_dist(M, I)
        for t in range(1, M + 1):
            S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * sn[t])
        if option_type == 'Call':
            hT = np.maximum(S[-1] - K, 0)
        else:
            hT = np.maximum(K - S[-1], 0)
        C0 = np.exp(-r * T) * np.mean(hT)


        Title = 'Option Valuation with the following parameters:'


        return Title + '\n'*2 + 'Initial Price: ' + str(S0) + '\n' +\
               'Strike Price: ' + str(K) + '\n' +\
               'Risk Free Interest Rate: ' + str(format(r, '.2%')) + '\n' +\
               'Time Horizon: ' + str(T) + ' year\n' +\
               'Option Type: ' + option_type + ' option' + '\n'*2 + \
               'Stochastic differential equation:' + '\n' + 'dS(t) = rS(t)dt + σS(t)dZ(t)' + '\n'*2 +\
               'Distribution method:' + '\n' + 'Standard Normal Distribution' + '\n'*2 + \
               option_type + ' option value: ' + str(C0.round(2))


    return monte_carlo_brownian_motion(S0, K, r, T, option_type)