
%load_ext autoreload
%autoreload 2

from tvDatafeed import tvData, Interval

# username = 'eagerdarwin@gmail.com'
# password = '$k jh34KUSjfsfs^^_Rwsdgvs'
# tv = tvData (username, password) # works 
# tv = tvData (username, password, "eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjo4Mjc5NTkxNiwiZXhwIjoxNzI1MDA2MzM1LCJpYXQiOjE3MjQ5OTE5MzUsInBsYW4iOiIiLCJleHRfaG91cnMiOjEsInBlcm0iOiIiLCJzdHVkeV9wZXJtIjoiIiwibWF4X3N0dWRpZXMiOjIsIm1heF9mdW5kYW1lbnRhbHMiOjEsIm1heF9jaGFydHMiOjEsIm1heF9hY3RpdmVfYWxlcnRzIjoxLCJtYXhfc3R1ZHlfb25fc3R1ZHkiOjEsImZpZWxkc19wZXJtaXNzaW9ucyI6W10sIm1heF9vdmVyYWxsX2FsZXJ0cyI6MjAwMCwibWF4X2FjdGl2ZV9wcmltaXRpdmVfYWxlcnRzIjo1LCJtYXhfYWN0aXZlX2NvbXBsZXhfYWxlcnRzIjoxLCJtYXhfY29ubmVjdGlvbnMiOjJ9.r-qOih_o-X9en3KrOYp9cD1wCxa2qinT_W5j0_p4DIGUVOxIkRBISvl6mWeYaJMqBsh0WTp4HH01WSiUEhYDk-gkuFsVLkwTnLYSGDOP-WKMpIPxE6UFWld50q-vKeZ4wPOYhP-fz0tjfExqNfg-9lIIA-KAqvor0Kw7vSFrGAk") # works 

tv = tvData () # nologin method, data you access may be limited

# most simple 1D Data - returns a pandas dataframe 

timeseries_DF = tv.get_timeseries('SPY','', interval=Interval.in_daily, n_bars=8000)

# ? Get Raw data - using flag `debug`
raw_data_debug = tv.get_timeseries('AAPL','NASDAQ', interval=Interval.in_daily, n_bars=8000, debug=True)



# 22 quarters and 10 fiscal years 
(revenueQ, earningsQ, revenueFY, earningsFY), financial_fullDict = tv.get_financials('KLAC','NASDAQ')
(revenueQ, earningsQ, revenueFY, earningsFY), financial_fullDict, myhtml = tv.get_financials('AMD','NASDAQ', html=True)

len(financial_fullDict.keys()) # 1254 - 1290 keys  - check 
financial_fullDict ['short_name'] # 'AAPL'


# ------------------------- END KEY FUNCITONS ---------------------------------# 

# ? --------------------- Earnings / Dividends/  RAW ---------------------- ? # 

tv = tvData()
# tm = tv.get_timeseries('AAPL','', interval=Interval.in_daily, n_bars=8000)

raw_data = tv.get_timeseries_earnings_dividends('AAPL','', interval=Interval.in_daily, n_bars=8000,debug=True)

ts, ern, div = tv.get_timeseries_earnings_dividends('AAPL','', interval=Interval.in_daily, n_bars=8000)

ts, ern, div = tv.get_timeseries_earnings_dividends('HNRG','', interval=Interval.in_daily, n_bars=8000,)
ts, ern, div = tv.get_timeseries_earnings_dividends('AVGO','', interval=Interval.in_daily, n_bars=8000,)

ern.to_csv('t.csv')
div.to_csv('t.csv')


import re 
import json 
raw_data = re.sub(r"\\\"", '', raw_data) # removes \" from string 
raw_data = re.sub(r"\\", '', raw_data) # removes \ from string 
raw_data = re.sub(r"~m~(.+?)~m~", ',', raw_data) #  ~m--m~ from string 
raw_data = "["+raw_data[1:]+"]" # remove the first comma and append to a list [] 
dataDict = json.loads(raw_data)

