import tkinter as tk
from tkinter import ttk
import pyquant
import csv
from datetime import datetime
import matplotlib
from tkinter import StringVar
from tkinter import simpledialog
import tkinter.messagebox
import tkinter.filedialog       
matplotlib.use('TkAgg')     
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import gridspec

''' 
Definitions
    Epochs are how data is divided into segments here; first 15 bars, third 1/4, etc.

    Logs are kept by both the autotrader and the manual trader. Each entry is in the following format
        [
            Bar Number
            Action
            Price
            Volume
            Starting Balance
            Ending Balance
            Total Equity
            Win Count
            Loss Count
        ]

|  ||
|| |_

'''

'''
To do
2. Rebind Functions to overarching class
3. Chartscroll - both
4. Migrate functions to toolbar - both
5. Configure data source changing - main
'''

class Main:
    def __init__(self, master):
        self.master = master

        ''' Menu '''
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Open CSV")
        fileMenu.add_command(label="Refresh")
        fileMenu.add_command(label="Close", command=quit)
        tradingMenu = tk.Menu(menubar)
        tradingMenu.add_command(label="Open Manual Trading Simulator")
        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="Trading", menu=tradingMenu)

        ''' Notebook '''
        self.notebook = ttk.Notebook(master)
        Frame1 = ttk.Frame(self.notebook)
        MainWindow(Frame1)
        Frame2 = ttk.Frame(self.notebook)
        MainWindow(Frame2)
        self.notebook.add(Frame1, text = "Tab 1")
        self.notebook.add(Frame2, text = "Tab 1")
        self.notebook.pack()


