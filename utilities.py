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
    return items