import pandas as pd
from extract_data import get_exchange_rate

FX_RATE_CACHE = {}

def add_stock_returns(stock_history)-> pd.DataFrame:
    """
    Function to enrich the stock history data.

    Arguments:
        stock_history: Pandas DataFrame with historical stock data.

    Return:
        Enriched Pandas DataFrame.
    """
    # Perform data enrichment operations here
    # For example, calculate daily returns
    stock_history = stock_history.sort_values(by="date")
    stock_history["daily_return"] = stock_history["close"].pct_change()
    stock_history["cumulative_return"] = (1 + stock_history["daily_return"]).cumprod()
    return stock_history



def standardize_price_to_usd(stock_history:pd.DataFrame)-> pd.DataFrame:
    stock_currency_code = stock_history.iloc[0]["currency_code"]
    if (stock_currency_code, "USD") in FX_RATE_CACHE:
        fx_rate = FX_RATE_CACHE[(stock_currency_code, "USD")]
    else:
        fx_rate_df = get_exchange_rate(stock_currency_code,"USD","1d","1d")
        fx_rate = fx_rate_df.iloc[0]['Close']
        FX_RATE_CACHE[(stock_currency_code, "USD")] = fx_rate
        
    stock_history["usd_close"] = stock_history["close"] * fx_rate
    return stock_history
    

def normalize_stock_data(stock_history: pd.DataFrame) -> pd.DataFrame:
    """
    Function to standardize stock data format, rounding values and renaming columns.

    Args:
        stock_history: Pandas DataFrame with historical stock data.

    Returns:
        Pandas DataFrame with standardized format.
    """
    stock_history[['open', 'high', 'low', 'close']] = stock_history[['open', 'high', 'low', 'close']].round(2)
    stock_history.rename(columns={'date': 'trade_date'}, inplace=True)
    return stock_history


def calculate_moving_average(stock_history: pd.DataFrame, window: int = 5) ->pd.DataFrame:
    stock_history['MA'] = stock_history['close'].rolling(window=window).mean()
    return stock_history

def get_top_bottom_days(stock_history: pd.DataFrame, n: int =5) -> pd.DataFrame:
    top_n = stock_history.nlargest(n,'close')
    bottom_n = stock_history.nsmallest(n, 'close')
    
    top_bottom_days = pd.concat([top_n,bottom_n])
    return top_bottom_days


def filter_significant_volume(stock_history: pd.DataFrame, threshold: int = 1_000_000) -> pd.DataFrame:
    """
    Filters stock history for days with significant trading volume.

    Args:
        stock_history: DataFrame with historical stock data.
        threshold: Volume threshold for filtering.

    Returns:
        Filtered DataFrame with rows where trading volume exceeds threshold.
    """
    high_volume_days = stock_history[stock_history['volume'] > threshold]
    
    return high_volume_days



def group_by_sector(stock_history: pd.DataFrame) -> pd.DataFrame:
    """
    Groups stock data by sector and calculates average closing price and volume for each sector.

    Args:
        stock_data: DataFrame with stock data, including sector.

    Returns:
        DataFrame grouped by sector with mean closing price and volume.
    """
    
    stock_history_grouped = stock_history.groupby('sector').agg({'close':'mean', 'volume':'mean'}).reset_index()
    stock_history_grouped = stock_history_grouped.rename(columns = {'close':"avg_close", "volume":"avg_volume"})
    return stock_history_grouped



def merge_stock_with_fx(stock_history: pd.DataFrame, fx_rates: pd.DataFrame) -> pd.DataFrame:
    """
    Merges stock history with foreign exchange rate data to adjust prices to USD.

    Args:
        stock_history: DataFrame with historical stock data.
        fx_rates: DataFrame with foreign exchange rates.

    Returns:
        Merged DataFrame with adjusted prices.
    """
    stock_history['date'] = pd.to_datetime(stock_history['date'])
    fx_rates['date'] = pd.to_datetime(fx_rates['Date'])
    
    # Merge on date
    merged_df = pd.merge(stock_history, fx_rates, on='date', how='inner')
    
    # Adjust stock price to USD
    merged_df['close_usd'] = merged_df['close'] * merged_df['Close']
    return merged_df
