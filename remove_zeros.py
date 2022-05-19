import pandas as pd

df = pd.read_csv('table.csv')
df = df[(df.iloc[:, 1:] != 0).all(1)]
df.to_csv('table_no_zero.csv', index=False)
