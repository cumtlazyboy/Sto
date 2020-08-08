import tushare as ts
import pandas as pd
import numpy as np
import csv
import re, time
import string
import os.path
import matplotlib.pyplot as plt

##queryDate = '20190102'
queryDate = '20200408'
downloadStartDate = '20140101'
downloadEndDate   = '20200430'
downloadStartDate = '20140101'
downloadEndDate   = '20200720'

##
##startDate = '20150101'
##endDate   = '20151231'
##
##startDate = '20160101'
##endDate   = '20161231'
##
##startDate = '20170101'
##endDate   = '20171231'
##
##
startDate = '20180101'
endDate   = '20181231'
##
startDate = '20160101'
endDate   = '20191231'
startDate = '20200601'
endDate   = '20201231'

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



def read_csv_file(_stock_name, _date,_open,_high,_low,_close,_volume):
##    if _freq == 'D':
##        dir_path = 'C:/python/csv/'
##    elif _freq == 'W':
##        dir_path = 'C:/python/csv_wk/'
##    elif _freq == 'M':
##        dir_path = 'C:/python/csv_mon/'
    dir_path = 'C:/python/csv/'
    DATA_PATH_NAME = dir_path + _stock_name + '.csv'
########    print (DATA_PATH_NAME)
    with open(DATA_PATH_NAME,"r",encoding="utf-8") as csvfile:
    #读取csv文件，返回的是迭代类型
        reader = csv.reader(csvfile)
        for row in reader :
            extract_csv_data(row, _date,_open,_high,_low,_close,_volume)
          


def calculateHighestPrice(_price):
    highestPrice = round(float(_price) * 1.100, 2)
##    print(f'price={price}, highestPrice={highestPrice}')
    return highestPrice

g_profitFileName = 'C:/python/csv/zhangting/profit.csv'
g_dirProfit = {}
#('000020.SZ', '2020-01-01', 9.5)
def saveProfitToCsv(ts_code, date, profit):
    writeMethod = 'w'
    isFileExist = os.path.isfile(g_profitFileName)
    if False == isFileExist:
        writeMethod = 'w'
    else:
        writeMethod = 'a'

    with open(g_profitFileName, writeMethod, encoding='utf-8') as f:
        writer = csv.writer(f)
        if False == isFileExist:
            writer.writerow(['ts_code', 'date', 'profit'])
        writer.writerow([ts_code, date, profit])
        
def deleteCsvFile(name):
    if True == os.path.isfile(name):
        os.remove(name)

g_profitFileName = 'C:/python/zhangting/whitelist.csv'
g_dirProfit = {}
g_delete_flag = True
#('000020.SZ', '2020-01-01', 9.5)
def saveParaToCsv(ts_code, date, profit):
    global g_delete_flag
    isFileExist = os.path.isfile(g_profitFileName)
    if True == isFileExist and g_delete_flag == True:
        g_delete_flag = False
        deleteCsvFile(g_profitFileName)
        time.sleep(5)
    isFileExist = os.path.isfile(g_profitFileName)
    with open(g_profitFileName, 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        if False == isFileExist:
            writer.writerow(['ts_code', 'date', 'profit'])
        writer.writerow([ts_code, date, profit])

kdj_stock_num = '601688.SH'
#首板成功率
g_cnt = 0

def ZT_success_rate(_stock_name):
    ZTprice = 0
    ZTSuccessCnt = 0
    ZTFailCnt = 0
    ZTSuccessCnt = 0
    ZT_rate = 0
    open_profit = 0  #以涨停次日开盘价计算收益
    close_profit = 0  #以涨停次日收盘价计算收益
    ave_open_profit = 0  #以涨停次日开盘价计算的  平均收益
    ave_close_profit = 0  #以涨停次日收盘价计算的  平均收益
    stockName = 0
    global g_cnt
    _date=[];_open=[];_high=[];_low=[];_close=[];_volume=[];  #define data
    read_csv_file(_stock_name,_date,_open,_high,_low,_close,_volume)
    length = len(_close)
    if length== 0:
        return
####    if _stock_name != '000698':    #debug  计算某一只票
####        return
    
    for i in range(2, length-1):
        ZTPredayPrice = calculateHighestPrice(_close[i-2])  #涨停前一天的假定涨停价
        ZTprice = calculateHighestPrice(_close[i-1])
        if ZTprice == _open[i]:  #开盘涨停就跳过
            continue
        if ZTprice == _high[i] and ZTPredayPrice > _close[i-1]:  #首板，当天最高价为涨停价，前一天收盘不能为涨停
            if ZTprice > _close[i]:
                ZTFailCnt = ZTFailCnt+1
####                print ('封板失败',_date[i])
            elif ZTprice == _close[i]:
                ZTSuccessCnt = ZTSuccessCnt+1
####                print ('封板成功',_date[i])              
            open_profit = round(_open[i+1]/ ZTprice - 1,2)
            close_profit= round(_close[i+1]/ ZTprice -1,2)
####            print (open_profit, close_profit)
            ave_open_profit = ave_open_profit + open_profit
            ave_close_profit = ave_close_profit + close_profit
##############        if ZTprice == _high[i] and ZTprice > _close[i]:
##############            ZTFailCnt = ZTFailCnt+1
################            print ('封板失败',_date[i])
##############        elif ZTprice == _high[i] and ZTprice == _close[i]:
##############            ZTSuccessCnt = ZTSuccessCnt+1
################            print ('封板成功',_date[i])
    if ZTFailCnt + ZTSuccessCnt>1:
        if ZTSuccessCnt/(ZTFailCnt+ZTSuccessCnt) >0.7:
            g_cnt= g_cnt +1
            ZT_rate = round(ZTSuccessCnt/(ZTFailCnt+ZTSuccessCnt),3)
            if _stock_name[0:2] == '00' or _stock_name[0:2] == '30':
                stockName = _stock_name+'.SZ'
            elif _stock_name[0:2] == '60':
                stockName = _stock_name+'.SH'
                print (stockName)
            saveParaToCsv(stockName,ZT_rate,ave_close_profit)
            print(_stock_name,'封板成功率=',ZT_rate,'；触及涨停次数=',ZTFailCnt + ZTSuccessCnt, g_cnt,)
            print(_stock_name,'                                          次日开盘平均收益%=',round(ave_open_profit*100/g_cnt, 2), '次日收盘平均收益%=',round(ave_close_profit*100/g_cnt,2))
##            print(f'whiteList count={len(_close)}')
        

def ZT_success_rate_all_stock():
    print('开始遍历所有股票')
    print('startDate =',startDate, 'endDate = ',endDate)
    with open('C:/python/csv/oneDayAllStock.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stock_name = row['ts_code'][:6]
            if stock_name[:2] == '00' or stock_name[:2] == '60':
                ZT_success_rate(stock_name)
    print('完成遍历所有股票')    

def main():    
    ZT_success_rate_all_stock()

if __name__ == '__main__':
    print('开始请求数据')
    main()
