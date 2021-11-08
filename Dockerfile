#FROM python:3.6-alpine AS builder
FROM python:3.6-slim AS builder
ADD requirements.txt .
RUN apt-get update \
  && apt-get -y install libopencv-dev iproute2 iputils-ping
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

# from https://hodalog.com/use-selenium-on-docker/
FROM python:3.6-slim
ENV PYTHONIOENCODING utf-8
ARG PIP_DIR=/usr/local/lib/python3.6/site-packages/
COPY --from=builder ${PIP_DIR} ${PIP_DIR}
WORKDIR /app
RUN apt-get update \
  && apt-get -y install libopencv-dev iproute2 iputils-ping
