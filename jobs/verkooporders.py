import os, sys, inspect, json, pandas as pd
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import modules.touchbase as tb

# read changed file
filename = sys.argv[1]

# transform
# read json
with open('config/global.json') as f: config = json.load(f)    
watch_path = config['watched_folders'][0]
full_path = watch_path + '/' + filename
with open(full_path, encoding="utf8") as f:
    json_data = json.load(f)
# json to Pandas DataFrame
df_vorh = pd.DataFrame(json_data['ProDataSet']['vorh'])

# select columns
# columns = ['RowKey', 'vorh_num', 'vorh_dat_order', 'debi_num.debi_naam', 'verk_num.verk_naam']
columns = ['vorh_num', 'vorh_dat_order', 'debi_num.debi_naam', 'verk_num.verk_naam']
df_vorh = df_vorh[columns]

# convert to datetime
columns = ['vorh_dat_order']
for col in columns:
    df_vorh[col] =  pd.to_datetime(df_vorh[col])

# rename columns
column_dict = {'vorh_num': 'Verkooporder', 'vorh_dat_order': 'Orderdatum', 
               'debi_num.debi_naam': 'Debiteur - Bedrijfsnaam', 'verk_num.verk_naam': 'Verkoper'}
df_vorh.rename(columns=column_dict, inplace=True)
df_vorh = tb.stringify_datetime_columns(df_vorh)

# push
with open('config/api_key.json') as f:
    api_key = json.load(f)['default']
job = tb.get_job(filename)
tb.push_report(df_vorh, job, api_key)