class MainWindow(ttk.Frame):
    def __init__(self, master):
        self.master = master
        self.master.grid_rowconfigure(0,weight=1)
        self.master.grid_columnconfigure(0,weight=1)
        self.frame = ttk.Frame(master,width = 100,height=100)
        self.initialize_widgets()
        self.master_strategy = pyquant.strategy()
        self.trading_data = None
        self.file_name = None
    '''Initialize all widgets here'''
    def initialize_widgets(self):
        '''Grid'''
        self.frame.grid(sticky='NW')
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ''' Labels '''
        self.file_name = tk.Label(self.frame,text = '--- No Data Loaded ---')
        self.file_name.grid(row = 1,column = 1, sticky='NE')
        self.file_name.grid_columnconfigure(0, weight=1)
        self.file_name.grid_rowconfigure(0, weight=1)
        self.trading_data_column_label = tk.Label(self.frame,text='Data Used')
        self.trading_data_column_label.grid(row=4, column=1)
        self.trading_data_column_label.grid_columnconfigure(0, weight=1)
        self.trading_data_column_label.grid_rowconfigure(0, weight=1)
        self.split_count_label = tk.Label(self.frame,text = 'Number of Epochs')
        self.split_count_label.grid(row = 4, column = 2)
        self.split_count_label.grid_columnconfigure(0, weight=1)
        self.split_count_label.grid_rowconfigure(0, weight=1)

        ''' Option Menu '''
        self.data_source = StringVar(self.frame)
        self.data_source.set('OHLC Average')
        self.stock_data_source = tk.OptionMenu(self.frame, self.data_source, 'OHLC Average', 'Opening','High','Low','Close','Adjusted Close','Volume')
        self.stock_data_source_options = {
            'OHLC Average' : 0,
            'Opening': 1,
            'High':2,
            'Low':3,
            'Close':4,
            'Adjusted Close':5,
            'Volume':6
        }
        self.stock_data_source.grid(row = 5, column = 1)

        ''' Entries '''
        self.split_count = tk.Entry(self.frame)
        self.split_count.grid(row = 5, column = 2)


        ''' Buttons '''
        self.open_new_trade_strategy_window_button = tk.Button(self.frame,text='Open Trading Rules',command=self.open_trading_strategies)
        self.open_new_trade_strategy_window_button.grid(row=3,column=3,sticky ='NEWS')
        self.next_epoch_button = tk.Button(self.frame,text = 'Next epoch >>', command = lambda: self.display_stock_data(epoch = (self.current_epoch + 1), epoch_count = int(self.split_count.get())) if (self.current_epoch + 1)<len(self.trading_data) else print('End of '))
        self.next_epoch_button.grid(row=3,column =2,sticky ='NEWS')
        self.next_epoch_button = tk.Button(self.frame,text = '<< Previous epoch', command = lambda: self.display_stock_data(epoch = (self.current_epoch - 1), epoch_count = int(self.split_count.get())) if (self.current_epoch -1) > -1 else print('End'))
        self.next_epoch_button.grid(row=3,column =1,sticky ='NEWS')
        self.refresh_chart = tk.Button(self.frame,text = 'refresh_charts', command = self.refresh)
        self.refresh_chart.grid(row = 5, column = 3)

        ### Demo
        #self.demo_button = tk.Button(text = 'Demo Button')
        #self.demo_button.grid(row = 5, column = 3)
        ###
        ''' Plot '''
        self.figure = Figure(figsize=(13,5))
        ''' Graph Creation and Grid Arrangement using Gridspec'''
        self.chart_grids = gridspec.GridSpec(2,2)
        
        self.stock_data_graph = self.figure.add_subplot(self.chart_grids[0,:])
        self.stock_data_graph.set_xlabel('Time Periods')
        self.stock_data_graph.set_ylabel('Price')
        
        self.profit_graph = self.figure.add_subplot(self.chart_grids[1,1])
        self.profit_graph.set_xlabel('Time Period')
        self.profit_graph.set_ylabel('Total Equity')
        
        self.win_loss_graph = self.figure.add_subplot(self.chart_grids[1,0])
        self.win_loss_graph.set_xlabel('Time Period')
        self.win_loss_graph.set_ylabel('Profit/Loss')

        ''' Integraph spacing'''
        self.figure.subplots_adjust(top=0.92, bottom=0.18, left=0.15, right=0.95, hspace=0.45,
                    wspace=0.55)
        ''' Canvas attachment '''
        self.canvas = FigureCanvasTkAgg(self.figure,master=self.frame)
        self.canvas.show()
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=2,column = 1,columnspan = 3, sticky ='NW')
        self.plot_widget.grid_rowconfigure(0,weight=1)
        self.plot_widget.grid_columnconfigure(0,weight=1)


    def segment_data(self,column,count):
        return pyquant.split_bars_fraction(self.trading_data[column],count)

    def refresh(self):
        self.display_stock_data(epoch = 0, epoch_count = int(self.split_count.get()))
        self.current_epoch = 0    

    def csv_export(self):
        self.log = self.master_strategy.log
        with open('Auto-Trade-Log.csv','w') as fp:
            writer = csv.writer(fp, delimiter=',')
            headers = [[
            "Period",
            "Action",
            "Volume",
            "Current Price",
            "Entry Price",
            "Starting Balance",
            "Ending Balance",
            "Total Equity",
            "Win Count",
            "Loss Count"]]
            writer.writerows(headers) 
            writer.writerows(self.log)

    def on_column_selection_change(self, event):
        None

    ''' Move Epoch tells the '''
    def move_epoch(self,epoch_index):
        self.current_epoch = epoch_index
        self.display_stock_data(self.current_epoch)
        print('Changed Epoch to '+self.current_epoch)

    def display_stock_data(self, epoch = 0,epoch_count = 1):
        self.stock_data_graph.clear()
        self.current_epoch = epoch
        data_to_plot = self.segment_data(self.stock_data_source_options[self.data_source.get()],epoch_count)
        self.stock_data_graph.plot([ x for x in range(0,len(data_to_plot[epoch]))],data_to_plot[epoch])
        self.figure.canvas.draw()
        '''Opens a trading strategies window to create strategies to pass to the main window'''

    def display_equity(self,epoch = 0):
        self.profit_graph.plot([ x for x in range(0,len(self.trading_data[epoch]))],self.trading_data[epoch])
        self.figure.canvas.draw()
        print('Redrew Profit Movement Data')

    def open_trading_strategies(self):
        self.trading_strategies_window = tk.Toplevel(self.master)
        self.trading_strategies_app = TradingStrategies(self.trading_strategies_window)
    
    def  open_manual_trading(self):
        if self.trading_data != None or self.file_name != None:
            self.manual_trading_window = tk.Toplevel(self.master)
            self.manual_trading_app = ManualTrading(self.manual_trading_window,self.trading_data[1],self.file_name)
        else:
            tk.messagebox.showinfo("Error","Please Upload Trading Data")

    def pass_file(self):
        return tk.filedialog.askopenfile(mode="r")

    def on_upload_csv_button_click(self): 
        csv = self.pass_file()
        self.trading_data = pyquant.parse_csv(csv.name)
        self.file_name = csv.name
        print(str(csv.name) + " Loaded")
        self.master_strategy.add_stock_data(pyquant.parse_csv(csv.name))
        self.display_stock_data()
        # self.file_name['text']= str(csv.name)

