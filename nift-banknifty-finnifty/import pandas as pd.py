import pandas as pd
filename = '^NSEI.csv'
data = pd.read_csv(filename)
print(data.to_string()) 