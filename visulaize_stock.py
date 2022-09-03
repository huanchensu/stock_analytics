import talib as ta #若無法pip install https://www.lfd.uci.edu/~gohlke/pythonlibs/
import pandas as pd
import matplotlib.pyplot as plt
import csv
import glob
import os
from datetime import datetime
targetStockId = '2330' #改股票代碼改這
maDay = 20 #調整天數改這
storedList = []
indexList= []

for filename in glob.glob('*\*\*.csv'):
    with open(os.path.join(os.getcwd(), filename), 'r',encoding='utf-8') as f:

        reader = csv.reader(f)
        for row in reader:
            if('2330' in row ):
                storedList.append(row)
                indexList.append(filename.split('.')[0][8:])

df=pd.DataFrame(storedList,columns=['證券代號','證券名稱','成交股數','成交筆數','成交金額','開盤價','最高價','最低價','收盤價','漲跌(+/-)','漲跌價差','最後揭示買價','最後揭示買量','最後揭示賣價','最後揭示賣量','本益比'],index=pd.to_datetime(indexList, format='%Y-%m-%d'))
df.index.name = 'Date'

print(df.head(),type(df.index))
df['Low'] = df['最低價'].astype(float)
df['High'] = df['最高價'].astype(float)
df['Close'] = df['收盤價'].astype(float)
#ADX - Average Directional Movement Index
df['avg'] = ta.ADX(df['High'],df['Low'], df['Close'], timeperiod=maDay)
df['avg'].plot(figsize=(18,10),label="ADX")


#RSI - Relative Strength Index
df['Relative'] = ta.RSI(df['Close'],timeperiod=maDay)
df['Relative'].plot(figsize=(18,10),label="RSI")


#DX - Directional Movement Index
df['DX'] = ta.DX(df['High'], df['Low'], df['Close'], timeperiod=maDay)
df['DX'].plot(figsize=(18,10),label="DMI")
plt.grid(True)
plt.legend(loc='upper right')
print(df['High'], df['Low'], df['Close'])
plt.title("StockId:"+targetStockId +" Stock Analysis")
plt.show()
