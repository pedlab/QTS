import tkinter as tk
import pyquant
import matplotlib
from tkinter import StringVar
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import gridspec
''' 
Definitions
    Epochs are how data is divided into segments here; first 15 bars, third 1/4, etc.
'''
class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.grid_rowconfigure(0,weight=1)
        self.master.grid_columnconfigure(0,weight=1)
        self.frame = tk.Frame(master,bg='cyan',width = 100,height=100)
        self.initialize_widgets()
        self.master_strategy = pyquant.strategy()
    '''Initialize all widgets here'''
    def initialize_widgets(self):
        ''' Menu '''
        menubar = tk.Menu(self.frame)
        self.master.config(menu=menubar)
        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Open CSV", command=self.on_upload_csv_button_click)
        fileMenu.add_command(label="Refresh", command=self.display_stock_data)
        fileMenu.add_command(label="Close", command=quit)
        menubar.add_cascade(label="File", menu=fileMenu)

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
        print('Pre-split data \n'+ str(self.trading_data[column]))
        return pyquant.split_bars_fraction(self.trading_data[column],count)

    def refresh(self):
        self.display_stock_data(epoch = 0, epoch_count = int(self.split_count.get()))
        self.current_epoch = 0    

    def save_simulation_results(self):
        dict = {}
        dict['trading data'] = self.trading_data

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
        print('Data to be plot \n'+ str(data_to_plot))

        self.stock_data_graph.plot([ x for x in range(0,len(data_to_plot[epoch]))],data_to_plot[epoch])
        self.figure.canvas.draw()
        
        print('Redrew Stock Data')
    '''Opens a trading strategies window to create strategies to pass to the main window'''

    def display_equity(self,epoch = 0):
        self.profit_graph.plot([ x for x in range(0,len(self.trading_data[epoch]))],self.trading_data[epoch])
        self.figure.canvas.draw()
        print('Redrew Profit Movement Data')

    def open_trading_strategies(self):
        self.trading_strategies_window = tk.Toplevel(self.master)
        self.trading_strategies_app = TradingStrategies(self.trading_strategies_window)
    def pass_file(self):
        return tk.filedialog.askopenfile(mode="r")
    def on_upload_csv_button_click(self):
        csv = self.pass_file()
        self.trading_data = pyquant.parse_csv(csv.name)
        print('Data Loaded')
        print(pyquant.parse_csv(csv.name))
        self.master_strategy.add_stock_data(pyquant.parse_csv(csv.name))
        self.display_stock_data()
        self.file_name['text']=csv.name

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
def main():
    root = tk.Tk()
    root.attributes('-fullscreen',False)
    app = MainWindow(root)
    root.mainloop()
if __name__ == '__main__':
    main()