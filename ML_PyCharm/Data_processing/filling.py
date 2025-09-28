from numpy import nan as NA
import pandas as pd

data=pd.DataFrame([[7.,6.5,4.7],
                [9.,6.,NA],
                [NA,NA,NA],
                [8.,NA,9.2]])
print(data)
print("-"*10)
cleaned = data.fillna(data.mean()) #điền các giá trị NA = giá trị TB của từng cột
print(cleaned)
