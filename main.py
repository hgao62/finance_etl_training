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
    start_date: str,
    end_date: str,
    interval: str = "1d",
    drop_existing_tables: bool = False,
    db_type: DBType = DBType.MYSQL,
):
    """_summary_

    Args:
        tickers (List[str]): _description_
        period (str, optional): _description_. Defaults to "1d".
        interval (str, optional): _description_. Defaults to "1d".
        drop_existing_tables (bool, optional): _description_. Defaults to False.
        db_type (DBType, optional): _description_. Defaults to DBType.MYSQL.
    """
    db_engine = load_data.DB_ENGINE_MAP[db_type]
    logger.info(
        "Running main function with parameters tickers:%s start_date:%s end_date:%s interval: %s  db_type: %s",
        tickers,
        start_date,
        end_date,
        interval,
        db_type,
    )
    print(f" stock list type is: {type(tickers)}")
    if drop_existing_tables:
        load_data.drop_existing_tables()

    for stock in tickers:
        logger.info("Getting data for ticker %s", stock)
        stock_history: pd.DataFrame = extract_data.get_stock_history_wrapper(
            stock, start_date,end_date,
        )
        stock_history = add_stock_returns(stock_history)
        stock_history = standardize_price_to_usd(stock_history)
        load_data.save_df_to_db(stock_history, "stock_history")

        news = extract_data.get_news(stock)
        load_data.save_df_to_db(news, "news")
        # fx_rates = extract_data.get_exchange_rate(stock, interval, period)
        # load_data.save_df_to_db(fx_rates, "exchange_rate", engine=db_engine)

        stock_financials = extract_data.get_stock_financials(stock)
        load_data.save_df_to_db(stock_financials, "financials")

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
    from datetime import datetime, timedelta
    end_date = datetime.today()
    start_date = end_date - timedelta(days=1)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    run_pipeline(tickers, start_date,end_date, db_type="mysql", drop_existing_tables=True)
