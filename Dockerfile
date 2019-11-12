FROM python:3.6-jessie
RUN apt-get update; apt-get -y install vim postgresql-client net-tools libev-dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/

RUN useradd -m -d /usr/src/app -s /bin/bash dev
RUN chown -R dev.dev /usr/src/app
USER dev