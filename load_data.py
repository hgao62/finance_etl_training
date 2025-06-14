
import logging
from enum import Enum
from getpass import getpass

import pandas as pd
import sqlalchemy
from mysql.connector import Error, connect
from sqlalchemy import create_engine

from config import ENV


class DBType(Enum):
    SQLITE = "sqlite"
    MYSQL = "mysql"


logger = logging.getLogger(__name__)
# DB_NAME = "stock_db"
# CONN = sqlite3.connect(f"./database/{DB_NAME}.db")
# ENGINE = create_engine(f"sqlite:///./database/{DB_NAME}.db", echo=True)


MYSQL_CONNECTION_STRING = (
    "mysql://airflow_user:airflow_pass@mysql:3306/airflow_db"
    if ENV == "PROD"
    else "mysql+mysqlconnector://airflow_user:airflow_pass@localhost/airflow_db"
)
# MYSQL_CONNECTION_STRING = "mysql://airflow_user:airflow_pass@mysql:3306/airflow_db"
logger.info(f"My sql connection string used is:{MYSQL_CONNECTION_STRING}")
print(MYSQL_CONNECTION_STRING)
MYSQL_ENGINE = create_engine(MYSQL_CONNECTION_STRING)
ENGINE = MYSQL_ENGINE

DB_ENGINE_MAP = {DBType.SQLITE.value: None, DBType.MYSQL.value: MYSQL_ENGINE}

import pandas as pd
from sqlalchemy import create_engine,text

# ✅ Use pymysql as driver
MYSQL_CONNECTION_STRING = "mysql+pymysql://airflow_user:airflow_pass@mysql/airflow_db"

MYSQL_POOL_ENGINE = create_engine(
    MYSQL_CONNECTION_STRING,
    pool_size=5,             # Number of persistent connections
    max_overflow=10,         # Extra connections above pool_size
    pool_recycle=1800,       # Recycle after 30 minutes
    pool_pre_ping=True       # Ping before using (avoids broken pipe)
)

def create_table_if_not_exists(df: pd.DataFrame, table_name: str, engine=MYSQL_POOL_ENGINE):
    dtype_map = {
        "int64": "INT",
        "float64": "FLOAT",
        "object": "VARCHAR(255)",
        "datetime64[ns]": "DATETIME",
        "bool": "BOOLEAN"
    }

    columns = []
    for col, dtype in df.dtypes.items():
        sql_type = dtype_map.get(str(dtype), "VARCHAR(255)")
        columns.append(f"`{col}` {sql_type}")

    ddl = f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n  {', '.join(columns)}\n);"

    with engine.connect() as conn:
        conn.execute(text(ddl))
        print(f"✅ Ensured table `{table_name}` exists.")


def save_df_to_db(df: pd.DataFrame, table_name: str, engine=MYSQL_POOL_ENGINE, replace=False):
    if df.empty:
        print(f"⚠️ DataFrame is empty, skipping insert to {table_name}")
        return

    create_table_if_not_exists(df, table_name, engine)
    columns = list(df.columns)
    col_names = ", ".join(f"`{col}`" for col in columns)
    placeholders = ", ".join(["%s"] * len(columns))  # %s for pymysql
    insert_sql = f"INSERT INTO `{table_name}` ({col_names}) VALUES ({placeholders})"
    data = df.to_records(index=False).tolist()

    raw_conn = engine.raw_connection()  
    try:
        cursor = raw_conn.cursor()
        if replace:
            cursor.execute(f"DELETE FROM `{table_name}`")
        cursor.executemany(insert_sql, data)
        raw_conn.commit()
        print(f"✅ Bulk inserted {len(data)} rows into `{table_name}`.")
    finally:
        cursor.close()
        raw_conn.close()


def drop_existing_tables(engine=MYSQL_POOL_ENGINE):
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

    with engine.connect() as conn:
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


if __name__ == "__main__":
    df = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"]
})

    save_df_to_db(df, "my_table", replace=True)
