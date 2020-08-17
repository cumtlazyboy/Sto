import tushare as ts
import pandas as pd
import numpy as np
import csv
import re, time
import string

##queryDate = '20190102'
queryDate = '20200408'
downloadStartDate = '20140101'
downloadEndDate   = '20200430'
downloadStartDate = '20140101'
downloadEndDate   = '20200720'

downloadStartDate = '20200601'
downloadEndDate   = '20200831'

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
startDate = '2010101'
endDate   = '20201231'


##startDate = '20200101'
##endDate   = '20201231'

STOCK_FILE = '601688.csv'   #华泰证券，


EXCHANGE_SHARE = 400
GRID_SET = 0.03  #网格差价
INITIAL_SHARE = 17001  #起始的股份，1000股，底仓


#****************************************************************************
######dwnld_stock_num = '512000'
######dwnld_stock_num = '159915'
######dwnldStartDate = '2018-01-01'
######dwnldEndDate   = '2020-04-06'
######def get_hist_data():
######    print('开始请求数据-start')
######    df = ts.get_hist_data(dwnld_stock_num, start=dwnldStartDate, end=dwnldEndDate)
######    df = df.sort_index(ascending=True)  #升序排列
######    print(df)
######    print('开始请求数据-2')
######    df.to_csv('C:/python/csv/'+dwnld_stock_num+'.csv', columns=['open', 'high','low','close','volume','ma20'])
######    print('开始请求数据-end')

download_stock_num='002746.SZ'
download_stock_num='601166.SH'
def get_hist_data_qfq(_freq):
    print('开始请求数据-start')
    #adj='qfq'前复权
    if _freq == 'D':
        dir_path == 'C:/python/csv/'
    elif _freq == 'W':
        dir_path = 'C:/python/csv_wk/'
    elif _freq == 'M':
        dir_path = 'C:/python/csv_mon/'
    print (dir_path)
    df = ts.pro_bar(ts_code=download_stock_num, adj='qfq', freq = _freq, start_date=downloadStartDate, end_date=downloadEndDate)
    del df['ts_code']
    df = df.sort_values(by='trade_date' , ascending=True)
    print(df)
    df.to_csv(dir_path+download_stock_num[0:6]+'.csv', columns=['trade_date','open', 'high','low','close'])
    
    

def get_k_data():
    each_code = '300333'
    #?????????????????
    df_x = ts.get_k_data(code=each_code, start='2017-03-01')
    print (df_x)
    ma5 = df_x['close'][-5:].mean()
    ma10 = df_x['close'][-10:].mean()
    print (ma5)
    print (ma10)    


#读取某天交易的所有股票信息
def saveOneDayAllCsv():
    print('开始保存所有股票信息......')
    pro = ts.pro_api()
    df = pro.query('daily_basic', ts_code='', trade_date=queryDate,fields='ts_code,pe,pb,total_share,float_share')
######    print(df)
######    ts_code = df['ts_code'][1]
######    print(ts_code)
    df.to_csv('C:/python/csv/oneDayAllStock.csv')
    print('完成保存所有股票信息')


###读取某天交易的所有股票信息
##def getAllStockName():
##    print('开始保存所有股票信息......')
##    stock_string = ''
##    cnt = 0
##    pro = ts.pro_api()
##    df = pro.query('daily_basic', ts_code='', trade_date=queryDate,fields='ts_code,pe,pb,total_share,float_share')
##    ts_code = df['ts_code'][1]
##    print(ts_code)
##    length = len(df['ts_code'])
##    print (length)
####    for i in range(900):
##    for i in range(length):
##        ts_code = df['ts_code'][i]
##        if ts_code[:2] == '60':
##            stock_string = stock_string +'s_sh' + ts_code[:6] + ','
##            cnt = cnt+1
##        elif ts_code[:2] == '00':
##            stock_string = stock_string +'s_sz' + ts_code[:6] + ','
##            cnt = cnt+1
##    stock_string = 'http://hq.sinajs.cn/list=' + stock_string
##    print (cnt)
##    print (stock_string)
##        
####    df.to_csv('C:/python/csv/oneDayAllStock.csv')
##    print('完成保存所有股票信息')
    


