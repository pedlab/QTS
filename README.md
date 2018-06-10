# pyquant
[WIP] PyQuant is a python 3  library for quantitative trading strategy backtesting.

<b> Features </b>
  <ul>
    <li>
      <p>
      Backtesting engine - pyquant allows users to define trading rules and apply them to historical stock data to test strategies, including stop loss and take profit commands
      </p>
     </li>
     <li>
      <p>
      Strategy evaluation - pyquant has several metrics to gauge the performance of your trading algorithm; Sharpe Ratio, Compound Annual Returns, HPRS.
      </p>
     </li>
     <li>
      <p>
      Technical indicators - pyquant comes equipped with the Aroon, MACD, RSI and OBV indicators.
      </p>
     </li>
  </ul>
<p>
<h1>Sample signals-based simulation</h1>
<pre><code>
trader = Trader(0.1,1000)
trader.add_stock_data('CSV.csv')
trader.signals = aroon_signals(trader.data, 2, 0.8,0.9)
trader.execute_trades()
</pre></code>
</p>
<p>
<h1>Sample hold and wait simulation</h1>
<pre><code>
hold_and_wait = Trader(0.1,10000)
hold_and_wait.add_stock_data('CSV.csv')
dictionary = {
    'TRADE_IT': 1,
    'Entry Price': 26.13,
    'Stop Loss': 26,
    'Target Price 1': 26.15,
    'Target Price 2': 26.8,
    'Type of Trade': 'LONG',
    'Pct of Available Cash': 0.15,
    'TP1 vs TP2 Split': 0.5,
    }
hold_and_wait.execute_hold_and_wait(dictionary,hold_and_wait.data,hold_and_wait.balance)
for entry in hold_and_wait.log:
    print(entry)
</code></pre>
</p>