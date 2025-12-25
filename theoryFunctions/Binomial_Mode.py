import numpy as np
import pandas as pd

''' Shown at A Short Introduction to Computational Methods in Finance "Pedro R. S. Antunes" IST Técnico 
    
    I will try to first apply the Binomial model first with
    for loops and after the same thing but using numpy arrays with vectorization,
    to see the difference in speed 
'''

'''
strike price = k,
Stock Price at Time 0 = S,
risk-free rate = r,
time to maturity = T,
volatility = sigma,
number of steps = N,
beta, value to find u and d
Opt = European or American
typeOpt = Type of Option
'''

''' Try for a European Call/Put Option or American Call/Put Option '''
def Binomial_Model(k, S, r, T, sigma, N, Opt='European', typeOpt='Call'):

    #  Constants
    dt = T / N  # Time step
    beta = 0.5 * ((1/np.exp(r*dt)) + (np.exp(r*dt) * np.exp(sigma**2 * dt))) # Value to find u and d
    u = beta + np.sqrt(beta ** 2 - 1) # Up Factor
    d = beta - np.sqrt(beta ** 2 - 1) # Down Factor
    p = (np.exp(r*dt)- d) / (u - d) # Risk-neutral probability
    print(f'Up Factor: {u}, Down Factor: {d}, Risk-neutral Probability: {p}')

    # Initialize stock prices at maturity
    S_t = np.zeros(N + 1)
    for j in range(N  + 1):
        S_t[j] = S * (u ** j) * d ** (N - j)
    
    if typeOpt == 'Call':
        S_t = np.maximum(S_t - k, 0) # Payoff at maturity Call Option
    else:
        S_t = np.maximum(k - S_t, 0) # Payoff at maturity Put Option

    # Backward induction for option price shown on Pag 76
    if Opt == 'European':
        for i in range(N - 1, -1, -1):
            for j in range(i + 1):
                S_t[j] = np.exp(-r * dt) * (p * S_t[j + 1] + (1 - p) * S_t[j])

    elif Opt == 'American':
            for i in range(N - 1, -1, -1):
                for j in range(i + 1):
                    # Recompute stock price at this node
                    stock_price = S * (u ** j) * (d ** (i - j))
                    continuation_value = np.exp(-r * dt) * (p * S_t[j + 1] + (1 - p) * S_t[j])

                    if typeOpt == 'Call':
                        exercise_value = np.maximum(stock_price - k, 0)
                    else:  # Put
                        exercise_value = np.maximum(k - stock_price, 0)

                    S_t[j] = np.maximum(exercise_value, continuation_value)

    print(f'Option Price: {S_t[0]}')

Binomial_Model(k = 10, S = 5, r = 0.06, T = 1, sigma = 0.3, N = 20, Opt='European', typeOpt='Put')


''' Now we will try to vectorize the code using numpy arrays '''

