# FROM python:3-alpine
FROM python:3

WORKDIR /flask-app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD python3 init_db.py && python3 main.py