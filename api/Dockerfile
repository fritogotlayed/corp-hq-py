# https://github.com/tiangolo/uwsgi-nginx-flask-docker
FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY main.py /app
COPY setup.py /app
COPY requirements.txt /app
COPY ./api /app/api
WORKDIR /app
RUN pip install -e .