##读取某天交易的所有股票信息
def getAllStockName():
    print('开始保存所有股票信息......')
    THREADHOLD = 600
    str_tmp = ''
    stock_string1 = ''
    stock_string2 = ''
    stock_string3 = ''
    stock_string4 = ''
    stock_string5 = ''
    cnt = 0
    pro = ts.pro_api()
    df = pro.query('daily_basic', ts_code='', trade_date=queryDate,fields='ts_code,pe,pb,total_share,float_share')
##    ts_code = df['ts_code'][1]
##    print(ts_code)
    length = len(df['ts_code'])
    print ('length all = ',length)
##    for i in range(900):
    for i in range(length):
        ts_code = df['ts_code'][i]
        if ts_code[:2] == '60':
            str_tmp = str_tmp +'sh' + ts_code[:6] + ','
            cnt = cnt+1
        elif ts_code[:2] == '00':
            str_tmp = str_tmp +'sz' + ts_code[:6] + ','
            cnt = cnt+1
            
        if cnt==THREADHOLD:
            stock_string1 = 'http://hq.sinajs.cn/list=' + str_tmp
            str_tmp = ''
        elif cnt==THREADHOLD*2:
            stock_string2 = 'http://hq.sinajs.cn/list=' + str_tmp
            str_tmp = ''
        elif cnt==THREADHOLD*3:
            stock_string3 = 'http://hq.sinajs.cn/list=' + str_tmp
            str_tmp = ''
        elif cnt==THREADHOLD*4:
            stock_string4 = 'http://hq.sinajs.cn/list=' + str_tmp
            str_tmp = ''
##        elif cnt==THREADHOLD*5:
##            stock_string5 = 'http://hq.sinajs.cn/list=' + str_tmp
##            str_tmp = ''
    stock_string5 = 'http://hq.sinajs.cn/list=' + str_tmp
    print (cnt)
    print (stock_string1)
    print (stock_string2)
    print (stock_string3)
    print (stock_string4)
    print (stock_string5)
##    df.to_csv('C:/python/csv/oneDayAllStock.csv')
    print('完成保存所有股票信息')
    
###########读取某天交易的所有股票信息
##########def getAllStockName():
##########    print('开始保存所有股票信息......')
##########    str_tmp = ''
##########    stock_string = []
##########    cnt = 0
##########    j = 0
##########    pro = ts.pro_api()
##########    df = pro.query('daily_basic', ts_code='', trade_date=queryDate,fields='ts_code,pe,pb,total_share,float_share')
##########    ts_code = df['ts_code'][1]
##########    print(ts_code)
##########    length = len(df['ts_code'])
##########    print (length)
############    for i in range(900):
##########    for i in range(length):
##########        ts_code = df['ts_code'][i]
##########        if ts_code[:2] == '60':
##########            str_tmp = str_tmp +'s_sh' + ts_code[:6] + ','
##########            cnt = cnt+1
##########        elif ts_code[:2] == '00':
##########            str_tmp = str_tmp +'s_sz' + ts_code[:6] + ','
##########            cnt = cnt+1
##########        if cnt>600:
##########            stock_string[j] = 'http://hq.sinajs.cn/list=' + str_tmp
##########            j = j +1
##########            cnt = 0
##########            str_tmp = ''
##########    stock_string = 'http://hq.sinajs.cn/list=' + str_tmp
##########    print (cnt)
##########    print (stock_string)
##########        
############    df.to_csv('C:/python/csv/oneDayAllStock.csv')
##########    print('完成保存所有股票信息')

    
#指定某个日期查询PB
def getPB(_date, _stock_num):
    pro = ts.pro_api()
    df = pro.query('daily_basic', ts_code=_stock_num, trade_date=_date,fields='ts_code,pe,pb,total_share,float_share')
    pb = df['pb'][0]
    return pb


