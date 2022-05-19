import pandas as pd

df = pd.read_csv('out.txt')
df = df[(df.iloc[:, 1:] != 0).all(1)]
df.to_csv('out_no_zero.csv', index=False)
