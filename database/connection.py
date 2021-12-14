# Reiterate the imports and settings for consistency
import pandas as pd
import sqlalchemy
import pymysql


# A new table we'll be working with
TABLE_NAME = "return_data"

# Database credentials, which we created before
SQL_USERNAME = "tutorial_user"
SQL_PASSWORD = "password"
SQL_DB_NAME = "tutorial_db"

# Connection settings
SQL_DIALECT = "mysql"  # we are using MySQL
SQL_DRIVER = "pymysql"  # pymsql provides an interface between MySQL and Python

# The 
SQL_URL = "{}+{}://{}:{}@localhost:3306/{}".format(SQL_DIALECT,
                                                   SQL_DRIVER,
                                                   SQL_USERNAME,
                                                   SQL_PASSWORD,
                                                   SQL_DB_NAME)

# Connect to the DB
engine = sqlalchemy.create_engine(SQL_URL, echo=False)


class DataBaseAPI:


    def __init__(self, engine):

        self.engine = engine

    def save_data_to_table(self, data, table_name, **to_sql_kwargs):
 
        data.to_sql(con=self.engine, name=table_name, **to_sql_kwargs)

    def get_data(self, query, **read_sql_kwargs):

        return pd.read_sql(sql=query, con=self.engine, **read_sql_kwargs)

    def timeseries_query(self, tab_name, tickers, dtype, start_date,
                         end_date):

 
        # Construct a string of tickers for 'IN' clause
        tickers_str = "(" + ",".join(["'" + x + "'" for x in tickers]) + ")"

        # Construct the query
        q = "SELECT _date, ticker, {dtype} FROM {tab_name} WHERE " \
            "_date BETWEEN {start} AND {end} AND " \
            "ticker IN {tickers};".format_map({
                "dtype": dtype, "tab_name": tab_name,
                "start":
                    "'" + pd.Timestamp(start_date).strftime("%Y-%m-%d") + "'",
                "end":
                    "'" + pd.Timestamp(end_date).strftime("%Y-%m-%d") + "'",
                "tickers": tickers_str
                }
            )
        out = self.get_data(q)

        return out
    
    