######def getPB():
########    print('查询PB')
######    pro = ts.pro_api()
######    df = pro.query('daily_basic', ts_code='601688.SH', trade_date=queryDate,fields='ts_code,pe,pb,total_share,float_share')
########    time.sleep(1)  #您每分钟最多访问该接口200次.    周线和月线1秒只能下载2次
######    pb = df['pb'][0]
######    return pb
########    print (pb)
########    pb = df.pb
########    print (pb)
########    df.to_csv('C:/python/csv/oneDayAllStock.csv')
########    print('完成查询PB')

    
#从保存的所有股票文件中，把总股本小于5亿的过滤出来，
#并且把每支股票某个时间段内 startDate--endDate 的交易信息各自保存到自己的文件里。
def saveTotalShareBelow5ToEachFile(_freq):
    print('开始保存所有股票的前复权数据......')
    cnt = 0
    if _freq == 'D':
        dir_path = 'C:/python/csv/'
    elif _freq == 'W':
        dir_path = 'C:/python/csv_wk/'
    elif _freq == 'M':
        dir_path = 'C:/python/csv_mon/'
        
    with open('C:/python/csv/oneDayAllStock.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
##            if row['ts_code'][0:2]!= '00' and row['ts_code'][0:2] != '60':  #只下载00和60开头的股票
            if row['ts_code'][0:2] == '30' or row['ts_code'][0:2] == '68':  #只下载00和60开头的股票
                continue
            df = ts.pro_bar(ts_code=row['ts_code'], adj='qfq', freq = _freq, start_date=downloadStartDate, end_date=downloadEndDate)
            df = df.sort_values(by='trade_date' , ascending=True)
            df.to_csv(dir_path +row['ts_code'][0:6]+'.csv', columns=['trade_date','open', 'high','low','close'])
            cnt =cnt +1
            print('完成保存前复权数据     '+dir_path, row['ts_code'][0:6], cnt)
##            time.sleep(3)  #周线和月线1秒只能下载2次
##            if (float(row['total_share']) < 500000000000): #and re.match('300', row['ts_code']):
##                try:
##                    df = ts.get_hist_data(row['ts_code'][:6], start=dwnldStartDate, end=dwnldEndDate)
##                    df = df.sort_index(ascending=True)
##                    df.to_csv('C:/python/csv/'+ row['ts_code'][:6] + '.csv', columns=['open','high','low','close','volume','p_change','ma5','ma20'])
##                except Exception as e:
##                    print(row['ts_code'],end=':')
##                    print(e)
    print('完成保存所有股票的前复权数据     '+dir_path)



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


########STOCK_FILE = '600030.csv'   #中信证券
######STOCK_FILE = '601318.csv'   #中信证券
########STOCK_FILE = '512000.csv'   #券商etf
##DATA_PATH = 'C:/python/csv/'
##
##DATA_PATH = 'C:/python/csv_wk/'
##DATA_PATH_NAME = DATA_PATH + STOCK_FILE

def read_csv_file(_freq, _date,_open,_high,_low,_close,_volume):
    if _freq == 'D':
        dir_path = 'C:/python/csv/'
    elif _freq == 'W':
        dir_path = 'C:/python/csv_wk/'
    elif _freq == 'M':
        dir_path = 'C:/python/csv_mon/'
    DATA_PATH_NAME = dir_path + STOCK_FILE
    print (DATA_PATH_NAME)
    with open(DATA_PATH_NAME,"r",encoding="utf-8") as csvfile:
    #读取csv文件，返回的是迭代类型
        reader = csv.reader(csvfile)
        for row in reader :
            extract_csv_data(row, _date,_open,_high,_low,_close,_volume)




def main():
    _freq = 'D' #下载日线 
##    _freq = 'W' #下载周线
##    _freq = 'M' #下载月线
    ########    get_k_data()   #debuf
##    get_hist_data()  #下载下载etf，基金等品种，如：券商etf 512000
##    get_hist_data_qfq(_freq) #前复权下载某个股票的历史数据，参数为日线，周线，月线
    
    saveOneDayAllCsv()  #只调用一次即可
    saveTotalShareBelow5ToEachFile(_freq) #只调用一次即可，参数为日线，周线，月线
    
    
##    getAllStockName();

if __name__ == '__main__':
    print('开始请求数据')
    main()
