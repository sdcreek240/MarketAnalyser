import os

# Clear terminal output
os.system('cls' if os.name == 'nt' else 'clear')

import MetaTrader5 as mt5

# Define contract details
contract = "EURUSD"
timeframe = mt5.TIMEFRAME_M15

# Create mt5 Object
from modules.mt5Class import *
mt5C = MT5Connector(contract, timeframe)

# Initialise mt5 Connection
mt5C.initialize()

#Create DATABASE
from modules.dbConfig import *
createDb(contract, timeframe)




# Terminate connection
mt5C.terminate()