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



startDate = '20180101'
endDate   = '20181231'
##
startDate = '20160101'
endDate   = '20191231'

startDate = '20200126'
endDate   = '20200631'

startDate = '20200528'
endDate   = '20200631'

##startDate = '20200626'
##endDate   = '20200731'

##startDate = '20200126'
##endDate   = '20200631'
##
startDate = '20191226'
endDate   = '20200831'
startDate = '20191226'
endDate   = '20200631'
startDate = '20200626'
endDate   = '20200731'
##
##startDate = '20181226'
##endDate   = '20191231'
####
startDate = '20171226'
endDate   = '20181231'
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

g_profitFileName2 = 'C:/python/zhangting/profit.csv'
g_dirProfit = {}
#('000020.SZ', '2020-01-01', 9.5)
def saveProfitToCsv(ts_code, date, profit):
    writeMethod = 'w'
    isFileExist = os.path.isfile(g_profitFileName2)
    if False == isFileExist:
        writeMethod = 'w'
    else:
        writeMethod = 'a'

    with open(g_profitFileName2, writeMethod, encoding='utf-8') as f:
        writer = csv.writer(f)
        if False == isFileExist:
            writer.writerow(['ts_code', 'date', 'profit'])
        writer.writerow([ts_code, date, profit])
        
def deleteCsvFile(name):
    if True == os.path.isfile(name):
        os.remove(name)
        time.sleep(8)

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

##计算首板的收益
def first_ZT_calculate_profit(_stock_name):
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
####        if ZTprice == _open[i]:  #开盘涨停就跳过
####            continue
##        if ZTprice == _high[i] and ZTPredayPrice > _close[i-1]:  #首板，当天最高价为涨停价，前一天收盘不能为涨停。封板成功和失败的情况都考虑
##        if ZTprice == _high[i] and ZTprice > _close[i]and ZTPredayPrice > _close[i-1]:  #首板，只算没封成功的情况
########        if ZTprice == _close[i] and ZTPredayPrice > _close[i-1]:  #首板，当天最高价为涨停价，前一天收盘不能为涨停。只算封板成功的情况
        if ZTprice == _close[i] and ZTprice == _open[i] and ZTprice > _low[i]:  
            if ZTprice > _close[i]:
                ZTFailCnt = ZTFailCnt+1
##                print (_stock_name,'封板失败',_date[i])
            elif ZTprice == _close[i]:
                ZTSuccessCnt = ZTSuccessCnt+1
##                print (_stock_name,'封板成功',_date[i])              
            open_profit = round(_open[i+1]/ ZTprice - 1,2)
            close_profit= round(_close[i+1]/ ZTprice -1,2)
            
            ave_open_profit = ave_open_profit + open_profit
            ave_close_profit = ave_close_profit + close_profit
##            saveProfitToCsv(_stock_name,_date[i],open_profit)
            saveProfitToCsv(_stock_name,_date[i],close_profit)
      
##计算二板的收益
def second_ZT_calculate_profit(_stock_name):
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
    
    for i in range(3, length-1):
        ZTPre2dayPrice = calculateHighestPrice(_close[i-3])  #涨停前2天的假定涨停价
        ZTPredayPrice = calculateHighestPrice(_close[i-2])  #涨停前一天的假定涨停价
        ZTprice = calculateHighestPrice(_close[i-1])
########        if ZTprice == _open[i]:  #开盘涨停就跳过
########            continue
##        if ZTprice == _high[i] and ZTPredayPrice == _close[i-1] and ZTPre2dayPrice >_close[i-2]:  #二板，当天和前一天最高价为涨停价，前2天收盘不能为涨停。封板成功和失败的情况都考虑
########        if ZTprice == _close[i]  and ZTPredayPrice == _close[i-1] and ZTPre2dayPrice > _close[i-2]:  #二板，当天和前一天最高价为涨停价，前2天收盘不能为涨停。只算封板成功的情况
        if ZTprice == _close[i]  and ZTprice == _open[i] and ZTprice > _low[i] and ZTPredayPrice == _close[i-1]:  #二板，当天和前一天最高价为涨停价，前2天收盘不能为涨停。只算封板成功的情况
            
            if ZTprice > _close[i]:
                ZTFailCnt = ZTFailCnt+1
##                print (_stock_name,'封板失败',_date[i])
            elif ZTprice == _close[i]:
                ZTSuccessCnt = ZTSuccessCnt+1
##                print (_stock_name, '封板成功',_date[i])              
            open_profit = round(_open[i+1]/ ZTprice - 1,2)
            close_profit= round(_close[i+1]/ ZTprice -1,2)

            ave_open_profit = ave_open_profit + open_profit
            ave_close_profit = ave_close_profit + close_profit
            saveProfitToCsv(_stock_name,_date[i],open_profit)
##            saveProfitToCsv(_stock_name,_date[i],close_profit)


##计算三板的收益
def third_ZT_calculate_profit(_stock_name):
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
    
    for i in range(4, length-1):
        ZTPre3dayPrice = calculateHighestPrice(_close[i-4])  #涨停前2天的假定涨停价
        ZTPre2dayPrice = calculateHighestPrice(_close[i-3])  #涨停前2天的假定涨停价
        ZTPredayPrice = calculateHighestPrice(_close[i-2])  #涨停前一天的假定涨停价
        ZTprice = calculateHighestPrice(_close[i-1])
