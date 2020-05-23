import sys
import os
sys.path.append('/script/')
import modules.touchbase as tb

# read changed file
filename = sys.argv[1]
print('This is a job for ' + filename)
df = tb.get_df(filename)

# push
api_key = os.environ['API_KEY']
job = tb.get_job(filename)
tb.push_report(df, job, api_key)
