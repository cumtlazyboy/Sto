import tushare as ts
import pandas as pd
import numpy as np
import csv
import re, time
import string
import os.path

#画图显示
import matplotlib.pyplot as plt
from pylab import mpl #正常显示画图时出现的中文
mpl.rcParams['font.sans-serif']=['SimHei'] #这里使用微软雅黑字体
mpl.rcParams['axes.unicode_minus']=False #画图时显示负号


startDate = '20200626'
endDate   = '20200731'


def roundf2(data):
    return round(float(data), 2)


def extract_csv_data(row, _date,_o,_h,_l,_c,_v):
    if row[1] == 'trade_date':
        return
    if row[1] < startDate or row[1] > endDate:
        return
    _date.append(row[1])
    _o.append(float(row[2]))
    _h.append(float(row[3]))
    _l.append(float(row[4]))
    _c.append(float(row[5]))



def read_csv_file(_stock_name, _date,_open,_high,_low,_close,_volume):
    dir_path = 'C:/python/csv/'
    DATA_PATH_NAME = dir_path + _stock_name + '.csv'
    with open(DATA_PATH_NAME,"r",encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader :
            extract_csv_data(row, _date,_open,_high,_low,_close,_volume)
          


def calculateHighestPrice(_price):
    highestPrice = round(float(_price) * 1.100, 2)
##    print(f'price={price}, highestPrice={highestPrice}')
    return highestPrice


CANDIDATE_FILE = 'C:/python/zhangting/candidateList.csv'
g_dirProfit = {}
#('000020.SZ', '2020-01-01', 9.5)
def saveToCsv(ts_code, date, profit):
    writeMethod = 'w'
    isFileExist = os.path.isfile(CANDIDATE_FILE)
    if False == isFileExist:
        writeMethod = 'w'
    else:
        writeMethod = 'a'

    with open(CANDIDATE_FILE, writeMethod, encoding='utf-8') as f:
        writer = csv.writer(f)
        if False == isFileExist:
            writer.writerow(['ts_code', 'date', 'profit'])
        writer.writerow([ts_code, date, profit])
        
def deleteCsvFile(name):
    if True == os.path.isfile(name):
        os.remove(name)
        time.sleep(8)




def openPriceEqualSurgePrice(_stock_name):
    ZTprice = 0
    stockName = 0
    _date=[];_open=[];_high=[];_low=[];_close=[];_volume=[];  #define data
    read_csv_file(_stock_name,_date,_open,_high,_low,_close,_volume)
    length = len(_close)
    if length== 0:
        return

    for i in range(1, length-1):
        ZTprice = calculateHighestPrice(_close[i-1])
        if ZTprice == _open[i]:
            close_profit =1
            saveToCsv(_stock_name,_date[i],close_profit)

        

g_dirStock = {}
def selectCandidateBaseOnDayK(fileName):
    global g_dirStock
    dirtCount = {}
    if False == os.path.isfile(fileName):
        return;
    with open(fileName, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row['date']
            value = row['profit']
            stock = row['ts_code']
            if date not in g_dirStock:
                dirtCount[date] = 1
                g_dirStock[date] = stock
            else:
                dirtCount[date] = dirtCount[date] + 1
                g_dirStock[date] = g_dirStock[date] + ',' + stock

    g_dirStock = dict(sorted(g_dirStock.items(), key=lambda d: d[0], reverse=False))
    print(g_dirStock)
    return g_dirStock
        



STOCK_LIST = 'C:/python/zhangting/whitelist.csv'
STOCK_LIST = 'C:/python/csv/oneDayAllStock.csv'
def runningAllStock():
    print('开始遍历所有股票')
    print('startDate =',startDate, 'endDate = ',endDate)
    with open(STOCK_LIST, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stock_name = row['ts_code'][:6]
            if stock_name[:2] == '00' or stock_name[:2] == '60':
                openPriceEqualSurgePrice(stock_name)

    print('完成遍历所有股票')    


CANDIDATE_FILE = 'C:/python/zhangting/candidateList.csv'
def main():
    deleteCsvFile(CANDIDATE_FILE)
    runningAllStock()
    selectCandidateBaseOnDayK(CANDIDATE_FILE)

    
if __name__ == '__main__':
    print('开始请求数据')
    main()
