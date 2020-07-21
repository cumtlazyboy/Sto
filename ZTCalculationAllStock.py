import tushare as ts
import pandas as pd
import numpy as np
import csv
import re, time
import string

##queryDate = '20190102'
queryDate = '20200408'
downloadStartDate = '2018-01-01'
downloadEndDate   = '2020-04-06'


startDate = '20190101'
endDate   = '20191231'


startDate = '20160101'
endDate   = '20191231'
 
STOCK_FILE = '000001.csv'   #平安银行，网格3%，2019年卖出64次



EXCHANGE_SHARE = 700
GRID_SET = 0.03  #网格差价
INITIAL_SHARE = 17001  #起始的股份，1000股，底仓




def string_to_float(str):
    return float(str)

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


########STOCK_FILE = '601688.csv'   #华泰证券
########STOCK_FILE = '512000.csv'   #券商etf
DATA_PATH = 'C:/python/csv/'
DATA_PATH_NAME = DATA_PATH + STOCK_FILE

def read_csv_file(_stock_name, _date,_open,_high,_low,_close,_volume):
    _data_path_name = DATA_PATH+_stock_name+'.csv'
    with open(_data_path_name,"r",encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader :
            extract_csv_data(row, _date,_open,_high,_low,_close,_volume)



stock_cnt = 0
high_cnt = 0
close_cnt = 0

def ZT_strategy(_stock_name, _search_date):  
    global stock_cnt
    _date=[];_open=[];_high=[];_low=[];_close=[];_volume=[];  #define data
    read_csv_file(_stock_name,_date,_open,_high,_low,_close,_volume)


    length = len(_close)
    if length== 0:
        return
    
    for i in range(2,length):
        if _search_date == _date[i]:
            if _high[i] / _close[i-1]>1.0997:
                high_cnt = high_cnt+1
            if _close[i] / _close[i-1]>1.0997:
                close_cnt = close_cnt+1

##    print(_stock_name, high_cnt, close_cnt)
    


def ZT_calculate_all_stock():  #遍历所有A股的网格交易次数
    print('开始遍历所有股票')
    search_date = 20200505
    with open('C:/python/csv/oneDayAllStock.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
##########################            print('1',row['ts_code'][:6],row['pe'])

            if row['pe'] == '':
                continue
##            if (float(row['pe']) >20) or (row['pe'] ==''):
##            if (float(row['pe']) >20):
##                continue
            stock_name = row['ts_code'][:6]
            ZT_strategy(stock_name, search_date)
    print(search_date, high_cnt, close_cnt)
    print('完成遍历所有股票')

    
##ttm市盈率获取https://tushare.pro/document/2?doc_id=128

def main():
    
    ZT_calculate_all_stock()
    


if __name__ == '__main__':
    print('开始请求数据')
    main()
