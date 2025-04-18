"""Project entry file"""
import logging  # 1. import logging
from typing import List

import extract_data
import load_data
from load_data import DBType
from transform_data import add_stock_returns, standardize_price_to_usd

# 2. Add logging configuration
logging.basicConfig(
    filemode="a",
    format="%(asctime)s - %(levelname)s- %(filename)s:%(lineno)s  - %(message)s",
    filename="project_loging.log",
    level=logging.INFO,
)

# 3. Create a logger object
logger = logging.getLogger(__name__)

import pandas as pd


def run_pipeline(
    tickers: List[str],
    period: str = "1d",
    interval: str = "1d",
    drop_existing_tables: bool = False,
    db_type: DBType = DBType.MYSQL,
):
    db_engine = load_data.DB_ENGINE_MAP[db_type]
    logger.info(
        "Running main function with parameters tickers:%s period:%s interval: %s  db_type: %s",
        tickers,
        period,
        interval,
        db_type,
    )
    print(f" stock list type is: {type(tickers)}")
    if drop_existing_tables:
        load_data.drop_existing_tables(db_engine)

    for stock in tickers:
        logger.info("Getting data for ticker %s", stock)
        stock_history: pd.DataFrame = extract_data.get_stock_history_wrapper(stock, period)
        stock_history = add_stock_returns(stock_history)
        stock_history = standardize_price_to_usd(stock_history)
        load_data.save_df_to_db(stock_history, "stock_history", engine=db_engine)

        news = extract_data.get_news(stock)
        load_data.save_df_to_db(news, "news", engine=db_engine)
        # fx_rates = extract_data.get_exchange_rate(stock, interval, period)
        # load_data.save_df_to_db(fx_rates, "exchange_rate", engine=db_engine)

        stock_financials = extract_data.get_stock_financials(stock)
        load_data.save_df_to_db(stock_financials, "financials", engine=db_engine)

    logger.info("Process finished successfully")


def return_data_frame() -> str:
    data = [[1, 2, 3], [3, 4, 5], [6, 7, 8]]
    return pd.DataFrame(data)


if __name__ == "__main__":
    tickers = [
        "AAPL",
        # "NIKE",
    ]
    # SECTOR ticker example https://www.sectorspdrs.com/sectortracker
    # tickers = ["AAPL", "AMZN", "COST"]
    # tickers = ["SHOP.TO"]
    PERIOD = "1d"
    # tickers = ["AAPL", "Meta"]
    run_pipeline(tickers, period=PERIOD, db_type="mysql", drop_existing_tables=True)
