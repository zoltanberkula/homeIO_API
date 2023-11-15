FROM python:3.12

WORKDIR /homeIO_API

COPY requirements.txt .
COPY /.env /.env
COPY /main.py /main.py

RUN pip install -r requirements.txt

CMD ["python", "/main.py"]