# identify : timeseries, dividend series, earnings series 
for item in dataDict : 
    try : ts = item ['p'][1]['sds_1']['s'] # ohlc array 
    except : pass 
    try: div = item['p'][1]['st2']["st"] # dividend array
    except : pass 
    try: ern = item ['p'][1]['st1']['st'] # earnings array 
    except: pass

# Time series : ohlcv 
t = list(map(lambda x : x['v'], ts))
t_col = ["datetime", "open", "high", "low", "close", "volume"]
import pandas as pd 
df = pd.DataFrame(t, columns=t_col)
df['datetime'] = pd.to_datetime(df['datetime'], unit='s')
df = df.set_index('datetime')


# Time series : earnings/ eps/ rev / dates  
e = list(map(lambda x : x['v'], ern))
t_col = ["datetime", "eps_std", "eps_est", "qy", "date", "eps_act", "rev_est_M", "rev_act_M", "sl"]
import pandas as pd 
e_df = pd.DataFrame(e, columns=t_col)
e_df['datetime'] = pd.to_datetime(e_df['datetime'], unit='s')
e_df['qy'] = pd.to_datetime(e_df['qy'], unit='s')
e_df['date'] = pd.to_datetime(e_df['date'], unit='ms')
e_df = e_df.set_index('datetime')
e_df.loc['2004']

# Time series : dividend 
d = list(map(lambda x : x['v'], div))
t_col = ["xdate", "divamt", "ex_date", "dd", "pay_date" ]
import pandas as pd 
d_df = pd.DataFrame(d, columns=t_col)
#  [1699626600.0, 0.239999995, 1699574400000.0, 1e+100, 1700092800000.0]
d_df['xdate'] = pd.to_datetime(d_df['xdate'], unit='s')
d_df['ex_date'] = pd.to_datetime(d_df['ex_date'], unit='ms')
d_df['pay_date'] = pd.to_datetime(d_df['pay_date'], unit='ms')
d_df = d_df.set_index('xdate')
d_df.loc['2015']



div
ern
        
# dividend 
dataDict[7]['m'] # 'du' 
dataDict[7]['p'][0]  
dataDict[7]['p'][1]['st2']['t']
dataDict[7]['p'][1]['st2'].keys()
dataDict[7]['p'][1]['st2']["st"][0]['v']
dataDict[7]['p'][1]['st2']["st"]  # dividend array 

# ohlcv 
dataDict[5]['m']
dataDict[5]['p'][1]['sds_1'].keys()
dataDict[5].keys()
dataDict[5]['p'][1]['sds_1']['t']
dataDict[5]['p'][1]['sds_1']['s'] # ohlc array 

# earnings 
dataDict[9]['m'] # 'timescale_update'
dataDict[9]['p'][0] # chart id 
dataDict[9]['p'][1]['st1'].keys()
dataDict[9]['p'][1]['st1']['st'] # earnings array 
dataDict[9]['p'][1]['st1']['node']
dataDict[9]['p'][1]['sds_1'].keys()



# # ohlc format 
# {"m":"timescale_update",
# {"node":"nje1-30-series-charts-free-2-runner-2","s":
# "v":[1687440600.0,183.74,187.045,183.67,187.0,51245327.0]  [t, open, high, low, close, volume ]

# # Dividend Format 
# {"m":"du",
# {"st2":{"node":"nje1-30-studies-charts-free-2-runner-3","st":
# "v":[547738200.0,0.119999997,547689600000.0,0.000535714295357142,550713600000.0] [ex-date, div amt, dataNA, pay-date ]

# # Earnings Format 
# {"m":"timescale_update",
# "st1":{"node":"nje1-30-studies-charts-free-2-runner-1","st":
# "v":[1722519000.0,1.3974,1.344647,1719705600.0,1722470400000.0,1.4,84432.539529,85777.0,22.0] 
# date-time, eps_std, eps_est, period-ending(QY) , date, eps_reported, revenue_est(M), revenue_reported (M), NA
# "v":[772205400.0,0.0104,1e+100,765072000.0,772156800000.0,1e+100,1e+100,1e+100,23.0]




# ? --------------------- FINANCIALS RAW ---------------------- ? # 