class TradingStrategies:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.initialize_widgets()
    def initialize_widgets(self):
        ''' Repeating Labels '''
        self.indicators_label = []
        self.row_count = 1
        self.indicators_label.append(tk.Label(self.frame,text = 'Rule 1'))
        self.indicators_label[0].grid(row = self.row_count,column = 1)
        ''' Repeating Dropdown Menus'''
        self.indicators_menus = []
        self.indicators_menus_items = []
        self.indicators_menus_items.append(StringVar(self.master))
        self.indicators_menus_items[self.row_count - 1].set('Select Indicator')
        self.indicators_menus.append(tk.OptionMenu(self.frame,self.indicators_menus_items[self.row_count-1],'Aroon','Vortex','MACD','RSI'))
        self.indicators_menus[self.row_count - 1].grid(row = self.row_count, column = 2)

        '''Buttons'''
        self.add_trading_rule_button = tk.Button(self.frame,text = 'Add New Row',command = self.add_indicator_rules)
        self.add_trading_rule_button.grid(row = self.row_count+1,column = 1)
        self.frame.grid()
    def add_indicator_rules(self):
        self.row_count = self.row_count + 1
        ''' Additional Label '''
        self.indicators_label.append(tk.Label(self.frame,text = 'Rule '+str(self.row_count)))
        self.indicators_label[-1].grid(column = 1, row = self.row_count)
        self.add_trading_rule_button.grid(row = self.row_count + 1)

        ''' Additional Rules Menu '''
        self.indicators_menus_items.append(StringVar(self.master))
        self.indicators_menus_items[self.row_count - 1].set('Select Indicator')
        self.indicators_menus.append(tk.OptionMenu(self.frame,self.indicators_menus_items[self.row_count-1],'Aroon','Vortex','MACD','RSI'))
        self.indicators_menus[self.row_count - 1].grid(row = self.row_count, column = 2)

