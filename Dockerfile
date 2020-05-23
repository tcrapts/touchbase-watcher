FROM python:3.7-slim
RUN python -m pip install watchdog &&\
    pip install pandas &&\
    pip install numpy &&\
    pip install requests
WORKDIR /script
ENTRYPOINT ["python", "-u", "watch.py"]