import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def fetch_stock_data(ticker, start_date, end_date):

    stock_data = yf.download(ticker, start=start_date, end=end_date)
    if stock_data.empty:
        raise ValueError(f"No data found for ticker: {ticker} between {start_date} and {end_date}")

    return stock_data

def get_moving_average(data, window=30):

    if 'Close' not in data.columns:
        raise ValueError("Data must contain 'Close' column for moving average calculation")

    moving_average = data['Close'].rolling(window=window).mean()
    return moving_average

def get_earnings(ticker):

    stock = yf.Ticker(ticker)
    earnings = stock.earnings
    if earnings.empty:
        raise ValueError(f"No earnings data found for ticker: {ticker}")

    return earnings

def get_income_statement(ticker):

    stock = yf.Ticker(ticker)
    income_statement = stock.financials
    if income_statement.empty:
        raise ValueError(f"No income statement data found for ticker: {ticker}")

    return income_statement

def get_dividends(ticker, start_date=None, end_date=None):

    stock = yf.Ticker(ticker)
    dividends = stock.dividends
    if dividends.empty:
        raise ValueError(f"No dividend data found for ticker: {ticker}")

    if start_date and end_date:
        dividends = dividends[start_date:end_date]

    return dividends


if __name__ == "__main__": 

    ticker = "AAPL"

    print("qual é a data de início e fim?")
    start = input("Data de Iníco (YYYY-MM-DD):")
    end = input("Data de Fim (YYYY-MM-DD):")

    data = fetch_stock_data(ticker, start, end)
    #print(data)
    #dividends = get_dividends(ticker, start, end)

    moving_average = get_moving_average(data)
    #print(data.head(10))
    #print(dividends.head(10))

    
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price')
    plt.plot(moving_average, label='20-Day Moving Average', color='orange')
    plt.title(f'{ticker} Stock Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    #income_statement = get_income_statement(ticker)
    #print(income_statement.head(30))