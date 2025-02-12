import os
import MetaTrader5 as mt5
from modules.mt5Class import *  # ---Create mt5 Object
from modules.dbConfig import *  # ---Create DATABASE

# Define symbol details
symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_M15

# Main execution
def main(symbol="EURUSD", timeframe=mt5.TIMEFRAME_M15):

    # Clear terminal output
    os.system('cls' if os.name == 'nt' else 'clear')

    print("---MAIN EXECUTING---")

    # Create mt5 Object
    mt5C = MT5Connector(symbol, timeframe)

    # Initialise mt5 Connection
    mt5C.initialize()

    # Create Database
    createDb(symbol, timeframe)

    # Populate Database

    mt5C.terminate()




if __name__=="__main__":

    main(symbol, timeframe)