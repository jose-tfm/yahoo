import matplotlib.pyplot as plt
import mplfinance as mpf


def plot_stock_data(df, title="Stock Data"):

    plt.figure(figsize=(12, 6), type='candle')
    plt.plot(df.index, df['Close'], label='Close Price')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.show()

def candle_plot_stock_data(df, title="Stock Data"):

    'Represent stock data as a candlestick chart with volume'
    'define custom colors for up and down days.'
    
    colors = mpf.make_marketcolors(up='g', down='r', inherit=True)
    style  = mpf.make_mpf_style(marketcolors=colors)
    mpf.plot(df, type='candle', style=style, title=title, volume=False)