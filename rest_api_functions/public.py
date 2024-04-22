def analyze_stock_performance(stock_history):
    """
    Function to analyze the stock performance.

    Arguments:
        stock_history: Pandas DataFrame with historical stock data.

    Return:
        Dictionary with stock performance metrics.
    """
    # Calculate daily returns
    stock_history["daily_return"] = stock_history["close"].pct_change()

    # Calculate cumulative returns
    stock_history["cumulative_return"] = (1 + stock_history["daily_return"]).cumprod()

    # Calculate other performance metrics
    performance_metrics = {
        "start_date": stock_history["date"].min(),
        "end_date": stock_history["date"].max(),
        "total_return": stock_history["cumulative_return"].iloc[-1] - 1,
        "average_daily_return": stock_history["daily_return"].mean(),
        "volatility": stock_history["daily_return"].std(),
        "max_drawdown": (
            stock_history["cumulative_return"]
            / stock_history["cumulative_return"].cummax()
            - 1
        ).min(),
    }

    return performance_metrics


def analyze_stock_financials(stock_financials, output_columns):
    insights = {}

    # Calculate average values for selected financial metrics
    average_values = stock_financials[output_columns].mean()

    # Calculate maximum values for selected financial metrics
    maximum_values = stock_financials[output_columns].max()

    # Calculate minimum values for selected financial metrics
    minimum_values = stock_financials[output_columns].min()

    # Add the calculated insights to the dictionary
    insights["average_values"] = average_values
    insights["maximum_values"] = maximum_values
    insights["minimum_values"] = minimum_values


def analyze_exchange_rate(fx_rates):
    # Calculate the average exchange rate
    average_exchange_rate = fx_rates["Currency Close"].mean()

    # Calculate the minimum and maximum exchange rate
    min_exchange_rate = fx_rates["Currency Close"].min()
    max_exchange_rate = fx_rates["Currency Close"].max()

    # Add the exchange rate insights to the fx_rates DataFrame
    fx_rates["Average Exchange Rate"] = average_exchange_rate
    fx_rates["Minimum Exchange Rate"] = min_exchange_rate
    fx_rates["Maximum Exchange Rate"] = max_exchange_rate
