import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from scipy.stats import norm
''' Historical Simulation Method for Value at Risk (VaR) Calculation'''
''' Value at Risk (VaR) is a statistical measure used to assess the potential loss in value of a portfolio over a defined period for a given confidence interval.'''

def download_stock_data(tickers, years_back):
    end_date = dt.datetime.now()
    start_date = end_date - dt.timedelta(days=years_back * 365)
    Adj_close_df = pd.DataFrame()
    for ticker in tickers: 
        stocks_data = yf.download(ticker, start=start_date, end=end_date)
        Adj_close_df[ticker] = stocks_data['Close']
    return Adj_close_df

def log_return(df):
    log_returns = np.log(df / df.shift(1))
    log_returns = log_returns.dropna()
    return log_returns

def historical_portfolio_returns(log_returns, portfolio_weights):
    portfolio_log_returns = (log_returns * portfolio_weights).sum(axis=1)
    return portfolio_log_returns

def x_day_returns(portfolio_log_returns, x):
    range_returns = portfolio_log_returns.rolling(window=x).sum()
    range_returns = range_returns.dropna()  
    return range_returns

def var_historical(range_returns, confidence_level=0.95, portofolio_value=100000):
    var = -np.percentile(range_returns, 100 - confidence_level * 100) * portofolio_value
    return var

def historical_var_plot(range_returns, var, confidence_level, portofolio_value):
    # Convert returns to dollar values
    range_returns_dollar = range_returns * portofolio_value
    
    plt.figure(figsize=(12, 6))
    plt.hist(range_returns_dollar.dropna(), bins=50, density=True, alpha=0.7, color='blue', edgecolor='black')
    plt.xlabel(f' {rolling_window} days Portfolio Return (Dollar Value)')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of Portfolio {rolling_window} days Returns (Dollar Value)')
    plt.axvline(-var, color='red', linestyle='dashed', linewidth=2, 
                label=f'VaR at {int(confidence_level*100)}% confidence level: ${abs(var):,.2f}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

tickers = ['SPY', 'BND', 'GLD']
data = download_stock_data(tickers, 10)
print(data.head(10))
log_returns = log_return(data)
portofolio_value = 100000
portfolio_weigths = np.array([1/len(tickers)] * len(tickers))
portfolio_log_returns = historical_portfolio_returns(log_returns, portfolio_weigths)
rolling_window = 30
range_returns = x_day_returns(portfolio_log_returns, rolling_window)
confidence_level = 0.99
var = var_historical(range_returns, confidence_level, portofolio_value)
print(f"Value at Risk (VaR) at {int(confidence_level*100)}% confidence level: ${var:.2f}")
historical_var_plot(range_returns, var, confidence_level, portofolio_value)