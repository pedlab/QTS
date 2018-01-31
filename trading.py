import csv
import math
import matplotlib.pyplot as plt
from signals import *
from indicators import *
from utilities import *

# This function continuosly alternates between long and short positions
#
# Note: Execute trades to be deprecated
# Signals are an array of 1's, 0's, and -1's
# Function returns a list containing
#   Total trade history
#   Number of successes
#   Number of failures
#   Total number of trades executed
def oscillating_positions(signals, data, start_balance=100000):
    success = fail = entry_price = holding = 0
    balance = start_balance
    history = []
    total = []
    history.append(balance)
    # Initial values
    if signals[0] == 1:
        holding = int(balance / data[len(data) - len(signals)])
        balance = balance - data[len(data) - len(signals)] * holding
        entry_price = data[len(data) - len(signals)]
        history.append(balance)
    else:
        holding = -(balance / data[len(data) - len(signals)])
        entry_price = data[len(data) - len(signals)]
        history.append(balance)

    # Main trading
    for x in range(len(data) - len(signals) + 1, len(data)):
        volume = (balance / data[x])
        # Buying/Short Exit
        sign = signals[x - (len(data) - len(signals))]
        if sign == 1:
            if holding < 0:
                if entry_price > data[x]:
                    success = success + 1
                elif entry_price < data[x]:
                    fail = fail + 1
                balance = balance - ((entry_price - data[x]) * holding)
                volume = (balance / data[x])
                balance = balance - (data[x] * volume)
                holding = volume
                entry_price = data[x]
                history.append(balance)
            elif holding == 0:
                volume = (balance / data[x])
                balance = balance - (data[x] * volume)
                holding = volume
                entry_price = data[x]
                history.append(balance)
        # Selling /Long exit
        elif sign == -1:
            if holding > 0:
                if entry_price < data[x]:
                    success = success + 1
                elif entry_price > data[x]:
                    fail = fail + 1
                balance = balance + (data[x]) * holding
                volume = (balance / data[x])
                holding = -volume
                entry_price = data[x]
                history.append(balance)
            elif holding == 0:
                volume = (balance / data[x])
                holding = -volume
                entry_price = data[x]
                history.append(balance)
        else:
            history.append(balance)
        if holding > 0:
            total.append(balance + holding * entry_price)
        elif holding <= 0:
            total.append(balance)
    if holding > 0:
        balance = balance + data[-1] * holding
    else:
        balance = balance + (entry_price - data[-1]) * holding
    history.append(balance)
    output = [history, success, fail, total]
    return output

# This function buys and sells according to input signals and can take short positions when a sell signal is reached and there are no held stocks
#
# Trade Volume: Number from 0.0 to 1.0 denoting the percentage to be bought when buying
# relative to how much balance is available. E.g, if 100 shares can be bought, and a trade_volume of 0.5 is used, 50 will be bought
# Sale Volume: Number from 0.0 to 1.0 denoting the percentage to be sold when selling
# relative to how much balance is available. E.g, if 100 shares are on hand and a sell order is given, and a sale_volume of 0.5 is used, 50 will be sold
# Signals [1 for buy, -1 for sell and 0 for hold
# can_short determines whether or
def execute_simulation(signals, data, stop_loss_percentage, take_profit_percentage, buy_percentage, sell_percentage, start_balance=100000):

    # Initialization
    balance = start_balance
    held_volume = 0
    acquisition_price = 0
    successes = 0
    fails = 0
    holding = False
    is_long = False

    # Main Trading Loop
    for x in (0, signals):
        buy_volume = (balance / buy_percentage) * buy_percentage
        sell_volume = held_volume * sell_percentage

        # Stop Loss / Take Profit Section
        if holding == True:
            if held_volume == 0:
                if (data[x] >= acquisition_price * (1+stop_loss_percentage)) or (data[x] <= acquisition_price * (1+take_profit_percentage)):
                    exit_short_position()
            else:
                if (data[x] >= acquisition_price * (1+take_profit_percentage)) or (data[x] <= acquisition_price * (1+stop_loss_percentage)):
                    exit_long_position()


        if signals[x] == 1:
            new_data = enter_long_position(data[x], balance, )

def enter_long_position(price, buy_volume, balance = 0):
        new_balance = balance - (price * buy_volume)
        new_volume = buy_volume
        acquisition_price = price
        return new_balance, new_volume, acquisition_price, True

def enter_short_position(price, buy_volume, balance = 0):
    return None

def exit_short_position(price, aquisition_price, held_volume, is_long_trade, percentage = 1.00):
    return None

def exit_long_position(price, aquisition_price, held_volume, is_long_trade, percentage = 1.00):
    return None
