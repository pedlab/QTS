from indicators import *

# Conventions
#   Signals passed to the trading functions
#       Buy: 1
#       Sell: -1
#       Hold: 0
#   Signals are output as an integer array, ex. [1,0,0,-1,1,0,0,0,0]

# Generates signals when the lines cross
# If no cross occurs, will generate a hold signal
def macd_signal(data, short_ema, long_ema, signal_period):
    # If the MACD is above the signal line, 1, else, 0
    positions = []
    # The MACD values calculated
    macd = []
    sn = []
    # Compiles an array of positions for back testing; see above for what the signals generated mean (Line: 4)
    signals = []
    for x in range(long_ema, len(data)):
        window = data[:x + 1]
        long_ema_value = ema(data[:x + 1], long_ema)
        short_ema_value = ema(data[:x + 1], short_ema)
        macd.append(short_ema_value - long_ema_value)

    for x in range(signal_period, len(macd)):
        sn.append(ema(macd[:signal_period + 1], signal_period))

    for x in range(0, len(sn)):
        if macd[x + signal_period] > sn[x]:
            positions.append(1)
        else:
            positions.append(0)

    # Indicator Positions to Trading Signals
    if positions[0] == 0:
        signals.append(-1)
    else:
        signals.append(1)
    for x in range(1, len(positions)):
        if positions[x] == positions[x - 1]:
            signals.append(0)
        else:
            if positions[x] == 1:
                signals.append(1)
            else:
                signals.append(-1)
    return signals

# Aroon based signal generation - if aroon up is above aroon down, buy, and vice versa
# Data: Raw stock prices in CSV (Use OHLC average)
# Time length: How long the indicator will search past data, by default 25
#
def aroon_signal(data, time_length=25, threshold_a = .7, threshold_b =0.2):
    signals = []
    for x in range(time_length, len(data)):
        # Checks if aroon up is greater than aroon down
        aroon_up = aroon(data[x - time_length:x], time_length)[0]
        aroon_down = aroon(data[x - time_length:x], time_length)[1]
        # Edit here to change trading thresholds for aroon up and down values
        if (aroon_up > threshold_a) & (aroon_down <= threshold_b):
            signals.append(1)
        elif (aroon_down > threshold_a) & (aroon_up <= threshold_b):
            signals.append(-1)
        else:
            signals.append(0)
    return signals
