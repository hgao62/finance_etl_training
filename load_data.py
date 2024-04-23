import sqlite3
from sqlalchemy import create_engine
import sqlalchemy
import logging

logger = logging.getLogger(__name__)
DB_NAME = "stock_db"
CONN = sqlite3.connect(f"./database/{DB_NAME}.db")
ENGINE = create_engine(f"sqlite:///./database/{DB_NAME}.db", echo=True)


def save_df_to_sqllite(df, table_name, if_exists="append", dtype=None) -> None:
    """
    Function to send a dataframe to SQL database.

    Args:
        df: DataFrame to be sent to the SQL database.
        table_name: Name of the table in the SQL database.
        if_exists: Action to take if the table already exists in the SQL database.
                   Options: "fail", "replace", "append" (default: "append").
        dtype: Dictionary of column names and data types to be used when creating the table (default: None).

    Returns:
        None. This function logs a note in the log file to confirm that data has been sent to the SQL database.
    """

    df.to_sql(table_name, ENGINE, if_exists=if_exists, index=False, dtype=dtype)
    logger.info(f"{len(df)} records inserted into {table_name} table")


def drop_existing_tables():
    """
    Function to clear database prior to new batch import.
    To be replaced with drop() or drop_all() method.

    Arguments:
        # empty

    Return:
        # returns note in log file to confirm data has been cleared in PostgreSQL database
    """

    table_list = [
        "earnings",
        "financials",
        "major_share_holders",
        "news",
        "quarterly_earnings",
        "stock_history",
        "stocks_master",
        "exchange_rate",
    ]

    with ENGINE.connect() as conn:
        for table in table_list:
            try:
                conn.execute(f"DROP TABLE IF EXISTS {table};")
                logger.info(f"{table} dropped from database")
            except Exception as e:
                logger.error(f"Error dropping table {table}: {e}")


def convert_df_type_to_db_type(df):
    dtypedict = {}
    dtypes = [str(x) for x in df.dtypes.values]
    for i, j in zip(df.columns, dtypes):
        if "object" in j:
            dtypedict[i] = sqlalchemy.types.VARCHAR(
                length=max(df[i].apply(lambda x: len(str(x))))
            )

        if "datetime" in j:
            dtypedict[i] = sqlalchemy.types.DateTime()

        if "Float" in j:
            dtypedict[i] = sqlalchemy.types.Float(precision=3, asdecimal=True)

        if "int" in j:
            dtypedict[i] = sqlalchemy.types.INT()

    return dtypedict
