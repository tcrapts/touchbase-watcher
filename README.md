# Touchbase watcher
A simple, isolated watcher that is suited for pushing data to Touchbase. The goal is to run a Python script every time a file is created or modified.

## Usage
The package manager [poetry](https://github.com/python-poetry/poetry) can be used. When used, prepend every command with `poetry run`, e.g. `poetry run python watcher.py`.

1. When using Poetry (optional): install required packages: `poetry install`. 
2. Create a `config.json` file based on `config.json.example`.
```json
{
    "watch_dir": "./watched_dir",
    "job_dir": "./jobs",
    "jobs": {
        "changeme.csv": "default.py"
    }
}
```
* `watch_dir` is the directory that will be watched
* `job_dir` is the directory where the jobs are located. A job is a Python script, it will get the full path from the modified file as the first argument.
* `jobs` lists the files and correspondings jobs.
3. Start watching: `python watch.py`
