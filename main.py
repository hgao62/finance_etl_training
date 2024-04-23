from typing import List
import extract_data
import load_data
import logging  # 1. import logging
from load_data import DBType

logging.basicConfig(
    filemode="a",
    format="%(asctime)s - %(levelname)s- %(filename)s:%(lineno)s  - %(message)s",
    filename="project_loging.log",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def main(
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
    if drop_existing_tables:
        load_data.drop_existing_tables(db_engine)
    for stock in tickers:
        stock_history = extract_data.get_stock_history(stock, period)

        stock_financials = extract_data.get_stock_financials(stock)
        news = extract_data.get_news(stock)
        fx_rates = extract_data.get_exchange_rate(stock, interval, period)

        load_data.save_df_to_db(stock_history, "stock_history", engine=db_engine)
        load_data.save_df_to_db(stock_financials, "financials", engine=db_engine)
        load_data.save_df_to_db(news, "news", engine=db_engine)
        load_data.save_df_to_db(fx_rates, "exchange_rate", engine=db_engine)

    logger.info("Process finished successfully")


if __name__ == "__main__":
    tickers = [
        # "AAPL",
        # "MSFT",
        # "GOOGL",
        # "AMZN",
        # "TSLA",
        "SPY",
        "COST",
        "WMT",
        "TGT",
        "AMC",
        "NIKE",
    ]

    tickers = ["IAG.L"]
    main(tickers, drop_existing_tables=True)
