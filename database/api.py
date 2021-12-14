import conncection.py

db_api = DataBaseAPI(engine=engine)

# Create a new table to accomodate the data
statements = [
    "DROP TABLE IF EXISTS {};".format(TABLE_NAME),
    
    "CREATE TABLE {} ("
        "_date date,"
        "ticker VARCHAR(10)," 
        "ret DOUBLE,"
        "sector VARCHAR(20),"
        "PRIMARY KEY (_date,ticker));".format(TABLE_NAME) 
    ]

for s in statements:
    db_api.engine.execute(s)

# Store the frame
db_api.save_data_to_table(data=data, table_name=TABLE_NAME, **{"if_exists": "append", "index": False})

# Time-series request
df = db_api.timeseries_query(tab_name=TABLE_NAME, tickers=["AAPL", "TSLA"], 
                             dtype="ret", start_date="2019-01-01", end_date="2020-08-31")

print(df.head())