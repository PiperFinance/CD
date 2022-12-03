FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8


WORKDIR /app

COPY requirements.txt ./requirements.txt


RUN pip install -r requirements.txt 
RUN pip install pyyaml


COPY ./ ./

# ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
COPY ./wait /wait
RUN chmod +x /wait

# CMD /wait
# ENV PORT=8800
# RUN echo  ${PORT}
# CMD ["uvicorn", "main:app" ,"--host","0.0.0.0" , "--port", ${PORT}]