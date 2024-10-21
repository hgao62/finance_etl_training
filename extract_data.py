import logging  # 1. import logging

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)

FX_RATES_CURRENY_MAP = {
    "USD": "GBP",
    "CAD": "USD",
    "AUD": "USD",
    "EUR": "USD",
    "GBP": "USD",
}


def get_stock_history(stock, period="1d"):
    """
    Function to pull historical stock data for a given stock.

    Arguments:
        stock: individual stock in which user wants to return data for.

    Return:
        Pandas DataFrame with historical stock data.
    """
    ticker = yf.Ticker(stock)
    sector = ticker.info["sector"]
    currency_code = ticker.fast_info["currency"]
    stock_history = ticker.history(period=period).reset_index()
    logging.info(f"stock_history dataframe downloaded: {stock_history}")
    if stock_history.empty:
        return pd.DataFrame(
            [],
            columns=[
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "dividends",
            "stock",
            "sector",
            "currency_code"
            ],
        )
    stock_history = stock_history.rename(str.lower, axis="columns")
    stock_history["stock"] = stock
    stock_history["date"] = pd.to_datetime(stock_history["date"])
    stock_history["sector"] = sector
    stock_history["currency_code"] =  currency_code
    stock_history = stock_history[
        [
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "dividends",
            "stock",
            "sector",
            "currency_code"
        ]
    ]
    return stock_history


def get_stock_financials(stock):
    """
    Function to pull financials data for a given stock.

    Arguments:
        stock: individual stock in which user wants to return data for.

    Return:
        Pandas DataFrame with financials data.
    """
    columns = [
        "date",
        "Tax Effect Of Unusual Items",
        "Tax Rate For Calcs",
        "Normalized EBITDA",
        "Net Income From Continuing Operation Net Minority Interest",
        "Reconciled Depreciation",
        "Reconciled Cost Of Revenue",
        "EBITDA",
        "EBIT",
        "Net Interest Income",
        "Interest Expense",
        "Interest Income",
        "Normalized Income",
        "Net Income From Continuing And Discontinued Operation",
        "Total Expenses",
        "Total Operating Income As Reported",
        "Diluted Average Shares",
        "Basic Average Shares",
        "Diluted EPS",
        "Basic EPS",
        "Diluted NI Availto Com Stockholders",
        "Net Income Common Stockholders",
        "Net Income",
        "Net Income Including Noncontrolling Interests",
        "Net Income Continuous Operations",
        "Tax Provision",
        "Pretax Income",
        "Other Income Expense",
        "Other Non Operating Income Expenses",
        "Net Non Operating Interest Income Expense",
        "Interest Expense Non Operating",
        "Interest Income Non Operating",
        "Operating Income",
        "Operating Expense",
        "Research And Development",
        "Selling General And Administration",
        "Gross Profit",
        "Cost Of Revenue",
        "Total Revenue",
        "Operating Revenue",
        "stock",
    ]
    ticker = yf.Ticker(stock)
    stock_financials = ticker.financials.transpose().reset_index()
    logging.info(f"stock financials dataframe downloaded: {stock_financials}")
    stock_financials.columns.values[0] = "date"
    stock_financials["stock"] = stock
    output_columns = []
    output_columns = stock_financials.columns.intersection(columns)
    return stock_financials[output_columns]


def get_news(stock):
    """
    Function to pull news data for a given stock.

    Arguments:
        stock: individual stock in which user wants to return data for.

    Return:
        Pandas DataFrame with news data.
    """
    ticker = yf.Ticker(stock)
    news_list = ticker.news
    news_df = pd.DataFrame(news_list)
    logging.info(f"news table dataframe downloaded: {news_df}")
    news_df["Ticker"] = stock
    news_df = news_df.drop(["thumbnail", "relatedTickers"], axis=1)

    return news_df

def get_stock_currency_code(stock: str) -> str:
    """this function should retrieve currency this stock belongs to

    Args:
        stock (str): stock ticker symbol

    Returns:
        pd.DataFrame: trading currency code of the stock
    """
    ticker = yf.Ticker(stock)
    currency_code = ticker.fast_info["currency"]
    return currency_code
    



def clean_stock_history(stock_history):
    """
    Function to clean the stock history data.

    Arguments:
        stock_history: Pandas DataFrame with historical stock data.

    Return:
        Cleaned Pandas DataFrame.
    """
    # Perform data cleaning operations here
    # For example, remove rows with missing values
    stock_history = stock_history.dropna()

    return stock_history


def get_exchange_rate(from_currency, to_currency, period, interval)->pd.DataFrame:
    # 1 get currency code of the stock

    fx_rate_ticker = f"{from_currency}{to_currency}=X"
    fx_rates = yf.download(fx_rate_ticker, period=period, interval=interval)
    fx_rates["Ticker"] = fx_rate_ticker
    fx_rates["From Currency"] = from_currency
    fx_rates["To Currency"] = to_currency
    fx_rates = fx_rates.reset_index()
    output_columns = [
        "Date",
        "Ticker",
        "From Currency",
        "To Currency",  
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
    ]

    return fx_rates[output_columns]


if __name__ == "__main__":
    # res = get_exchange_rate2("USD", "GBP", "5d", "1d")
    res = get_stock_history("SHOP.TO", "5d")
    print(res)
    # tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    # get_stock_history("AAPL", "5d")
    # get_exchange_rate("SHOP.TO")
    # get_stock_history("SHOP.TO", "5d")
    # get_stock_history("TSCO.L", "5d")
    # get_major_shareholders("APPL")
    # get_news("APPL")
