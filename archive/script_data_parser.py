# script_data_parser.py

import datetime
import re 
import json 
import pandas as pd

# read indicator name from args 
# indicatorName = args[0] if len(args) > 0 else exit # default indicator name

raw_data = ""
dataDict = {}

indicatorName = "fdema" # change this to your indicator name
# read fdema.ws file
with open(f"{indicatorName}.ws", "r") as f:
    raw_data = f.read()


# Format Raw data 
raw_data = re.sub(r"\\\"", '', raw_data) # removes \" from string 
raw_data = re.sub(r"\\", '', raw_data) # removes \ from string 
raw_data = re.sub(r"~m~(.+?)~m~", ',', raw_data) #  ~m--m~ from string 
raw_data = "["+raw_data[1:]+"]" # remove the first comma and append to a list [] 
dataDict = json.loads(raw_data)

#  eleement with 'm': 'du', 'p': [....] contains the data we need
dataElement = list(filter(lambda x : x.get('m', '') == 'du', dataDict))
# extract st from this data  where st5 is dynamic
st_key = list(filter(lambda x : x.startswith('st'), dataElement[0]['p'][1].keys()))[0]
ts = dataElement[0]['p'][1][st_key]['st'] # ohlc array   
# Time series : 
t = list(map(lambda x : x['v'], ts))
df = pd.DataFrame(t)
df['datetime'] = pd.to_datetime(df[0], unit='s')
df['datetime'] = df['datetime'].dt.date
drop_cols = [0] # drop the first column which is timestamp
df.drop(columns=drop_cols, inplace=True)
df.set_index('datetime', inplace=True)
# enumerate columns names as A, B, C, D ... depending on number of columns
df.columns = [chr(i) for i in range(65, 65 + df.shape[1])]


# # ask user for column names one by one 
# col_names = []
# for i in range(df.shape[1]):
#     col_name = input(f"Enter name for column {chr(65 + i)} (default: col_{i+1}): ")
#     if not col_name.strip():
#         col_name = f"col_{i+1}"
#     col_names.append(col_name)
# df.columns = col_names


print(df)

# SAVE DATA TO CSV
df.to_csv(f"{indicatorName}.csv")



# df = None 
# for item in dataDict : 
#     try : 
#         ts = item ['p'][1]['sds_1']['s'] # ohlc array 
        
#         # Time series : ohlcv 
#         t = list(map(lambda x : x['v'], ts))
#         has_volume = len(t[0]) == 6
#         t_col = ["datetime", "open", "high", "low", "close", "volume"] if has_volume else ["datetime", "open", "high", "low", "close"]  # NO VOLUME DATA CASE HANDLING
        
#         df = pd.DataFrame(t, columns=t_col)
#         df['datetime'] = pd.to_datetime(df['datetime'], unit='s')
#         # keep only date part
#         df['datetime'] = df['datetime'].dt.date
#         df = df.set_index('datetime')             
#         if not has_volume :  df["volume"] = 0.0 # NO VOLUME DATA CASE HANDLING                    
#     except : pass 

# df  # final dataframe - OHLCV 
