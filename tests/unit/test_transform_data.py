import pandas as pd
import os
print( f"current working directory is:{os.getcwd()}")
from transform_data import add_stock_returns
from transform_data import normalize_stock_data

# 1. file name test_file_you_want_to_test.py
# 2. function name test_function_you_want_to_test
    #2.1 passs input sample data to the function
    # 2.2 call the function with the sample data
     # 2.3 compare the output with the expected output
# 3. assert statements to check the expected output

def test_add_stock_returns():
    data = pd.DataFrame({
        "date": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-01-03"]),
        "close": [100, 110, 121]
    })
    result = add_stock_returns(data.copy())
    # Check columns exist
    assert "daily_return" in result.columns
    assert "cumulative_return" in result.columns
    # Check daily_return calculation
    expected_daily = [None, 0.1, 0.1]
    actual_daily = result["daily_return"].round(2).tolist()
    # The first value should be NaN (None after tolist()), rest as expected
    assert actual_daily[0] is None or pd.isna(actual_daily[0])
    assert actual_daily[1:] == expected_daily[1:]
    # Check cumulative_return calculation
    expected_cum = [None, 1.1, 1.21]
    actual_cum = result["cumulative_return"].round(2).tolist()
    assert actual_cum[0] is None or pd.isna(actual_cum[0])
    assert actual_cum[1:] == expected_cum[1:]
    
    



def test_normalize_stock_data():
    input_data = pd.DataFrame({
        "date": pd.to_datetime(["2023-01-01", "2023-01-02"]),
        "open": [100.123, 110.456],
        "high": [105.987, 115.654],
        "low": [99.876, 109.321],
        "close": [104.555, 114.789],
        "volume": [1000, 2000]
    })
    expected_result = pd.DataFrame({
        "trade_date": pd.to_datetime(["2023-01-01", "2023-01-02"]),
        "open": [100.12, 110.46],
        "high": [105.99, 115.65],
        "low": [99.88, 109.32],
        "close": [104.56, 114.79],
        "volume": [1000, 2000]
    })
    actual_result = normalize_stock_data(input_data.copy())
    pd.testing.assert_frame_equal(actual_result.reset_index(drop=True), expected_result.reset_index(drop=True))