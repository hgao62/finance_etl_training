import pandas as pd


def enrich_stock_history(stock_history):
    """
    Function to enrich the stock history data.

    Arguments:
        stock_history: Pandas DataFrame with historical stock data.

    Return:
        Enriched Pandas DataFrame.
    """
    # Perform data enrichment operations here
    # For example, calculate daily returns
    stock_history["daily_return"] = stock_history["close"].pct_change()
    stock_history["cumulative_return"] = (1 + stock_history["daily_return"]).cumprod()
    return stock_history
