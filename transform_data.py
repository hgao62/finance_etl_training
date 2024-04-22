import pandas as pd


def enrich_exchange_rate_table(exchange_rate_table):
    """
    Function to enrich exchange rate table with additional columns.

    Arguments:
        exchange_rate_table: Pandas DataFrame with exchange rate data.

    Return:
        Pandas DataFrame with additional columns.
    """
    exchange_rate_table["date"] = pd.to_datetime(exchange_rate_table["date"])
    exchange_rate_table["year"] = exchange_rate_table["date"].dt.year
    exchange_rate_table["month"] = exchange_rate_table["date"].dt.month
    exchange_rate_table["day"] = exchange_rate_table["date"].dt.day
    exchange_rate_table["day_of_week"] = exchange_rate_table["date"].dt.dayofweek
    exchange_rate_table["week_of_year"] = (
        exchange_rate_table["date"].dt.isocalendar().week
    )
    exchange_rate_table["quarter"] = exchange_rate_table["date"].dt.quarter
    exchange_rate_table["currency"] = exchange_rate_table["stock"].str[-3:]
    return exchange_rate_table
