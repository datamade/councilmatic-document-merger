FROM python:3.9-slim

LABEL maintainer "DataMade <info@datamade.us>"

RUN apt-get update && \
    apt-get install -y make libreoffice poppler-utils wget && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app

RUN which unoconv || ( \
    UNOCONV_PATH=/unoconv && \
    wget -P $UNOCONV_PATH https://raw.githubusercontent.com/dagwieers/unoconv/master/unoconv && \
    chmod 755 $UNOCONV_PATH/unoconv && \
    sed -i 's;#!/usr/bin/env python;#!/usr/bin/python3;' $UNOCONV_PATH/unoconv && \
    ln -s $UNOCONV_PATH/unoconv /usr/bin/unoconv \
)

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
