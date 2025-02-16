import os
import MetaTrader5 as mt5
from modules.mt5Class import *  # ---Create mt5 Object
from modules.dbConfig import *  # ---Create DATABASE
from modules.algo import *      # ---Create algo Object

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

    # Create Database & cursor
    db = createDb(symbol, timeframe)
    cursor = db.cursor()

    df = mt5C.getCandles(3000)

    cleanDb = input("Clean Database Instance [Y/N] (default: N): ").strip().upper() or "N"

    if cleanDb=="Y":

        Candlestick.delete().execute()

    recordDataFrame(df)

    # Create algo Object
    algo = Algo(db)

    algo.runStrat(2)


    mt5C.terminate()
    db.commit()




if __name__=="__main__":

    main(symbol, timeframe)