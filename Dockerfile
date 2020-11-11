FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
    && mkdir -p /usr/src \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src
COPY . /usr/src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