# ? Get Raw data - using flag `debug`
d_raw_data = tv.get_financials('AAPL','', debug=True)
raw_data = d_raw_data

d_raw_data = raw_data = tv.get_financials('AAPL','NASDAQ', debug=True)

raw_data = d_raw_data

import re 
import json 
raw_data = re.sub(r"\\\"", '', raw_data) # removes \" from string 
raw_data = re.sub(r"\\", '', raw_data) # removes \ from string 
raw_data = re.sub(r"~m~(.+?)~m~", ',', raw_data) #  ~m--m~ from string 
raw_data = "["+raw_data[1:]+"]" # remove the first comma and append to a list [] 
dataDict = json.loads(raw_data)

# len(dataDict)


# ? --------------------- EXPLORING DICT ---------------------- ? # 

dailybar = {'close': '226.05', 'data-update-time': '1723853985.275493', 'high': '226.8271', 'low': '223.6501', 'open': '223.92', 'time': '1723766400', 'update-time': '1723852796.831432', 'volume': '44340240'}
pd.DataFrame (dailybar, )

len(dataDict) # 5 
l = dataDict[1]

dataDict[0] # session id 
dataDict[1]['p'][0] # session id 
dataDict[1]['p'][1] # value
dataDict[2]['p'][0]
dataDict[2]['p'][1]['v'] # dict value
dataDict[3]['p'][1]['v'] # dict value 
dataDict[4]['p'][1] # value 

dataDict[0]

{**dataDict[0], **dataDict[1], **dataDict[4],}

dataDict[2]['p'][1]['v'] ['short_name'] # dict value
dataDict[2]['p'][1]['v'] ['original_name'] # dict value
dataDict[2]['p'][1]['v'] ['pro_name'] # dict value

# ? ---------------- SANITIZE CONSOLIDATE DICT ---------------- ? # 

header = {}
merged = {} 
for toplevelItem in dataDict : 
    # print (item)
    # merged.update ( {k: v for k, v in item.items() if v})
    try : merged = {**merged, **toplevelItem['p'][1]['v']} # merge 2 dicts - will overwrite if same key 
    except: pass 
    try : header = {**header, **toplevelItem}
    except: pass 

len(header.keys()) , header.keys()  # count 11
len(merged.keys()) , merged.keys()  # count 1254 

merged['short_name']  # AAPL 
pd.DataFrame(merged["revenues_fq_h"])
pd.DataFrame(merged["revenue_seg_by_region_h"])
pd.DataFrame(merged["daily-bar"], index=[0]).to_html()



merged["source2"]
merged["symbol"]
merged["short_name"]
merged["pro_name"]
merged["original_name"]
merged["beta_5_year"] # beta_1_year beta_3_year
merged["enterprise_value_current"]

# 6 key dfs 
merged["revenues_fq_h"] # 31 QYs : 22 QY past + 9 QY forecast QY
merged["earnings_fq_h"] # 31 QYs : 22 QY past + 9 QY forecast QY 
merged["revenues_fy_h"] # 14 yrs : 9 past + 5 forecast years 
merged["earnings_fy_h"] # 14 yrs : 9 past + 5 forecast years 
merged["revenue_seg_by_region_h"]
merged["revenue_seg_by_business_h"]

# time periods FY and FQ 
merged["earnings_fiscal_period_fy_h"] # timeperiod : 8 FY years 
merged["earnings_fiscal_period_fq_h"] # timeperiod : 8 QY
merged["fiscal_period_fy_h"]  # 8years
merged["gross_profit_fy_h"]  # 8 FY years 
merged["dividend_payout_ratio_fy_h"]
merged["total_extra_items_fy_h"]
merged["revenue_fq_h"] # 8 Q
merged["revenue_fq"] 
merged["revenue_fy_h"] # 8 Y 
merged["revenue_fy"]
merged["market_cap_basic_fy_h"] # 8 Q 


merged["fiscal_period_fq_h"]  # 11 quarters
merged["market_cap_basic_fq_h"] # 11 Q 
merged["accounts_receivables_net_fq_h"] # 11 quarters 
merged["total_equity_fq_h"] # 11 quarters 
merged["pre_tax_margin_fq_h"] # 11 quarters 

