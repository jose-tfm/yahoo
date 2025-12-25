import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt

def download_stock_data(tickers, years):
    end_date = dt.datetime.now()
    start_time = end_date - dt.timedelta(days=years * 365)
    Adj_close_df = pd.DataFrame()
    for ticker in tickers:
        stocks_data = yf.download(ticker, start=start_time, end=end_date)
        Adj_close_df[ticker] = stocks_data['Close']
    return Adj_close_df

def monthly_return(df):
    monthly_returns = df.resample('M').last().pct_change().dropna()
    return monthly_returns

def portfolio_return(df):
    weights = np.array([1/len(df.columns)] * len(df.columns))
    portfolio_returns = (df * weights).sum(axis=1)
    return portfolio_returns

def portfolio_evolution_with_contributions(portfolio_returns, initial_investment=1000, monthly_contribution=100):
    portfolio_value = [initial_investment]
    
    for i, monthly_return in enumerate(portfolio_returns):
        new_value = portfolio_value[-1] * (1 + monthly_return)
        new_value += monthly_contribution
        portfolio_value.append(new_value)
    
    return pd.Series(portfolio_value[1:], index=portfolio_returns.index)

def calculate_total_contributions(initial_investment, monthly_contribution, num_months):
    return initial_investment + (monthly_contribution * num_months)

############################# S&P 500 #####################################
def comparing_sp500(portfolio_returns):
    sp500_data = yf.download('^GSPC', start=portfolio_returns.index[0], end=portfolio_returns.index[-1])
    if isinstance(sp500_data.columns, pd.MultiIndex):
        sp500_close = sp500_data['Close'].iloc[:, 0] 
    else:
        sp500_close = sp500_data['Close']
    
    sp500_monthly = sp500_close.resample('M').last().pct_change().dropna()
    
    comparison_df = pd.DataFrame({
        'Portfolio': portfolio_returns,
        'S&P 500': sp500_monthly
    }).dropna()
    
    return comparison_df    

def sp500_evolution_with_contributions(portfolio_returns, initial_investment=1000, monthly_contribution=100):

    sp500_data = yf.download('^GSPC', start=portfolio_returns.index[0], end=portfolio_returns.index[-1])
    if isinstance(sp500_data.columns, pd.MultiIndex):
        sp500_close = sp500_data['Close'].iloc[:, 0]
    else:
        sp500_close = sp500_data['Close']
    
    sp500_monthly_returns = sp500_close.resample('M').last().pct_change().dropna()
    sp500_monthly_returns = pd.to_numeric(sp500_monthly_returns, errors='coerce').fillna(0)
    
    print(f"SP500 returns type: {type(sp500_monthly_returns.iloc[0]) if len(sp500_monthly_returns) > 0 else 'Empty'}")
    print(f"SP500 returns sample: {sp500_monthly_returns.head(3)}")
    
    sp500_value = [initial_investment]
    
    for monthly_return in sp500_monthly_returns:
        try:
            return_val = float(monthly_return)
            new_value = sp500_value[-1] * (1 + return_val)
            new_value += monthly_contribution
            sp500_value.append(new_value)
        except (ValueError, TypeError) as e:
            print(f"Error converting {monthly_return} to float: {e}")
            new_value = sp500_value[-1] + monthly_contribution
            sp500_value.append(new_value)
    
    return pd.Series(sp500_value[1:], index=sp500_monthly_returns.index)

############################# S&P 500 END #####################################

if __name__ == "__main__":
    # 'EXXT.DE' - Nasdaq , S&P 500, 'BND', Gold 'GLD' 
    tickers = ['EXXT.DE']
    data = download_stock_data(tickers, 15)
    print("Stock data:")
    print(data.head())
    
    monthly_returns = monthly_return(data)
    
    portfolio_returns = portfolio_return(monthly_returns)

    initial_investment = 1000
    monthly_contribution = 100
    
    portfolio_value = portfolio_evolution_with_contributions(portfolio_returns,  initial_investment=initial_investment, monthly_contribution=monthly_contribution)
    
    # Calculate S&P 500 evolution with same investment strategy
    sp500_value = sp500_evolution_with_contributions(portfolio_returns, initial_investment=initial_investment, monthly_contribution=monthly_contribution)
    
    print(f"\nPortfolio evolution (first 10 months):")
    print(portfolio_value.head(10))
    print(f"\nFinal portfolio value: ${portfolio_value.iloc[-1]:,.2f}")
    print(f"Final S&P 500 value: ${sp500_value.iloc[-1]:,.2f}")
    
    # Calculate total contributions for comparison
    total_contributions = calculate_total_contributions(
        initial_investment, 
        monthly_contribution, 
        len(portfolio_returns)
    )
    print(f"Total contributions: ${total_contributions:,.2f}")
    print(f"Investment gains (Portfolio): ${portfolio_value.iloc[-1] - total_contributions:,.2f}")
    print(f"Investment gains (S&P 500): ${sp500_value.iloc[-1] - total_contributions:,.2f}")
    
    # Plot the evolution
    plt.figure(figsize=(14, 8))
    plt.plot(portfolio_value.index, portfolio_value.values, label=f'Portfolio ({tickers[0]})', linewidth=2)
    plt.plot(sp500_value.index, sp500_value.values, label='S&P 500', linewidth=2)
    
    total_contrib_line = [initial_investment + monthly_contribution * i for i in range(len(portfolio_returns))]
    contribution_series = pd.Series(total_contrib_line, index=portfolio_returns.index)
    plt.plot(contribution_series.index, contribution_series.values, 
             label='Total Contributions', linestyle='--', alpha=0.7)
    
    plt.title(f'{tickers[0]} vs S&P 500\nPortfolio Value Evolution\n(Initial: ${initial_investment}, Monthly: ${monthly_contribution})')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()