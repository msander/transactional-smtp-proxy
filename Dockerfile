FROM python:3.7-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt && useradd pxy

COPY . .

ENV PYTHONPATH=.

USER pxy
CMD [ "aiosmtpd", "-n", "-c", "proxy.TransactionalHandler", "-l", "0.0.0.0:1025" ]
