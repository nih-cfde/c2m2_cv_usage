import pandas as pd

df = pd.read_csv('table.csv')
#df = df[(df.iloc[:, 1:] != 0).any(1)]
df = df[(df.iloc[:, 1:-1] > 0).any(1)]
df.to_csv('table_no_zero.csv', index=False)
