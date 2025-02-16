# Import libraries
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import os
from peewee import *

class Algo:

    # Define Strategy 1
    def strat1(self):
        
        # Your strategy 1 code here
        pass

    # Define Strategy 2
    def strat2(self):
        
        # Your strategy 2 code here
        pass

    def __init__(self, db):

        self.db = db

        self.strats = {
            1: self.strat1,
            2: self.strat2
        }

    def runStrat(self, strat):
        
        if strat in self.strats:

            print(f"---RUNNING_STRAT: Strat_{strat}---")
            self.strats[strat]()  # Call the function dynamically
        else:
            print(f"--STRAT_NOT_FOUND: Strat_{strat}---")

