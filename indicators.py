import math

# Returns the aroon up and aroon down values for the set time period with
# user defined time length (by default 25)
def aroon(data, time_length=25):
    highest = 0
    lowest = math.inf
    lowest_index = highest_index = 0
    for x in range(len(data) - 1, len(data) - time_length - 1, -1):
        if data[x] > highest:
            highest = data[x]
            highest_index = x
        if data[x] < lowest:
            lowest = data[x]
            lowest_index = x
    aroon_down = -(time_length - len(data) - 1 - lowest_index) / time_length
    aroon_up = -(time_length - len(data) - 1 - highest_index) / time_length
    return [aroon_up, aroon_down]

# Returns the Relative Strength Index for the selected period
def RSI(data, time_length):
    loss_sum = 0
    gain_sum = 0
    for x in range(len(data) - 1, len(data) - time_length - 1, -1):
        if data[x] > data[x - 1]:
            gain_sum = gain_sum + data[x] - data[x - 1]
        elif data[x] < data[x - 1]:
            loss_sum = loss_sum + data[x - 1] - data[x]
    if (loss_sum == 0) & (gain_sum > 0):
        return 1
    relative_strength = gain_sum / loss_sum
    print(relative_strength)
    return (100 - 100 / (1 + relative_strength)) / 100

# Returns the EMA for the selected period
def ema(s, n):
    ema = []
    j = 1

    # get n sma first and calculate the next n period ema
    sma = sum(s[:n]) / n
    multiplier = 2 / float(1 + n)
    ema.append(sma)

    # EMA(current) = ( (Price(current) - EMA(prev) ) x Multiplier) + EMA(prev)
    ema.append(((s[n] - sma) * multiplier) + sma)

    # now calculate the rest of the values
    for i in s[n + 1:]:
        tmp = ((i - ema[j]) * multiplier) + ema[j]
        j = j + 1
        ema.append(tmp)
    return ema[-1]

# Returns the on balance volume value for the period
def OBV(data,volume_data):
    on_balance_volume = 0
    for x in range(1,len(data)):
        if data[x]>data[x-1]:
            on_balance_volume = on_balance_volume+volume_data[x]
        elif data[x]>data[x-1]:
            on_balance_volume = on_balance_volume-volume_data[x]
    return on_balance_volume


