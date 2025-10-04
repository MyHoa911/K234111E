import pandas as pd
#df=dataframe, pd=pandas
df=pd.read_csv("../dataset/SalesTransactions.csv",
               sep=',', encoding='utf-8', low_memory=False)

print(df)