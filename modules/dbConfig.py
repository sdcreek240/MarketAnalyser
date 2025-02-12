# Import functions for MT5 connection
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime as dt
import sqlite3
from peewee import * # ORM

# Initialize connection to mt5 servers
import os
# from mt5Class import *

# Create the Data folder if it doesn't exist
os.makedirs('Data', exist_ok=True)

def createDb(symbol, timeframe):

    # Define the database file
    db = SqliteDatabase(f'Data/{symbol}db.db')

    # Define the Candlestick model (table)
    class Candlestick(Model):

        symbol = CharField()  # symbol="EURUSD"
        timeframe = CharField()  # timeframeStr=timeframeMap.get(timeframe, "M15")"M1"
        timestamp = DateTimeField()  # Timestamp of the candlestick
        open = FloatField()  # Open price
        high = FloatField()  # High price
        low = FloatField()  # Low price
        close = FloatField()  # Close price
        volume = IntegerField()  # Volume

        class Meta:
            database = db
            table_name = symbol

    db.connect()
    # If Candlestick table does not exist, create one according to Candlestick model
    db.create_tables([Candlestick])

    print(f"---{symbol} DATABASE CREATED---")

if __name__=="__main__":
    
    # Define symbol details
    symbol = "CADUSD"
    timeframe = mt5.TIMEFRAME_M15

    createDb(symbol, timeframe)