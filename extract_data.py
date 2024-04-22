import pandas as pd
import yfinance as yf

FX_RATES_CURRENY_MAP = {
    "USD": "GBP",
    "CAD": "USD",
    "AUD": "USD",
    "EUR": "USD",
    "GBP": "USD",
}


def get_stock_history(stock):
    """
    Function to pull historical stock data for a given stock.

    Arguments:
        stock: individual stock in which user wants to return data for.

    Return:
        Pandas DataFrame with historical stock data.
    """
    ticker = yf.Ticker(stock)
    stock_history = ticker.history(period="1mo").reset_index()
    stock_history = stock_history.rename(str.lower, axis="columns")
    stock_history["stock"] = stock
    stock_history["date"] = pd.to_datetime(stock_history["date"])
    stock_history = stock_history[
        ["date", "open", "high", "low", "close", "volume", "dividends", "stock"]
    ]
    return stock_history


def get_major_shareholders(stock):
    """
    Function to pull major shareholders data for a given stock.

    Arguments:
        stock: individual stock in which user wants to return data for.

    Return:
        Pandas DataFrame with major shareholders data.
    """
    ticker = yf.Ticker(stock)
    major_share_holders = ticker.major_holders
    major_share_holders = major_share_holders.rename(
        columns={0: "percent", 1: "detail"}
    )
    major_share_holders["stock"] = stock
    return major_share_holders


# get_major_shareholders("IAG.L")


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
    stock_financials.columns.values[0] = "date"
    stock_financials["stock"] = stock
    return stock_financials[columns]


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


def get_exchange_rate(stock, interval="1d", period="1d"):
    currency_code = {}

    ticker = yf.Ticker(stock)
    currency_code = ticker.fast_info["currency"]
    to_currency = FX_RATES_CURRENY_MAP.get(currency_code.upper(), "USD")
    fx_rate_ticker = f"{currency_code}{to_currency}=X"
    fx_rates = yf.download(fx_rate_ticker, period=period, interval=interval)
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


if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
    # get_major_shareholders("APPL")
    get_news("APPL")
