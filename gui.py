import tkinter as tk
import pyquant
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.initialize_widgets()
        self.master_strategy = pyquant.strategy()
    '''Initialize all widgets here'''
    def initialize_widgets(self):
        self.upload_data_button = tk.Button(self.frame,text='Open CSV',command=self.on_upload_csv_button_click)
        self.upload_data_button.grid(row=2,column=1)
        self.open_new_trade_strategy_window_button = tk.Button(self.frame,text='Open Trading Strategies',command=self.open_trading_strategies)
        self.open_new_trade_strategy_window_button.grid(row=2,column=3)
        self.figure = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.figure,master=self.master)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=1)
        self.frame.grid()
    # def display_stock_data(self):
    #     plt(self.trading_data,[range(0,len(self.trading_data))])
    #     self.figure.canvas.draw()
    #     print('Redrew Stock Data')
    '''Opens a trading strategies window to create strategies to pass to the main window'''
    def open_trading_strategies(self):
        self.trading_strategies_window = tk.Toplevel(self.master)
        self.trading_strategies_app = TradingStrategies(self.trading_strategies_window)
    def pass_file(self):
        return tk.filedialog.askopenfile(mode="r")
    def on_upload_csv_button_click(self):
        csv = self.pass_file()
        self.trading_data= pyquant.parse_csv(csv.name)
        self.master_strategy.add_stock_data(pyquant.parse_csv(csv.name))
        self.display_stock_data()

class TradingStrategies:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.initialize_widgets()
    def initialize_widgets(self):
        self.upload_data_button = tk.Button(self.frame,text='Close CSV')
        self.upload_data_button.grid(row=2,column=1)
        self.open_new_trade_strategy_window_button = tk.Button(self.frame,text='Open Trading Strategies')
        self.open_new_trade_strategy_window_button.grid(row=2,column=2)
        self.frame.pack()
    def add_field(self):


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
if __name__ == '__main__':
    main()