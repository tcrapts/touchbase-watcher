import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os 
import pathlib
import json

# Configure
with open('config.json') as f: config = json.load(f)    
watch_dir = config['watch_dir']

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Watcher
def process_file(src_path):
    p = pathlib.Path(src_path)
    relevant_path = os.path.basename(src_path)
    job = config['jobs'][relevant_path] if relevant_path in config['jobs'] else None
    if job == None:
        logging.error('No job defined for ' + relevant_path)
    else:
        job = config['jobs'][relevant_path]
        absolute_path = os.path.abspath(src_path)
        logging.info('Starting ' + job)
        os.system('python -u ' + config['job_dir'] + '/' + job + ' ' + absolute_path)

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
    observer.schedule(event_handler, watch_dir, recursive=True)
    logging.info('Watcher started')
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
