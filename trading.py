import csv
import math
import matplotlib.pyplot as plt
import sys
from .signals import *
from .utilities import *


'''
    To do : 
    1. Refactor Oscillator, use the buy and sell methods
    2. Refactor Buy and Sell
    3. Add reset function after trde
    4. Standardize documentation
    5. Change logs from array to dictionary
'''

class Trader(object):
    def __init__(self, trade_volume = 0, balance = 0, stop_loss_percentage = 0.0, take_gain_percentage = 0.0):
        # Array of buy, sell and hold signals
        self.signals = None
        # Iteration Counter
        self.time_pointer = 0
        # How much cash the user has on hand
        self.balance = balance
        # How much of the current cash on hand to be used
        self.trade_volume = trade_volume
        # How many stocks are on hand
        self.held_amount = 0 
        # Price when either buying stock or shorting stock
        self.entry_price = 0
        # Percent loss threshold before trades are exited
        self.stop_loss_percentage = 0
        # Percent gain threshold before trades are exited
        self.take_gain_percentage = 0

        self.log = []

        self.win_count = 0
        self.current_price = 0
        self.loss_count = 0
    def add_stock_data(self,file_name,source = 0):
        self.data = parse_csv(file_name)[source]

    # A position is always held, whether short or long
    # - To refactor - 
    # Returns a list containing
    #   Total trade history
    #   Number of successes
    #   Number of failures
    #   Total number of trades executed
    def oscillator(signals, data, start_balance=100000):
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
    # Signals [1 for buy, -1 for sell and 0 for hold]
    # can_short determines whether or
    def execute_trades(self):
        self.time_pointer = len(self.data) - len(self.signals)
        for x in range(len(self.data) - len(self.signals),len(self.signals) - 1):
            if self.signals[x] == 1:
                self.buy()
            elif self.signals[x] == -1:
                self.sell()
            else:
                self.hold()
				
    # All is true on Stop Loss or Take Gain Exits
    def buy(self, all = False, is_stop_loss = False):
        if self.time_pointer >= len(self.data):
            print('EOF')
        else:
            current_price = self.data[self.time_pointer]
            if all:
                requested_amount = self.held_amount
            else:
                requested_amount = current_price/(self.trade_volume * self.balance)
            trade_type = 'LONG ENTER'
            if self.held_amount > 0:
                new_balance = self.balance - requested_amount * current_price
                self.entry_price = ((self.held_amount * self.entry_price) + (requested_amount * current_price))/(self.held_amount + requested_amount)

            elif self.held_amount < 0:
                if is_stop_loss:    
                    trade_type = 'SL SHORT EXIT'
                else:
                    trade_type = 'SHORT EXIT'

                if current_price < self.entry_price:
                    self.win_count = self.win_count + 1
                elif current_price > self.entry_price:
                    self.loss_count = self.loss_count + 1

                new_balance = self.balance + (self.entry_price - current_price) * requested_amount

            else:
                new_balance = self.balance - requested_amount * current_price
                self.entry_price = current_price
            log_entry = {
                'period': self.time_pointer,
                'type': trade_type,
                'volume': requested_amount,
                'current_price': current_price,
                'entry_price': self.entry_price,
                'starting_balance': self.balance,
                'end_balance': new_balance,
                'total_equity': self.balance + self.held_amount * current_price,
                'held': self.held_amount,
                'win_count': self.win_count,
                'loss_count': self.loss_count
	        }
            self.log.append(log_entry)
            self.balance = new_balance
            self.held_amount = self.held_amount + requested_amount
            self.time_pointer = self.time_pointer + 1

    # All is only true on Stop Loss Exits

    def sell(self, all = False, is_stop_loss = False):
        if self.time_pointer >= len(self.data):
            print('EOF')
        else:
            current_price = self.data[self.time_pointer]
            requested_amount = current_price/(self.trade_volume * self.balance)
            trade_type = 'SHORT ENTER'
            new_balance = self.balance

            if self.held_amount > 0:
                if is_stop_loss:    
                    trade_type = 'SL LONG EXIT'
                else:
                    trade_type = 'LONG EXIT'
                if all:
                    requested_amount = self.held_amount
                new_balance = self.balance + requested_amount * current_price
                self.balance = new_balance

                if current_price > self.entry_price:
                    self.win_count = self.win_count + 1
                elif current_price < self.entry_price:
                    self.loss_count = self.loss_count + 1

            elif self.held_amount < 0:
                self.entry_price = ((-self.held_amount) * self.entry_price + requested_amount * current_price)/(-self.held_amount + requested_amount)
            else:
                self.entry_price = current_price
            log_entry = {
                'period': self.time_pointer,
                'type': trade_type,
                'volume': requested_amount,
                'current_price': current_price,
                'entry_price': self.entry_price,
                'starting_balance': self.balance,
                'end_balance': new_balance,
                'total_equity': self.balance + self.held_amount * current_price,
                'held': self.held_amount,
                'win_count': self.win_count,
                'loss_count': self.loss_count
	        }
            self.log.append(log_entry)
            self.held_amount = self.held_amount - requested_amount
            self.time_pointer = self.time_pointer + 1

    def hold(self):
        current_price = self.data[self.time_pointer]
        log_entry = {
            'period': self.time_pointer,
            'type': 'HOLD',
            'volume': 0,
            'current_price': self.data[self.time_pointer],
            'entry_price': self.entry_price,
            'starting_balance': self.balance,
            'end_balance': self.balance,
            'total_equity': self.balance + self.held_amount * current_price,
            'held': self.held_amount,
            'win_count': self.win_count,
            'loss_count': self.loss_count
        }
        self.log.append(log_entry)
        self.time_pointer = self.time_pointer + 1

# Beta Section
    # Assumes that TP 2 > TP 1 
    def execute_hold_and_wait(self, dictionary, data, available_balance):
        # Determine how much stocks will be on hand - (Balance * Pct of Available Cash) / Entry Price
        self.held_amount = (self.balance * dictionary['Pct of Available Cash'])/dictionary['Entry Price']
        self.balance = self.balance * (1-dictionary['Pct of Available Cash'])
        self.entry_price = dictionary['Entry Price']
        on_hand = self.held_amount
        tp1_taken = False
        tp2_taken = False
        self.time_pointer = 0
        for x in range(1,len(data)):
            i = self.time_pointer 
            data = self.data
            # Stop Loss Section
            if self.held_amount != 0:
                if((data[i] < dictionary['Stop Loss']) and dictionary['Type of Trade'] == 'LONG'):
                    self.sell(True,True)
                elif((data[i] > dictionary['Stop Loss']) and dictionary['Type of Trade'] == 'SHORT'):
                    self.buy(True,True)
                else:
                    # Take Profit Section
                    
                    # Temporarily changes held amount to the percentage of it according to split then sells all
                    # Returns the new value of held amount after
                    if(data[i] > dictionary['Target Price 1']) and (dictionary['Type of Trade'] == 'LONG') and (tp1_taken == False):
                        self.held_amount = self.held_amount * (dictionary['TP1 vs TP2 Split'])
                        tp1_taken = True
                        self.sell(all)
                        self.held_amount = on_hand - self.held_amount
                    if(data[i] > dictionary['Target Price 2']) and (dictionary['Type of Trade'] == 'LONG') and (tp2_taken == False):
                        tp2_taken = True
                        self.sell(all)
                        self.held_amount = on_hand - self.held_amount
                    else:
                        self.hold()
            else:
                self.hold()
