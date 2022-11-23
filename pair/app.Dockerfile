FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8


WORKDIR /app

COPY requirements.txt ./requirements.txt


RUN pip install -r requirements.txt 
RUN pip install pyyaml


COPY ./ ./

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

# CMD /wait
CMD ["uvicorn", "main:app"]