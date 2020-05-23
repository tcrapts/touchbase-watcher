import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os 
import pathlib
import json

# Configure
watch_path = './../dir'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Watcher
def process_file(src_path):
    with open('config/jobs.json') as f: jobs = json.load(f)    
    p = pathlib.Path(src_path)
    relevant_path = '/'.join(str(x) for x in p.parts[2:])
    job_defined = (relevant_path in jobs) and ('job' in jobs[relevant_path])
    if not job_defined: logging.error('No job defined for ' + relevant_path)
    if job_defined:
        job = jobs[relevant_path]['job'] 
        os.system('python -u jobs/' + job + ' ' + relevant_path)

class WatcherEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        logging.info('Created: ' + event.src_path)
        process_file(event.src_path)

    def on_modified(self, event):
        logging.info('Modified: ' + event.src_path)
        process_file(event.src_path)        

if __name__ == "__main__":    
    event_handler = WatcherEventHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
