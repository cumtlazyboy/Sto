import tushare as ts
import pandas as pd
import numpy as np
import csv
import re, time
import string
import os.path
import matplotlib.pyplot as plt

#画图显示
import matplotlib.pyplot as plt
from pylab import mpl #正常显示画图时出现的中文
mpl.rcParams['font.sans-serif']=['SimHei'] #这里使用微软雅黑字体
mpl.rcParams['axes.unicode_minus']=False #画图时显示负号

g_dirProfit = {}



##queryDate = '20190102'
queryDate = '20200408'
downloadStartDate = '2018-01-01'
downloadEndDate   = '2020-04-06'


startDate = '20190101'
endDate   = '20191231'


startDate = '20160101'
endDate   = '20191231'
 
STOCK_FILE = '300123.SZ.csv'   



EXCHANGE_SHARE = 700
GRID_SET = 0.03  #网格差价
INITIAL_SHARE = 17001  #起始的股份，1000股，底仓




def string_to_float(str):
    return float(str)

def roundf2(data):
    return round(float(data), 2)






########STOCK_FILE = '601688.csv'   #华泰证券
########STOCK_FILE = '512000.csv'   #券商etf
DATA_PATH = 'C:/python/csv/'
DATA_PATH_NAME = DATA_PATH + STOCK_FILE




def extract_csv_data2(row, _date,_time,_o,_h,_c):
    if row[2] == 'trade_time':
        return
##    if row[1] < startDate or row[1] > endDate:
##        return
##    print (row[2], row[3])
##    _date.append(row[2])
    _date.append(row[2][0:10])
    _time.append(row[2][-8:])
##    print (_time)
    _o.append(float(row[3]))
    _h.append(float(row[5]))
    _c.append(float(row[4]))
    
def read_csv_file2(_stock_name, _freq, _date,_time,_open,_high,_close):
##    if _freq == 'MIN':
##        dir_path = 'C:/python/csv_min/'
##    elif _freq == 'D':
##        dir_path = 'C:/python/csv/'
##    elif _freq == 'W':
##        dir_path = 'C:/python/csv_wk/'
##    elif _freq == 'M':
##        dir_path = 'C:/python/csv_mon/'
    STOCK_FILE = '0'
    dir_path = 'C:/python/20200106to20200717/'
    if _stock_name[:2] == '30'or _stock_name[:2] == '00':
        STOCK_FILE = _stock_name+ '.SZ.csv'
    elif _stock_name[:2] == '60':
        STOCK_FILE = _stock_name+'.SH.csv'
##    STOCK_FILE = '300123.SZ.csv'  
    DATA_PATH_NAME = dir_path + STOCK_FILE
    print (DATA_PATH_NAME)
    try:
        with open(DATA_PATH_NAME,"r",encoding="utf-8") as csvfile:
            #读取csv文件，返回的是迭代类型
            reader = csv.reader(csvfile)
            for row in reader :
                extract_csv_data2(row, _date,_time,_open,_high,_close)
##            print (_date, _open)

            
    except Exception as e:
        STOCK_FILE = '1'
        print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


def calculateHighestPrice(price):
    highestPrice = round(float(price) * 1.100, 2)
##    print(f'price={price}, highestPrice={highestPrice}')
    return highestPrice

g_profitFileName = 'C:/python/zhangting/profit.csv'
g_dirProfit = {}
#('000020.SZ', '2020-01-01', 9.5)
def saveParaToCsv(ts_code, date, profit):
    isFileExist = os.path.isfile(g_profitFileName)
    with open(g_profitFileName, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        if False == isFileExist:
            writer.writerow(['ts_code', 'date', 'profit'])
        writer.writerow([ts_code, date, profit])

def ZT_strategy2(_stock_name):  
    global stock_cnt
    _freq = 'MIN' #分钟线 
    _date=[];_time=[];_open=[];_high=[];_low=[];_close=[];_volume=[];  #define data

##    read_csv_file(_stock_name,_date,_open,_high,_low,_close,_volume)
    print(_stock_name)
    read_csv_file2(_stock_name, _freq,_date,_time,_open,_high,_close)
    ts_code = 0
    date = 0
    profit = 0
    
    length = len(_close)
    if length== 0:
        return
    print("lenth=", length)
    idx=[];
    for i in range(1,length):
        if _time[i] == "15:00:00":
            idx.append(i)
##            print (_date[i], _close[i] )
##            print (idx)
            
    length = len(idx)   
    for j in range(2, length):
        index = idx[j]
        price = calculateHighestPrice(_close[idx[j-2]])
##        print ( _date[index],_time[index], _close[index], price, _close[idx[j-1]])
        
        if price == _close[idx[j-1]]:  ##涨停价
            print ( _date[index],_time[index], _close[index], price, _close[idx[j-1]])
            ts_code = _stock_name
            date= _date[index]
            profit = _close[index]/_close[idx[j-1]]-1
            saveParaToCsv(ts_code,date,profit)
        


##    print(_stock_name, high_cnt, close_cnt)
    


def ZT_calculate_all_stock():  #遍历所有A股的网格交易次数
    print('开始遍历所有股票')
##    search_date = 20200505
    with open('C:/python/csv/oneDayAllStock.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stock_name = row['ts_code'][:6]
            ZT_strategy2(stock_name)
##            print(stock_name)
##            grid_uniform_strategy(stock_name)
##########################            print('1',row['ts_code'][:6],row['pe'])

##            if row['pe'] == '':
##                continue
####            if (float(row['pe']) >20) or (row['pe'] ==''):
####            if (float(row['pe']) >20):
####                continue
##            stock_name = row['ts_code'][:6]
##            ZT_strategy2(stock_name, search_date)
##    print(search_date, high_cnt, close_cnt)
    print('完成遍历所有股票')





def calculateProfit(fileName):
    global g_dirProfit
    g_dirProfit = {}
    dirtCount = {}
    with open(fileName, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row['date']
            value = row['profit']
            if date not in g_dirProfit:
                g_dirProfit[date] = float(value)
                dirtCount[date] = 1
            else:
                g_dirProfit[date] = g_dirProfit[date] + float(value)
                dirtCount[date] = dirtCount[date] + 1

    g_dirProfit = dict(sorted(g_dirProfit.items(), key=lambda d: d[0], reverse=False))
    for k in g_dirProfit:
        g_dirProfit[k] = round(g_dirProfit[k] *100/ dirtCount[k], 4)
    print(g_dirProfit)

def drawProfitPic():
    print(g_dirProfit)
    totalProfit = 0
    averageProfit = 0
    x1 = list(g_dirProfit.keys())
    y1 = list(g_dirProfit.values())
    plt.plot(x1, y1, label='Frist line', linewidth=3, color='r', marker='o',
             markerfacecolor='blue', markersize=12)
    plt.xlabel('日期')
    plt.ylabel('收益率')
    for i in range(len(y1)):
        totalProfit += y1[i]
    averageProfit = round(totalProfit / len(y1), 2)
    plt.title(str(len(y1)) + '天' + '平均收益率: ' + str(averageProfit))
    plt.legend()
    plt.show()
    
##ttm市盈率获取https://tushare.pro/document/2?doc_id=128

def main():
    
##    ZT_calculate_all_stock()
##    stock_name = 000001.SZ.csv"

##    ZT_strategy2(STOCK_FILE)


    ##    ZT_calculate_all_stock()
    calculateProfit('C:/python/zhangting/profit.csv')
    drawProfitPic()


if __name__ == '__main__':
    print('开始请求数据')
    main()
