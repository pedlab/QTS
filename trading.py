import csv
import math
import matplotlib.pyplot as plt
from signals import *
from indicators import *
from utilities import *


# Note: Execute trades to be deprecated
# Signals are an array of 1's, 0's, and -1's
# Function returns a list containing
#   Total trade history
#   Number of successes
#   Number of failures
#   Total number of trades executed
def execute_trades(signals, data, start_balance=100000):
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
        # Long exit
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


# def execute_simulation(signals, data,stop_loss_percentage, take_profit_percentage, start_balance=100000, trade_volume):
#     balance = start_balance
#     held_volume = 0
#     successes = 0
#     fails = 0
#     for x in (0, signals):
#         if signals[x] == 1:
#             new_data = buy(data[x],balance,buy_volume)
# def enter_position(price, buy_volume, is_long_trade, balance = 0):
#     if is_long_trade:
#         new_balance = balance - (price * buy_volume)
#         new_volume = buy_volume
#         acquisition_price = price
#         return new_balance, new_volume, acquisition_price, True
#     else:
#         new_volume = buy_volume
#         acquisition_price = price
#         return new_volume,acquisition_price, False
# def exit_position(price, aquisition_price, held_volume, is_long_trade, percentage = 1.00):
#     if is_long_trade:
#         return None
