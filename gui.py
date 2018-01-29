from tkinter import *
from tkinter import filedialog
import trading
import utilities
import signals
import matplotlib

# class window(Frame):
#     def __init__(self,master=None):
#         Frame.__init__(self,master)
#         self.createViews()
#     def createViews(self):
#         upload_csv_button = Button(text = "Open CSV", command = self.on_upload_csv_button_click())
#         upload_csv_button.pack()
#     def pass_file(self):
#         return filedialog.askopenfile(mode="r")
#     def on_upload_csv_button_click(self):
#         csv = self.pass_file()
#         utilities.parse_csv(csv.name)
# def main():
#     root = Tk()
#     root.geometry("250x150+300+300")
#     app = window()
#     root.mainloop()
# main()