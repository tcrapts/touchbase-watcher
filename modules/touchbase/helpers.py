import json
import numpy as np
import pandas as pd
import requests
import os

def get_job(filename):
    with open('config/jobs.json') as f:
        jobs = json.load(f)
    job = jobs[filename]
    return job

def get_df(filename): 
    df = pd.read_csv('./../dir/' + filename)
    datetime_columns = df.select_dtypes(include=[np.datetime64]).columns
    for col in datetime_columns:
        df[col] = df[col].dt.strftime('%Y-%m-%d')    
    return df

def push_report(df, job, api_key):
    payload = {
        'table': df.to_json(orient='records'),
        'report_path': job['report_path'],
        'report_name': job['report_name'],
        'id_headers': job['id_headers'] if 'id_headers' in job else [],
        'api_key': api_key
    }
    r = requests.post(os.environ['API_URL'] + 'report/', json=payload)
    print('pushed ' + job['report_name'] +'; status: ' + str(r.status_code))