######        if ZTprice == _open[i]:  #开盘涨停就跳过
######            continue
##        if ZTprice == _high[i] and ZTPredayPrice == _close[i-1] and ZTPre2dayPrice >_close[i-2]:  #二板，当天和前一天最高价为涨停价，前2天收盘不能为涨停。封板成功和失败的情况都考虑
##        if ZTprice == _close[i] and ZTPredayPrice == _close[i-1] and ZTPre2dayPrice == _close[i-2]  and ZTPre3dayPrice > _close[i-3]:  #二板，当天和前一天最高价为涨停价，前2天收盘不能为涨停。只算封板成功的情况
############        if ZTprice == _close[i]  and ZTprice == _open[i] and ZTprice > _low[i]  and ZTPredayPrice == _close[i-1] and  ZTPredayPrice == _open[i-1] and  ZTPredayPrice == _low[i-1] \
############           and ZTPre2dayPrice == _close[i-2] and ZTPre2dayPrice == _open[i-2] and ZTPre2dayPrice == _low[i-2]:
        if ZTprice == _close[i]  and ZTprice == _open[i] and ZTprice > _low[i]  and ZTPredayPrice == _close[i-1] and ZTPre2dayPrice == _close[i-2]:
##        if ZTprice == _close[i]  and ZTprice == _open[i] and ZTprice > _low[i]  and ZTPredayPrice == _close[i-1] and ZTPredayPrice == _open[i-1] and ZTPredayPrice > _low[i-1] :            
            if ZTprice > _close[i]:
                ZTFailCnt = ZTFailCnt+1
##                print (_stock_name,'封板失败',_date[i])
            elif ZTprice == _close[i]:
                ZTSuccessCnt = ZTSuccessCnt+1
##                print (_stock_name, '封板成功',_date[i])              
            open_profit = round(_open[i+1]/ ZTprice - 1,2)
            close_profit= round(_close[i+1]/ ZTprice -1,2)

            ave_open_profit = ave_open_profit + open_profit
            ave_close_profit = ave_close_profit + close_profit
            saveProfitToCsv(_stock_name,_date[i],open_profit)
##            saveProfitToCsv(_stock_name,_date[i],close_profit)



g_dirProfit = {}
g_dirStock = {}
def calculateProfit(fileName):
    global g_dirProfit
    global g_totalProfit
    global g_dirStock
##    g_dirProfit = {}
    dirtCount = {}
    if False == os.path.isfile(fileName):
        return;
    with open(fileName, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row['date']
            value = row['profit']
            stock = row['ts_code']
            if date not in g_dirProfit:
                g_dirProfit[date] = float(value)
                dirtCount[date] = 1
                g_dirStock[date] = stock
            else:
                g_dirProfit[date] = g_dirProfit[date] + float(value)
                dirtCount[date] = dirtCount[date] + 1
                g_dirStock[date] = g_dirStock[date] + ',' + stock
    #print(g_dirProfit)
    g_dirProfit = dict(sorted(g_dirProfit.items(), key=lambda d: d[0], reverse=False))
    g_dirStock = dict(sorted(g_dirStock.items(), key=lambda d: d[0], reverse=False))
    g_totalProfit = 1
    for k in g_dirProfit:
        g_dirProfit[k] = round((g_dirProfit[k]) / dirtCount[k], 4)
        g_totalProfit = round(g_totalProfit*(1 + g_dirProfit[k]),4)
##        g_totalProfit = round(g_totalProfit*(1 + (g_dirProfit[k]/100)),4)
    print(g_dirProfit)
    print(g_dirStock)
        

    

def drawProfitPic():
##    print(g_dirProfit)
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
    averageProfit = round(totalProfit / len(y1), 4)
##    plt.title(str(len(y1)) + '天' + '平均收益率: ' + str(averageProfit))
    plt.title(str(len(y1)) + '天' + '平均收益率: ' + str(averageProfit) + ', 总收益: ' + str(g_totalProfit))
##    print(g_dirProfit)
    print (len(y1),'天， 平均收益率: ' ,averageProfit , ', 总收益: ' , g_totalProfit)
    plt.legend()
################    plt.show()

##def drawProfitPic():
##    localtime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
##    print(f'Draw profit picture at {localtime}')
##    print(f'drawProfitPic,  g_dirProfit = {g_dirProfit}')
##    totalProfit = 0
##    averageProfit = 0
##    if 0 == len(g_dirProfit):
##        return;
##
##    x1 = list(g_dirProfit.keys())
##    y1 = list(g_dirProfit.values())
##    plt.plot(x1, y1, label='Frist line', linewidth=3, color='r', marker='o',
##             markerfacecolor='blue', markersize=12)
##    plt.xlabel('日期')
##    plt.ylabel('收益率')
##    for i in range(len(y1)):
##        totalProfit += y1[i]
##    averageProfit = round(totalProfit / len(y1), 2)
##    plt.title(str(len(y1)) + '天' + '平均收益率: ' + str(averageProfit) + ', 总收益: ' + str(g_totalProfit))
##    plt.legend()
##    plt.show()



STOCK_LIST = 'C:/python/zhangting/whitelist.csv'
STOCK_LIST = 'C:/python/csv/oneDayAllStock.csv'
def ZT_profit_all_stock():
    print('开始遍历所有股票')
    print('startDate =',startDate, 'endDate = ',endDate)
    with open(STOCK_LIST, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stock_name = row['ts_code'][:6]
##            if stock_name[:2] == '00' or stock_name[:2] == '60' or stock_name[:2] == '30':
            if stock_name[:2] == '00' or stock_name[:2] == '60':
##                first_ZT_calculate_profit(stock_name)
##                second_ZT_calculate_profit(stock_name)
                third_ZT_calculate_profit(stock_name)
    print('完成遍历所有股票')    



PROFIT_FILE = 'C:/python/zhangting/profit.csv'
def main():
    deleteCsvFile(PROFIT_FILE)
    ZT_profit_all_stock()
    calculateProfit(PROFIT_FILE)
    drawProfitPic()
    
if __name__ == '__main__':
    print('开始请求数据')
    main()
