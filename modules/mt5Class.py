import sys
import os
import MetaTrader5 as mt5
import pandas as pd

# V1.0
class MT5Connector:

    def __init__(self, symbol="EURUSD", timeframe=mt5.TIMEFRAME_H1):

        self.symbol = symbol

        self.timeframe = timeframe

        self.timeframe_map = {

            mt5.TIMEFRAME_M1: "M1",
            mt5.TIMEFRAME_M5: "M5",
            mt5.TIMEFRAME_M15: "M15",
            mt5.TIMEFRAME_H1: "H1",
            mt5.TIMEFRAME_D1: "D1"
        }

        # Declare member variable for last loaded data frame
        self.df = None

        print("---MT5 DEFAULT VARIABLES CREATED---")

    def initialize(self):

        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'MT5'))

        try:

            from config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER
        except ImportError:

            print("---CONFIG IMPORT FAILURE--- Ensure config.py exists in the MT5 folder")
            return False
        
        if not mt5.initialize(login=MT5_LOGIN, server=MT5_SERVER, password=MT5_PASSWORD):

            print("---MT5 INITIALIZE FAILURE---", mt5.last_error())
            return False
        
        print("---MT5 CONNECTION INITIALIZED---")

        return True

    def terminate(self):

        if mt5.terminal_info() is not None:

            mt5.shutdown()
            print("---MT5 TERMINATED---")
        else:

            print("---MT5 TERMINATION FAILURE---")

    def getCandles(self, n):

        # Get the latest `n` candles
        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, n)

        if rates is None:

            print(f"Failed to fetch candles for {self.symbol}. Error:", mt5.last_error())
            return None

        # Convert to a Pandas DataFrame for easier processing
        cFrame = pd.DataFrame(rates)
        cFrame.drop('real_volume', axis=1, inplace=True)
        cFrame['time'] = pd.to_datetime(cFrame['time'], unit='s')
        cFrame.rename(columns={'time': 'timestamp', 'tick_volume': 'volume'}, inplace=True)
        return cFrame

# Example usage
if __name__ == "__main__":

    mt5C = MT5Connector()

    if mt5C.initialize():

        print("--Load DataFrame")

        print(mt5C.getCandles(50))

        # Do something with MT5
        mt5C.terminate()

