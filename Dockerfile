FROM python:3.11-slim

RUN mkdir /vink_chatbot

WORKDIR /vink_chatbot

COPY requirements.txt .

# Для запуска на хостинге
# RUN apt-get update
# RUN apt-get install gcc -y
# RUN apt-get install --reinstall libpq-dev python3-dev -y

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod a+x /vink_chatbot/scripts/*.sh