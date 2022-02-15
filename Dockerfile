FROM python:3.10-alpine

RUN apk add --update \
  build-base libffi-dev openssl-dev \
  xmlsec xmlsec-dev \
  && rm -rf /var/cache/apk/*

ADD requirements.txt /tmp
RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

EXPOSE 9001
ENV FLASK_ENV development
CMD python app.py
