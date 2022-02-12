FROM python:3.6.6-alpine3.7

RUN apk add --update \
  build-base libffi-dev openssl-dev \
  xmlsec xmlsec-dev \
  && rm -rf /var/cache/apk/*

ADD requirements.txt /tmp
RUN pip install --upgrade pip==21.1.1
RUN pip install -r /tmp/requirements.txt

EXPOSE 9001
CMD python app.py
