import pandas as pd
import numpy as np

risk_free_rate = 0
initial_cash = 10000
df = pd.read_csv('SPY.csv')
closes = df.Close.to_numpy()
cash, account = [np.array([initial_cash] * len(closes)) for _ in range(2)]
upwards, changes_12, positions, shares = [np.zeros(len(closes)) for _ in range(4)]

for i in range(12, len(closes)):
  if (closes[i] - closes[i-12] >= risk_free_rate):
    upwards[i] = True
    if upwards[i-1]:
      cash[i] = cash[i-1]
      shares[i] = shares[i-1]
      positions[i] = shares[i] * closes[i]
    else:
      shares[i] = cash[i-1] // closes[i]
      positions[i] = shares[i] * closes[i]
      cash[i] = cash[i-1] - positions[i]
    account[i] = cash[i] + positions[i]
  else:
    upwards[i] = False
    shares[i] = 0
    positions[i] = 0
    if upwards[i-1]:
      cash[i] = cash[i-1] + shares[i-1] * closes[i]
    else:
      cash[i] = cash[i-1]
    account[i] = cash[i] + positions[i] 
  changes_12[i] = (closes[i] - closes[i-12]) / closes[i-12]

benchmark_shares = initial_cash // closes[0]
benchmark = closes * benchmark_shares

df['Upward'] = upwards.tolist()
df['Change_12'] = changes_12.tolist()
df['Shares'] = shares.tolist()
df['Position'] = positions.tolist()
df['Cash'] = cash.tolist()
df['Account'] = account.tolist()
df['Benchmark'] = benchmark.tolist()

print(df.head)
df.to_csv('SPY_simulation_12.csv')
chart = df.plot.line(x='Date', y=['Account', 'Benchmark'], grid=True, figsize=(20,12), xticks=np.arange(0, 346, 12), yticks=np.arange(0, 120000, 10000))
chart.tick_params(axis='x', rotation=90)
chart.figure.savefig('simulation_12.jpg')