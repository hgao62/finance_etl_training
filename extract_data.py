import pandas as pd
import yfinance as yf
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging  # 1. import logging

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
            ],
        )
    stock_history = stock_history.rename(str.lower, axis="columns")
    stock_history["stock"] = stock
    stock_history["date"] = pd.to_datetime(stock_history["date"])

    stock_history = stock_history[
        ["date", "open", "high", "low", "close", "volume", "dividends", "stock"]
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

    # # Extract keywords from news headlines
    # keywords = []
    # """
    # >>> import nltk
    # >>> nltk.download('stopwords')
    # nltk.download('punkt')
    # """
    # stop_words = set(stopwords.words("english"))
    # for headline in news_df["title"]:
    #     tokens = word_tokenize(headline)
    #     keywords.extend(
    #         [word.lower() for word in tokens if word.lower() not in stop_words]
    #     )

    # # Count the frequency of each keyword
    # keyword_freq = nltk.FreqDist(keywords)

    # # Get the top 5 most common keywords
    # top_keywords = keyword_freq.most_common(5)

    # # Add the top keywords to the news DataFrame
    # news_df["top_keywords"] = [
    #     ", ".join([keyword for keyword, _ in top_keywords])
    # ] * len(news_df)

    return news_df


def get_exchange_rate(stock, interval="1d", period="1d"):
    currency_code = {}

    ticker = yf.Ticker(stock)
    try:
        currency_code = ticker.fast_info["currency"]
    except KeyError:
        return pd.DataFrame(
            [],
            columns=[
                "Date",
                "Open",
                "Currenyc Close",
                "Low",
                "High",
                "Fromcurrency",
                "Tocurrency",
                "Exchange Id",
                "Currency Date key",
                "Ticker",
                "Currency Code",
            ],
        )

    to_currency = FX_RATES_CURRENY_MAP.get(currency_code.upper(), "USD")
    fx_rate_ticker = f"{currency_code}{to_currency}=X"
    fx_rates = yf.download(fx_rate_ticker, period=period, interval=interval)
    logging.info(f"exchange rate dataframe downloaded: {fx_rates}")
    fx_rates = fx_rates[["Open", "Close", "Low", "High"]]
    fx_rates.reset_index(inplace=True)
    fx_rates["Fromcurrency"] = currency_code
    fx_rates["Tocurrency"] = to_currency
    fx_rates["Exchange Id"] = fx_rates["Date"].dt.strftime("%m%d%Y") + (
        fx_rates["Fromcurrency"]
    )
    fx_rates["Currency Date key"] = fx_rates["Date"].dt.strftime("%m%d%Y")

    # rename columns
    fx_rates["Ticker"] = stock
    fx_rates["Currency Code"] = to_currency
    fx_rates.rename(columns={"Close": "Currency Close"}, inplace=True)

    return fx_rates


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


if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    # get_major_shareholders("APPL")
    # get_news("APPL")
