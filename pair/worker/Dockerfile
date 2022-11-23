FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8


WORKDIR /worker

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
RUN pip install celery

COPY ./ ./


# ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
COPY ./wait /wait
RUN chmod +x /wait

CMD /wait