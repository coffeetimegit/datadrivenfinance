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

        Title = 'Option Valuation with the following parameters:\n\n'
        S0_desc = 'Initial Price: {}\n'.format(str(S0))
        K_desc = 'Strike Price: {}\n'.format(str(K))
        r_desc = 'Risk Free Interest Rate: {}\n'.format(str(format(r, '.2%')))
        T_desc = 'Time Horizon: {} year\n'.format(str(T))
        option_type_desc = 'Option Type: {} option \n\n'.format(option_type)
        valuation_desc = 'Stochastic differential equation:\ndS(t) = rS(t)dt + σS(t)dZ(t)\n\n'
        distribution_desc = 'Distribution method:\nStandard Normal Distribution\n\n'
        valuation_res = '{} option value: {}'.format(option_type, str(C0.round(2)))

        return '{}{}{}{}{}{}{}{}{}'.format(Title, S0_desc, K_desc, r_desc, T_desc, option_type_desc,
                                           valuation_desc, distribution_desc, valuation_res)


    return monte_carlo_brownian_motion(S0, K, r, T, option_type)