merged["dividend_record_date_h"]
merged["earnings_release_date_h"]
merged["short_description"]
merged["rates_earnings_next_fq"]
merged["rates_earnings_fq"]

merged["subsessions"]

# Get all the possible dataframes in dataDict 
for k in merged.keys() : 
    if type(merged[k]) == list : # dict :  # list 
        if type (merged[k][0]) == dict : 
            print (k) # dataframes dict 


# Get all the dicts 
for k in merged.keys() : 
    if type(merged[k]) == dict : # dict :  # list 
        print (k)



## ------------ Original method -------------- ## 

import json 

out = re.search('"earnings_fq_h":\[(.+?)\]', raw_data).group(1)

dfdata = pd.read_json (out, lines=True)


import re
import pandas as pd
# def create_revenue_qy_df(raw_data):
#     try:
#         out = re.search('"revenues_fq_h":\[(.+?)\}\]', raw_data).group(1)
#         # x = out.split(',{"')
#         data = list(out)
        
#         print (out)
        
#         # data = pd.DataFrame( out ) 
#         return data
#     except AttributeError:
#         pass

# a, b, c = tv.create_financial_df(raw_data)

# # check json 

# revenues_fq_h 
# earnings_fq_h
# revenues_fy_h

# 22 quarters and 10 fiscal years 
revenueQ, earningsQ, revenueFiscal = tv.get_financials('MU','NASDAQ', interval=Interval.in_daily, n_bars=500)
# raw_data = 

raw_data = tv.get_financials('MU','NASDAQ', interval=Interval.in_daily, n_bars=500, debug=True)

out = re.search('"changes":\[(.+?)\]', raw_data).group(1)

dfdata = pd.read_json (out, lines=True)



# ------------------------- JSON to HTML CONVERSION  ------------------------------ # 
# ? Method #1 - not so great with json2HTML 
from json2html import *
htmldata = json2html.convert(json = raw_data)
with open ('socket.data.html', 'w') as f : 
    f.write (htmldata)

# ? Method #2 - custom to this JSON data type  
# HTML conversion - manual 
htmlText = ""
count = 0 
for toplevelItem in dataDict : 
    # print (toplevelItem)
    try : 
        dd = toplevelItem['p'][1]['v'] # a dict         
        for item in dd : 
            if type (dd[item]) == dict : 
                try: 
                    print (item, dd[item])
                    htmlText += "<strong>" + item + "</strong>"
                    count +=1 
                    # table = pd.DataFrame(dd[item]).to_html()   
                    df = pd.DataFrame(dd[item], index=[0]) # scalar dict data 
                    htmlText += df.to_html()
                    print ("table added")
                except : 
                    print ("exception #1 ! ") ; pass
            elif type (dd[item]) == list : 
                # print (item, dd[item])
                if type (dd[item][0]) == dict : 
                    htmlText += "<strong>" + item + "</strong>"
                    count +=1 
                    try: 
                        # ? KEY financial data is here 
                        htmlText += pd.DataFrame(dd[item]).to_html() # 2D dict data 
                        print (item, "2D table added")
                    except: print ("exception #2 ! "); pass
                else : 
                    # print (item, dd[item])
                    try: 
                        htmlText += "<strong>" + item + "</strong>" + "<table border='1'><tr>"
                        count +=1                         
                        for i in dd[item] :                             
                            htmlText += "<td>" + str(i) + "</td>"
                        htmlText += "</tr></table>"
                        print (item, "1D row added")
                    except: print ("exception #3 ! "); pass
            else: 
                try: 
                    htmlText += "<strong>" + item + "</strong> :    " + str(dd[item]) + "</br>"
                    count += 1
                except: print ("exception #4 ! "); pass
    except: 
        pass
    
print ("HTML Tables added: ", count)
with open ('dataTable.html', 'w') as f : 
    f.write (htmlText)
    
# ------------------------- END HTML CONVERSION  -------------------------------- # 
