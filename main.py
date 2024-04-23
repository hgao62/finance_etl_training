from typing import List
import extract_data
import load_data
import logging  # 1. import logging

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
):
    logger.info(
        "Running main function with parameters tickers:%s period:%s interval%s",
        tickers,
        period,
        interval,
    )
    if drop_existing_tables:
        load_data.drop_existing_tables()
    for stock in tickers:
        stock_history = extract_data.get_stock_history(stock, period)

        stock_financials = extract_data.get_stock_financials(stock)
        news = extract_data.get_news(stock)
        fx_rates = extract_data.get_exchange_rate(stock, interval, period)

        load_data.save_df_to_sqllite(stock_history, "stock_history")
        load_data.save_df_to_sqllite(stock_financials, "financials")
        load_data.save_df_to_sqllite(news, "news")
        load_data.save_df_to_sqllite(fx_rates, "exchange_rate")


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
    logger.info("Process started")
    tickers = ["IAG.L"]
    main(tickers)
    logger.info("Process finished successfully")
