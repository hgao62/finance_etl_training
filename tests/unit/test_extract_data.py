import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
import yfinance as yf

from extract_data import get_stock_financials,get_stock_history


# tests/test_your_module.py

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd

EXPECTED_COLUMNS = [
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "dividends",
    "stock",
    "sector",
]

def mock_ticker(info, history_data):
    mock = MagicMock()
    mock.info = info
    mock.history.return_value = history_data
    return mock

def test_get_stock_history_valid():
    stock_symbol = "AAPL"
    period = "1y"
    mock_info = {"sector": "Technology"}
    mock_history = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=5, freq='D'),
        "Open": [150, 152, 153, 154, 155],
        "High": [151, 153, 154, 155, 156],
        "Low": [149, 151, 152, 153, 154],
        "Close": [150.5, 152.5, 153.5, 154.5, 155.5],
        "Volume": [1000000, 1100000, 1200000, 1300000, 1400000],
        "Dividends": [0, 0, 0, 0, 0],
    })
    with patch('extract_data.yf.Ticker') as mock_ticker_class:
        mock_ticker_instance = mock_ticker(mock_info, mock_history)
        mock_ticker_class.return_value = mock_ticker_instance
        df = get_stock_history(stock_symbol, period)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == EXPECTED_COLUMNS
        assert not df.empty
        assert df["stock"].unique() == [stock_symbol]
        assert df["sector"].unique() == [mock_info["sector"]]
        assert len(df) == 5

def test_get_stock_history_no_sector():
    stock_symbol = "UNKNOWN"
    period = "1y"
    mock_info = {}
    mock_history = pd.DataFrame({
        "Date": pd.date_range(start="2023-01-01", periods=3, freq='D'),
        "Open": [200, 202, 204],
        "High": [201, 203, 205],
        "Low": [199, 201, 203],
        "Close": [200.5, 202.5, 204.5],
        "Volume": [500000, 600000, 700000],
        "Dividends": [0, 0, 0],
    })
    with patch('extract_data.yf.Ticker') as mock_ticker_class:
        mock_ticker_instance = mock_ticker(mock_info, mock_history)
        mock_ticker_class.return_value = mock_ticker_instance
        df = get_stock_history(stock_symbol, period)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == EXPECTED_COLUMNS
        assert not df.empty
        assert df["stock"].unique() == [stock_symbol]
        assert df["sector"].unique() == ["Unknown"]
        assert len(df) == 3

def test_get_stock_history_empty():
    stock_symbol = "INVALID"
    period = "1y"
    mock_info = {"sector": "Finance"}
    mock_history = pd.DataFrame()
    with patch('extract_data.yf.Ticker') as mock_ticker_class:
        mock_ticker_instance = mock_ticker(mock_info, mock_history)
        mock_ticker_class.return_value = mock_ticker_instance
        df = get_stock_history(stock_symbol, period)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == EXPECTED_COLUMNS
        assert df.empty

def test_get_stock_history_exception():
    stock_symbol = "ERROR"
    period = "1y"
    with patch('extract_data.yf.Ticker') as mock_ticker_class:
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.history.side_effect = Exception("API failure")
        mock_ticker_instance.info = {"sector": "Healthcare"}
        mock_ticker_class.return_value = mock_ticker_instance
        with pytest.raises(ValueError) as exc_info:
            get_stock_history(stock_symbol, period)
        assert "Failed to retrieve data for stock: ERROR." in str(exc_info.value)

def test_get_stock_history_custom_period():
    stock_symbol = "GOOGL"
    period = "6mo"
    mock_info = {"sector": "Technology"}
    mock_history = pd.DataFrame({
        "Date": pd.date_range(start="2023-07-01", periods=10, freq='D'),
        "Open": [2700 + i for i in range(10)],
        "High": [2705 + i for i in range(10)],
        "Low": [2695 + i for i in range(10)],
        "Close": [2702 + i for i in range(10)],
        "Volume": [1500000 + i*10000 for i in range(10)],
        "Dividends": [0]*10,
    })
    with patch('extract_data.yf.Ticker') as mock_ticker_class:
        mock_ticker_instance = mock_ticker(mock_info, mock_history)
        mock_ticker_class.return_value = mock_ticker_instance
        df = get_stock_history(stock_symbol, period)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == EXPECTED_COLUMNS
        assert not df.empty
        assert df["stock"].unique() == [stock_symbol]
        assert df["sector"].unique() == [mock_info["sector"]]
        assert len(df) == 10

def test_get_stock_history_empty_structure():
    stock_symbol = "EMPTY"
    period = "1d"
    mock_info = {"sector": "Utilities"}
    mock_history = pd.DataFrame()
    with patch('extract_data.yf.Ticker') as mock_ticker_class:
        mock_ticker_instance = mock_ticker(mock_info, mock_history)
        mock_ticker_class.return_value = mock_ticker_instance
        df = get_stock_history(stock_symbol, period)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == EXPECTED_COLUMNS
        assert df.empty

def test_get_stock_history_date_format():
    stock_symbol = "MSFT"
    period = "1mo"
    mock_info = {"sector": "Technology"}
    mock_history = pd.DataFrame({
        "Date": ["2023-09-01", "2023-09-02", "2023-09-03"],
        "Open": [300, 305, 310],
        "High": [305, 310, 315],
        "Low": [295, 300, 305],
        "Close": [302, 307, 312],
        "Volume": [2000000, 2100000, 2200000],
        "Dividends": [0, 0, 0],
    })
    with patch('extract_data.yf.Ticker') as mock_ticker_class:
        mock_ticker_instance = mock_ticker(mock_info, mock_history)
        mock_ticker_class.return_value = mock_ticker_instance
        df = get_stock_history(stock_symbol, period)
        assert pd.api.types.is_datetime64_any_dtype(df['date'])
        assert df["stock"].unique() == [stock_symbol]
        assert df["sector"].unique() == [mock_info["sector"]]
