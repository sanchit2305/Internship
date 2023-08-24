import pandas as pd
df1 = pd.read_csv('^NSEI.csv')
df2 = pd.read_csv('^NSEBANK.csv')
df3 = pd.read_csv('NIFTY_FIN_SERVICE.NS.NIFTY_FIN_SERVICE.NS.csv')
col1 = df1.loc[:,'High']
col2 = df2.loc[:,'High']
col3 = df3.loc[:,'High']
j = 0
total = 0
final = []
for i  in range(len(col1)):
    if ((i+1)%5 !=0):
        total = total + col1[i]
        final.append('-')
    else:
        total = total + col1[i]
        final.append(round(total/5, 2))
        total = 0
df1["5-day Avg"] = final
df1.to_csv('^NSEI.csv')

j = 0
total = 0
final = []
for i  in range(len(col2)):
    if ((i+1)%5 !=0):
        total = total + col2[i]
        final.append('-')
    else:
        total = total + col2[i]
        final.append(round(total/5, 2))
        total = 0
df2["5-day Avg"] = final
df2.to_csv('^NSEBANK.csv')

j = 0
total = 0
final = []
for i  in range(len(col3)):
    if ((i+1)%5 !=0):
        total = total + col3[i]
        final.append('-')
    else:
        total = total + col3[i]
        final.append(round(total/5, 2))
        total = 0
df3["5-day Avg"] = final
df3.to_csv('NIFTY_FIN_SERVICE.NS.NIFTY_FIN_SERVICE.NS.csv')