import os, sys, inspect, json
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import modules.touchbase as tb

# read changed file
filename = sys.argv[1]
df = tb.get_df(filename)

# push
with open('config/api_key.json') as f:
    api_key = json.load(f)['default']
job = tb.get_job(filename)
tb.push_report(df, job, api_key)