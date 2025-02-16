# Import libraries
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import os
from peewee import *

# Create the Data folder if it doesn't exist
os.makedirs('Data', exist_ok=True)

# Initialize the database globally
db = None

class Candlestick(Model):
    timestamp = DateTimeField(primary_key=True)
    date = DateField(constraints=[SQL("DEFAULT (DATE(timestamp))")])  # SQL - Extracts date from timestamp
    time = TimeField(constraints=[SQL("DEFAULT (TIME(timestamp))")])  # SQL - Extracts time from timestamp
    open = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()
    volume = IntegerField()

    class Meta:
        database = db  # This will be assigned dynamically

def createDb(symbol, timeframe):
    global db
    db = SqliteDatabase(f'Data/{symbol}db.db')

    # Dynamically set the table name
    class Meta:
        database = db
        table_name = f"{symbol}_{timeframe}"

    Candlestick._meta.database = db  # Assign database to model
    Candlestick._meta.table_name = f"{symbol}_{timeframe}"  # Assign table name

    db.connect()
    db.create_tables([Candlestick], safe=True)

    print(f"---{symbol} DATABASE CREATED---")
    return db

def cndlExists(timestamp):

    return Candlestick.select().where(Candlestick.timestamp==timestamp).exists()

def recordDataFrame(df):

    iRec = df.shape[0] # Num records recieved
    iDup = 0 # Num duplicates found

    bLoadingBar = (iRec>=1000)
    if bLoadingBar: print(f"---DATAFRAME_LOADING [", end="")

    for _, row in df.iterrows():

        if (bLoadingBar) and (_%1000==0): print("=", end="", flush=True)

        timestamp = row['timestamp'].to_pydatetime()

        if not (cndlExists(timestamp)):

            Candlestick.create(
                timestamp=timestamp,
                date=timestamp.date(),  # Extract date from timestamp
                time=timestamp.time(),  # Extract time from timestamp
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
                volume=row['volume']
            )

        else: iDup += 1

    print("]---")

    if (iDup!=0):
        print(f"---DUPLICATES FOUND [{iDup}] | RECORDS RECIEVED [{iRec}]")
    else: print(f"---RECORDS_ADDED: [{iRec}]---")


if __name__ == "__main__":
    symbol = "CADUSD"
    timeframe = mt5.TIMEFRAME_M15
    createDb(symbol, timeframe)