class ManualTrading:
    """docstring for ManualTrading"""
    def __init__(self, master,data,file_name):
        self.master = master
        self.main_frame = self.master
        self.time_pointer = 0
        self.held_amount = 0
        self.win_count = 0
        self.balance = 0
        self.loss_count = 0
        self.entry_price = 0
        self.log = []
        self.insert_data(data,file_name)
        self.initialize_widgets()
        self.set_initial_balance()

    def initialize_widgets(self):
        self.master.grid_rowconfigure(0, weight = 1)
        self.master.grid_columnconfigure(0, weight = 1)

        menubar = tk.Menu(self.main_frame)
        self.master.config(menu=menubar)
        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Save Logs as CSV", command=self.csv_export)
        fileMenu.add_command(label="Close", command=quit)
        
        menubar.add_cascade(label="File", menu=fileMenu)

        """ Plots """
        self.figure = Figure(figsize=(6,4))
        self.chart_grids = gridspec.GridSpec(2,2)
        ''' Subplot Creation '''
        
        self.stock_data_graph = self.figure.add_subplot(self.chart_grids[0,:])
        self.stock_data_graph.set_xlabel('Time Periods')
        self.stock_data_graph.set_ylabel('Price')

        self.equity_graph = self.figure.add_subplot(self.chart_grids[1,1])
        self.equity_graph.set_xlabel('Time Period')
        self.equity_graph.set_ylabel('Total Equity')
        
        self.win_loss_graph = self.figure.add_subplot(self.chart_grids[1,0])
        self.win_loss_graph.set_xlabel('Time Period')
        self.win_loss_graph.set_ylabel('Profit/Loss')

        ''' Integraph spacing'''
        self.figure.subplots_adjust(top=0.92, bottom=0.18, left=0.15, right=0.95, hspace=0.45,
                    wspace=0.55)
        ''' Canvas attachment '''
        self.canvas = FigureCanvasTkAgg(self.figure,master=self.main_frame)
        self.canvas.show()
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=1,column = 1,columnspan = 3, sticky ='NW')
        self.plot_widget.grid_rowconfigure(0,weight=1)
        self.plot_widget.grid_columnconfigure(0,weight=1)


        """ Buttons """
        self.buy_button = tk.Button(self.main_frame, text = "Buy", command = self.buy)
        self.buy_button.grid(row = 2, column = 1)
        self.sell_button = tk.Button(self.main_frame, text = "Sell", command = self.sell)
        self.sell_button.grid(row = 2, column = 2)
        self.hold_button = tk.Button(self.main_frame, text = "Hold")
        self.hold_button.grid(row = 2, column = 3)
        self.exit_button = tk.Button(self.main_frame, text = "Close",command=self.before_close)
        self.exit_button.grid(row = 4, column = 3)

        """ Entries """
        self.buy_or_sell_amount_entry = tk.Entry(self.main_frame)
        self.buy_or_sell_amount_entry.grid(row = 4, column = 1)
        
        """ Labels """
        self.symbol_name_label = tk.Label(self.main_frame, text = self.file_name)
        self.symbol_name_label.grid(row = 0, column = 1)
        self.current_price_label = tk.Label(self.main_frame, text = "Current Price "+ str(self.data[self.time_pointer]))
        self.current_price_label.grid(row = 0, column = 2)
        self.current_bar_label = tk.Label(self.main_frame, text = "Current Bar "+str(self.time_pointer))
        self.current_bar_label.grid(row = 0, column = 3)
        self.total_equity_label = tk.Label(self.main_frame, text = "Total Equity: $"+ str(self.balance+self.data[self.time_pointer*self.held_amount]))
        self.total_equity_label.grid(row = 3, column = 1)
        self.shares_held_label = tk.Label(self.main_frame, text = "shares Held: "+str(self.held_amount*self.data[self.time_pointer]+self.balance))
        self.shares_held_label.grid(row = 3, column = 2)
        self.wins_losses_ratio_label = tk.Label(self.main_frame, text = "Profit / Loss Ratio")
        self.wins_losses_ratio_label.grid(row = 3, column = 3)
        self.balance_label = tk.Label(self.main_frame, text = "Current Balance: "+str(self.balance))
        self.balance_label.grid(row=5,column=1)

    def insert_data(self,data,file_name):
        self.data = data
        self.file_name = file_name

    def set_initial_balance(self):
        accepted = False
        value = None
        while accepted == False:
            value = tkinter.simpledialog.askinteger("Initialization","Enter the initial balance:")
            if value < self.data[0]:
                tkinter.messagebox.showinfo("Error","Starting balance cannot be lower than the first bar. Please enter a value higher than: " + str(self.data[0]))
            else:
                accepted = True
        self.balance = value
        self.total_equity_label['text'] = str(self.balance+self.data[self.time_pointer]*self.held_amount)
        self.update_labels()
    def before_close(self):
        if tkinter.messagebox.askyesno("Save Data?","Save?") == 'yes':
            self.master.destroy()
        else:
            self.csv_export()
            self.master.destroy()

    def buy(self):
        if self.time_pointer >= len(self.data):
            tkinter.messagebox.showinfo("End of Data")
        else:
            requested_amount = int(self.buy_or_sell_amount_entry.get())
            current_price = self.data[self.time_pointer]
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
            
            self.update_labels()
            self.refresh_charts()

    def sell(self):
        if self.time_pointer >= len(self.data):
            tkinter.messagebox.showinfo("End of Data")
        else:
            requested_amount = int(self.buy_or_sell_amount_entry.get())
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

            self.update_labels()
            self.refresh_charts()

    def hold(self):
        self.log.append([self.time_pointer, 'HOLD', 0 ,self.data[self.time_pointer], self.entry_price, self.balance, self.balance, self.balance + self.held_amount * current_price, self.win_count, self.loss_count])
        self.time_pointer = self.time_pointer + 1
        self.update_labels()
        self.refresh_charts()

    def csv_export(self):
        with open('Manual-Trade-Log.csv','w') as fp:
            writer = csv.writer(fp, delimiter=',')
            headers = [[
            "Period",
            "Action",
            "Volume",
            "Current Price",
            "Entry Price",
            "Starting Balance",
            "Ending Balance",
            "Total Equity",
            "Win Count",
            "Loss Count"]]
            writer.writerows(headers) 
            writer.writerows(self.log)

    def test_next(self):
        self.time_pointer = self.time_pointer + 1
        self.refresh_charts()

    def update_labels(self):
        self.current_price_label.configure(text = "Current Price "+ str(self.data[self.time_pointer]))
        self.current_bar_label.configure(text = "Current Bar "+str(self.time_pointer))
        self.balance_label.configure(text="Current Balance: "+str(self.balance))
        if self.held_amount > 0:
            self.total_equity_label.configure(text = "Total Equity: $"+ str(self.balance + self.data[self.time_pointer]*self.held_amount))
        else:
            self.total_equity_label.configure(text = "Total Equity: $"+ str(self.balance))

        self.shares_held_label.configure(text = "Units Held: "+str(self.held_amount))
        if self.loss_count > 0:
            self.wins_losses_ratio_label.configure(text = "Profit / Loss Ratio: "+str(self.win_count/self.loss_count))
        else:
            self.wins_losses_ratio_label.configure(text = "Profit / Loss Ratio: Inf")

        map(lambda x: print(str(x)), self.log)

    def refresh_charts(self):
        self.stock_data_graph.clear()
        self.win_loss_graph.clear()
        self.equity_graph.clear()

        x_range = [ x for x in range(0,self.time_pointer)]
        success_array = [ self.log[x][7] for x in range(0,self.time_pointer)]
        fail_array = [ self.log[x][8] for x in range(0,self.time_pointer)]

        self.stock_data_graph.plot(x_range,self.data[:self.time_pointer])
        self.win_loss_graph.plot(x_range, success_array, label = 'Win')
        self.win_loss_graph.plot(x_range,fail_array, label = 'Loss')
        self.figure.canvas.draw()

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
if __name__ == '__main__':
    main()