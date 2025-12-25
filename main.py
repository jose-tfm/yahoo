import streamlit as st
from getData.YahooFinanceData import get_stock_data, get_percentage_change
from supportFunctions.plots import candle_plot_stock_data


if __name__ == "__main__":

    st.title("Stock Analysis")
    st.info("We can use: **1y**, **5y**, **max**, **ytd**, **3mo**, **6mo**")


    stock = 'AAPL'
    stock2 = 'MSFT'
    period = "ytd"
    df1 = get_stock_data(stock, period=period, interval="1d")
    df2 = get_stock_data(stock2, period=period, interval="1d")
    st.dataframe(df1)
    st.dataframe(df2)



    pct_change = get_percentage_change(df1)
    # Print the percentage change
    print(f"Percentage change in closing prices: {pct_change}%")
    
    # Find the index (date) with the maximum dividend
    max_dividend_index = df1['Dividends'].idxmax()
    print("Date with maximum dividend:", max_dividend_index)

    # Plot the stock data:
    candle_plot_stock_data(df1, title=f"{stock} Stock Data - Last {period}")