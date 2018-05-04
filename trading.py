import csv
import math
import matplotlib.pyplot as plt
from .signals import *
from .indicators import *
from .utilities import *

class strategy(object):
    def __init__(self):
        self.signals = None
        # Iteration Counter
        self.time_pointer = 0
        # How much cash the user has on hand
        self.balance = 0
        # How much of the current cash on hand to be used
        self.trade_volume = 0
        # How many stocks are on hand
        self.held_amount = 0 
        self.stop_loss_percentage = 0
        self.stop_loss_percentage
        self.log = []
    def add_stock_data(self,data):
        self.data = data
    def add_indicator_aroon(self, time_length, threshold_a, threshold_b):
        self.signals.append(aroon_signal(self.data, time_length, threshold_a, threshold_b))

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
    def execute_trades(self):
#        current_price = self.data[self.time_pointer]
        for x in range(0,len(self.data)):
#            if ((current_price < self.entry_price) * (1 - self.stop_loss_percentage) and (self.holding > 0)) or ((current_price > self.entry_price * (1 + self.stop_loss_percentage)) and (self.holding < 0)):
            if signals[x] == 1:
                self.buy()
            elif signals[x] == 0:
                self.sell()
            else:
                self.hold()


    def buy(self):
        if self.time_pointer >= len(self.data):
            print('EOF')
        else:
            current_price = self.data[self.time_pointer]
            requested_amount = current_price/(self.trade_volume * self.balance)
            trade_type = 'LONG ENTRY'

            if self.held_amount > 0:
                new_balance = self.balance - requested_amount * current_price
                self.entry_price = ((self.held_amount * self.entry_price) + (requested_amount * current_price))/(self.held_amount + requested_amount)

            elif self.held_amount < 0:
                trade_type = 'SHORT EXIT'

                if current_price < self.entry_price:
                    self.win_count = self.win_count + 1
                elif current_price > self.entry_price:
                    self.loss_count = self.loss_count + 1

                new_balance = self.balance + (self.entry_price - current_price) * requested_amount

            else:
                new_balance = self.balance - requested_amount * current_price
                self.entry_price = current_price
            
            self.log.append([self.time_pointer,trade_type, requested_amount,current_price, self.entry_price, self.balance, new_balance, self.balance + self.held_amount * current_price, self.win_count, self.loss_count])
            self.balance = new_balance
            self.held_amount = self.held_amount + requested_amount
            self.time_pointer = self.time_pointer + 1


    def sell(self):
        if self.time_pointer >= len(self.data):
            print('EOF')
        else:
            requested_amount = current_price/(self.trade_volume * self.balance)
            current_price = self.data[self.time_pointer]
            trade_type = 'SHORT ENTER'
            new_balance = self.balance

            if self.held_amount > 0:
                trade_type = 'LONG EXIT'
                new_balance = self.balance + requested_amount * current_price
                self.balance = new_balance

                if current_price < self.entry_price:
                    self.win_count = self.win_count + 1
                elif current_price > self.entry_price:
                    self.loss_count = self.loss_count + 1

            elif self.held_amount < 0:
                self.entry_price = ((-self.held_amount) * self.entry_price + requested_amount * current_price)/(-self.held_amount + requested_amount)
            else:
                self.entry_price = current_price

            self.log.append([self.time_pointer, trade_type, requested_amount,current_price, self.entry_price, self.balance, new_balance, self.balance + self.held_amount * current_price, self.win_count, self.loss_count])
            self.held_amount = self.held_amount - requested_amount
            self.time_pointer = self.time_pointer + 1

    def hold(self):
        self.log.append([self.time_pointer, 'HOLD', 0 ,self.data[self.time_pointer], self.entry_price, self.balance, self.balance, self.balance + self.held_amount * current_price, self.win_count, self.loss_count])
        self.time_pointer = self.time_pointer + 1
