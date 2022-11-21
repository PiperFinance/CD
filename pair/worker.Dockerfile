FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8


WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
RUN pip install celery

COPY ./ ./
# HEALTHCHECK CMD celery inspect ping -A AggV3 -d celery@$HOSTNAME
RUN chmod +x ./worker-start.sh 


## Wait for other services to Open Thier TCP Connection
# Env is WAIT_HOSTS
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait


CMD /wait

