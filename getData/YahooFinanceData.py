import yfinance as yf


def get_stock_data(ticker, period="1mo", interval="1d"):
    """
    Parameters:
    ticker (str): Stock ticker symbol.
    period (str): Data period to download.
    interval (str): Data interval.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    return hist

def get_percentage_change(df):
    
    """Calculate percentage change from worst day to current day."""
    worstDay = df['Close'].min()
    currentDay = df['Close'].iloc[-1]
    pct_change = (currentDay - worstDay) / worstDay * 100
    return pct_change