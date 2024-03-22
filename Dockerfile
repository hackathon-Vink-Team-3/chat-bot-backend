FROM python:3.11

RUN mkdir /vink_chatbot

WORKDIR /vink_chatbot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /vink_chatbot/scripts/*.sh