import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

'''
Kelly Criterion Implementation for Trading Strategy
Interesting things: 
1. Optimal bet sizing based on win probability and payout ratio.
2. It is hard to get these values in real life.
3. Overbetting can lead to ruin, underbetting leads to suboptimal growth.
4. In real market strategies, consider transaction costs, slippage, and changing probabilities.
'''

def kelly_criterion(win_prob, b): 

    if not (0 < win_prob < 1):
        raise ValueError("Win probability must be between 0 and 1.")
    
    kelly_fraction = win_prob - (1 - win_prob) / b
    return kelly_fraction


def simulate_trading_stategy(initial_capital, win_prob, b, num_trades):

    kelly = kelly_criterion(win_prob, b)
    capital = initial_capital
    capital_history = [capital]

    for i in range(num_trades): 
        if np.random.rand() < win_prob:
            capital += capital * kelly * b
        else:
            capital -= capital * kelly
        capital_history.append(capital)
    
    print("Final capital after {} trades: {:.2f}".format(num_trades, capital))
    return capital_history

def plot_capital_growth(capital_history):
    plt.figure(figsize=(10, 6))
    plt.plot(capital_history)
    plt.title("Capital Growth Over Time")
    plt.xlabel("Number of Trades")
    plt.ylabel("Capital")
    plt.show()

if __name__ == "__main__":
    initial_capital = 1000
    win_prob = 0.5
    b = 2
    num_trades = 100

    capital_history = simulate_trading_stategy(initial_capital, win_prob, b, num_trades)
    plot_capital_growth(capital_history)