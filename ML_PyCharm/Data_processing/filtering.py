from numpy import nan as NA
import pandas as pd

data=pd.DataFrame([[2.,6.4,9.],
                [NA,4.7,7.],
                [NA,NA,NA],
                [5.8,NA,6.]])
print(data)
print("-"*10)
cleaned = data.dropna() #xóa hàng nào có ít nhất 1 giá trị NA
print(cleaned)
cleaned2=data.dropna(how='all') #chỉ xóa hàng nào toàn bộ đều NA
print(cleaned2)