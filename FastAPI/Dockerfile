FROM python:3.12

COPY ./app /app
COPY ./requirements.txt /app

WORKDIR /app

RUN apt-get update && apt-get upgrade -y && apt-get install -y mariadb-client && pip install mysqlclient

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]
