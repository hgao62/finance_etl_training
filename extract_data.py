"""This module contains functions to extract stock data from Yahoo Finance and Tiingo APIs."""
import logging  # 1. import logging
import os
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

def get_stock_history_wrapper(stock: str, start_date:str, 
                              end_date:str, api:str ='yaohoo') -> pd.DataFrame:
    """This function is a wrapper for the get_stock_history function.
    It allows the user to specify the API to use for fetching stock data.

    Args:
        stock (str): stock ticker
        start_date (str): start date in the format YYYY-MM-DD
        end_date (str): _description_
        api (str, optional): _description_. Defaults to 'yaohoo'.

    Raises:
        ValueError: _description_

    Returns:
        pd.DataFrame: _description_
    """
    if api == 'yahoo':
        return get_stock_history(stock, start_date, end_date)
    elif api == 'tiingo':
        return get_stock_history_tiingo(stock, start_date, end_date)
    else:
        raise ValueError(f"Unsupported API: {api}")
def get_stock_history(stock, start_date:str, end_date:str) -> str:
    """
    Function to pull historical stock data for a given stock.

    Arguments:
        stock: individual stock in which user wants to return data for.
        start_date: Start date in the format YYYY-MM-DD.
        end_date: End date in the format YYYY-MM-DD.

    Return:
        Pandas DataFrame with historical stock data.
    """
    cache_filename = f"{stock}_{start_date}_{end_date}.csv"
    cache_path = os.path.join("cache", cache_filename)
    if os.path.exists(cache_path):
        stock_history = pd.read_csv(cache_path)
        logger.info(f"stock_history dataframe loaded from cache: {stock_history}")
        return stock_history
    ticker = yf.Ticker(stock)
    sector = ticker.info["sector"]
    currency_code = ticker.fast_info["currency"]
    stock_history = ticker.history(start_date=start_date,end_date=end_date).reset_index()
    logger.info(f"stock_history dataframe downloaded: {stock_history}")
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
    try:
        stock_history.to_csv(cache_path, index=False)
        logging.info(f"Saved data to cache: {cache_path}")
    except Exception as e:
        logging.error(f"Failed to save cache file: {e}")
    return stock_history


import pandas as pd
import logging
from tiingo import TiingoClient

# Initialize the Tiingo client (make sure your API key is correct)
config = {
    'session': True,
    'api_key': '56d6d8978c631aeeed1ced2bf370b7788c617104'
}

tiingo_client = TiingoClient(config)

def get_stock_history_tiingo(stock: str,  start_date:str, end_date:str) -> pd.DataFrame:
    """
    Function to pull historical stock data for a given stock using Tiingo.

    Arguments:
        stock: individual stock in which user wants to return data for.
        start_date: Start date in the format YYYY-MM-DD.
        end_date: End date in the format YYYY-MM-DD.

    Return:
        Pandas DataFrame with historical stock data.
    """
    # Convert period to dates
    cache_filename = f"{stock}_{start_date}_{end_date}.csv"
    cache_path = os.path.join("cache", cache_filename)
    if os.path.exists(cache_path):
        stock_history = pd.read_csv(cache_path)
        logger.info(f"stock_history dataframe loaded from cache: {stock_history}")
        return stock_history

    try:
        prices = tiingo_client.get_ticker_price(
            stock,
            startDate=start_date,
            endDate=end_date,
            frequency="daily"
        )
    except Exception as e:
        logging.error(f"Error fetching Tiingo data for {stock}: {e}")
        raise

    if not prices:
        logging.warning(f"No data returned for {stock}")
        return pd.DataFrame([], columns=[
            "date", "open", "high", "low", "close", "volume", "dividends",
            "stock", "sector", "currency_code"
        ])

    df = pd.DataFrame(prices)
    df["date"] = pd.to_datetime(df["date"])
    df["stock"] = stock
    df["dividends"] = pd.NA  # Not directly available from Tiingo daily API

    # Sector and currency info are not available from free Tiingo API — set placeholders
    df["sector"] = pd.NA
    df["currency_code"] = "USD"  # Tiingo returns USD for US stocks by default

    # Rename adjusted columns for consistency with Yahoo-style
    df = df.rename(columns={
        "adjOpen": "open",
        "adjHigh": "high",
        "adjLow": "low",
        "adjClose": "close",
        "adjVolume": "volume"
    })

    df = df[[
        "date", "open", "high", "low", "close", "volume",
        "dividends", "stock", "sector", "currency_code"
    ]]
    try:
        stock_history.to_csv(cache_path, index=False)
        logging.info(f"Saved data to cache: {cache_path}")
    except Exception as e:
        logging.error("Failed to save cache file: %s", e)
        
    logging.info(f"stock_history dataframe downloaded: {df}")
    return df


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
    output_columns = [
        "Ticker",
        "Date",
        "Tax Effect Of Unusual Items",
        "Tax Rate For Calcs",
        "Normalized EBITDA",
        "Net Income From Continuing Operation Net Minority Interest",
        "Reconciled Depreciation",
        "Reconciled Cost Of Revenue",
        "EBITDA",
        "EBIT"
    ]
    ticker = yf.Ticker(stock)
    stock_financials = ticker.financials.transpose().reset_index()
    logging.info(f"stock financials dataframe downloaded: {stock_financials}")
    stock_financials.columns.values[0] = "Date"
    stock_financials["Ticker"] = stock
    # output_columns = []
    # output_columns = stock_financials.columns.intersection(columns)
    column_diff = set(output_columns) - set(stock_financials.columns)
    if column_diff:
        stock_financials[list(column_diff)] = 0
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
    output_columns = [ "Date","Ticker","From Currency",
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
    stock_history: pd.DataFrame = get_stock_history("goog")
    
    
    
    res = get_stock_history("SHOP.TO", "5d")
    tickers = [
        "AAPL",
        "MSFT","GOOGL", "AMZN","TSLA",
        # "SPY",
        "COST",
        "WMT",
        "VZ",
        "OKE",
        "GS",
        "JPM",
        "PFE",
        "JNJ",
        "BA",
        "LMT",
        "EQIX",
        "FE",
        "AMC",
        # "NIKE",
    ]
    for ticker in tickers:
        financial = get_stock_financials('SHOP.TO')
        print(financial)
        
        
        
        
    # tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    # get_stock_history("AAPL", "5d")
    # get_exchange_rate("SHOP.TO")
    # get_stock_history("SHOP.TO", "5d")
    # get_stock_history("TSCO.L", "5d")
    # get_major_shareholders("APPL")
    # get_news("APPL")
