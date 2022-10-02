FROM python:3-alpine

WORKDIR /flask-app

COPY . .

CMD sh start.sh