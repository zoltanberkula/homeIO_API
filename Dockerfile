FROM python:3.12

WORKDIR /homeIO_API

COPY requirements.txt .
COPY /.env /.env
COPY /main.py /src/main.py
COPY /modules/errorHandling.py /modules/errorHandling.py
COPY /modules/helpers.py /modules/helpers.py
COPY /modules/utils.py /modules/utils.py
RUN pip install -r requirements.txt

CMD ["python", "/main.py"]

