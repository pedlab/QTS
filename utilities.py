import numpy
import csv

def sharpe_ratio(data,rfr):
    hprs = HPRS(data)
    ahpr = AHPR(data)
    print('Sharpe Ratio', (ahpr -rfr) / numpy.std(hprs))

def HPRS(data):
    hprs = []
    price_changes = []
    for x in range(1, len(data)):
        if data[x] != data[x - 1]:
            price_changes.append(data[x])
    for x in range(1, len(price_changes)):
        hprs.append(price_changes[x] / price_changes[x - 1])
    return hprs

def AHPR(data):
    return numpy.mean(HPRS(data))

def CAR(data):
    hprs = HPRS(data)
    car = 1
    for x in hprs:
        car = car * x
    car = car ** (1 / len(hprs))
    return car

# Cuts the stock data to fit the signals
# For example, if there are 10,000 bars and 9,975 signals, it will cut the bars
# so that it starts at index 25
def trim_data(signals,data):
    return data[(len(data)-len(signals)):]

def split_bars_fraction(data,epoch_count = 1, allow_uneven_end = True):
    result = []
    step = int(len(data)/epoch_count)
    x,y = step,0
    main_range = step * epoch_count
    print(step)
    print(main_range)
    while x <= main_range:
        result.append(data[y:x])
        x = x + step
        y = y + step
    if allow_uneven_end:
        result.append(data[main_range:len(data)])
    return result


def split_bars_absolute(data, time_length, allow_uneven_end = True):
    x = 0
    result = []
    while x + time_length < len(data):
        result.append(data[x:x+time_length])
        x = x + time_length
    if allow_uneven_end:
        result.append(data[x:len(data)])
    return result


#  Accepts CSV files following Yahoo finance's format
#  Ensure that there are no missing fields in the csv before passing it to the file
#  Parse a csv and returns a tuple with the following values, in order:
#   OHCL average array
#   Opening prices array
#   High prices array
#   Closing prices array
#   Low prices array
#   Adjusted close
#   Volume
def parse_csv(file_path):
    items = ([], [], [], [], [], [], [])
    with open(file_path) as file:
        reader = csv.reader(file, delimiter=",")
        reader = list(reader)
        reader = reader[1:]
        for row in reader:
            sum = 0
            for x in range(1,5):
                sum = sum + float(row[x])
            items[0].append(sum/4)
            items[1].append(float(row[1]))
            items[2].append(float(row[2]))
            items[3].append(float(row[3]))
            items[4].append(float(row[4]))
            items[5].append(float(row[5]))
            items[6].append(float(row[6]))
        print(items[1])
    return items
