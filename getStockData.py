import requests
import pandas as pd
import requests
import os
import time
#------參數設定開始---------  98-102年 => 2009~2013
startDate = 20220710  #開始日 日期不要隔太久 資料會抓很久
endDate = 20220720  #結束日
#------參數設定結束---------

for i in range(startDate,endDate+1):

    try:
        if(int(i/100)%100>12 or int(i/100)%100==0): #超過13 or 0月 是不是合法月份
            continue
        if(i%100>31 or i%100==0): #超過31和0不是合法日期
            continue
        # 把csv檔抓下來
        url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date='+ str(i) +'&type=ALL'
        print(url)

        tryFlag = True
        data = None
        start = time.time()
        while(tryFlag):
            res = requests.get(url)
            end = time.time()

            if end-start<1:
                print("時間過短 資料可能有誤 重新請求")
                time.sleep(10)
                continue
            if res.status_code == requests.codes.ok:

                data = res.text
                tryFlag = False
            else:
                time.sleep(2)
                print("連線異常重新嘗試")

        if(data==''  or data is None or len(data)<2000): # len(data)<2000 為錯誤資訊
            print("此日:",i," 無資料")
            continue

        # 把爬下來的資料整理乾淨
        cleaned_data = []
        for da in data.split('\n'):
            if len(da.split('","')) == 16 and da.split('","')[0][0] != '=':
                cleaned_data.append([ele.replace('",\r','').replace('"','')
                    for ele in da.split('","')])

        # 輸出成表格並呈現在excel上
        df = pd.DataFrame(cleaned_data, columns = cleaned_data[0])
        df = df.set_index('證券代號')[1:]
        date = str(i)
        dir = date[:4]+'/'+date[4:6]
        if not os.path.exists(dir):
            os.makedirs(dir)
        filename=(dir +"/{}-{}-{}.csv".format(date[:4],date[4:6],date[6:8]))
        df.to_csv(filename)
        print("寫檔入",filename)
    except Exception as e:
        print("第",i,"日執行有誤")
        print(e)

