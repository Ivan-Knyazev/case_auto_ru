FROM python:3-alpine

WORKDIR /flask-app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD python3 init_db.py && python3 main.py