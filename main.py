import streamlit as st
import plotly.graph_objects as go
from getData.YahooFinanceData import get_stock_data, get_percentage_change
from supportFunctions.plots import candle_plot_stock_data

if __name__ == "__main__":

    st.title("Stock Analysis")
    st.info("We can use: **1y**, **5y**, **max**, **ytd**, **3mo**, **6mo**")
    choice = st.chat_input("Enter the stock ticker symbol (e.g., AAPL, COIN): ")
    stockChoosen = choice.upper() if choice else "AAPL"

    period = "1y"
    df1 = get_stock_data(stockChoosen, period=period, interval="1d")

    # Check if data was retrieved successfully
    if df1.empty:
        st.error("Failed to retrieve stock data. Please check your internet connection and try again.")
        st.stop()

    # Candlestick chart for stock 1
    fig1 = go.Figure(data=[go.Candlestick(x=df1.index,
                    open=df1['Open'],
                    high=df1['High'],
                    low=df1['Low'],
                    close=df1['Close'],
                    increasing_line_color='green',
                    decreasing_line_color='red')])
    fig1.update_layout(title=f'{stockChoosen} Candlestick Chart', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig1)

    pct_change = get_percentage_change(df1)
    st.write(f"Percentage change in closing prices from worst day to current day: {pct_change:.2f}%")