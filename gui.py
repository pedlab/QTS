from tkinter import *
from tkinter import filedialog
import csv
import datetime
import trading
import utilities
import signals
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler

class window(Frame):
    trading_data =  None
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.createViews()
    def createViews(self):
        upload_csv_button = Button(text = "Open CSV", command = self.pass_file())
        upload_csv_button.pack()
        create_strategies = Button(text = "Open trading rules creator", command = self.open_trading_strategies_window())
        create_strategies.pack()
    def pass_file(self):
        return filedialog.askopenfile(mode="r")
    def on_upload_csv_button_click(self):
        csv = self.pass_file()
        self.trading_data = utilities.parse_csv(csv.name)
        print(self.trading_data)
    def open_trading_strategies_window(self):
        window = Tk.Toplevel()
    def segment_training_data(self, data, count, allow_incomplete, name = None):
        items = utilities.split_bars_fraction(data, count)
        for x in range (0, count):
            filename = name + str("_"+x)+str("_"+datetime.datetime.now()+".csv","a+")
            with open(filename,"a+") as file:
                filewriter = csv.writer(file, quoting = csv.QUOTE_NONE)
                for y in range (0,len(items[x])):
                    filewriter.writerow(items[x][y])



def main():
    root = Tk()
    root.wm_title("QTS Trading Simulator")
    root.geometry("250x150+300+300")
    app = window()
    root.mainloop()
main()