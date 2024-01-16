FROM python:slim

RUN useradd -ms /bin/bash pythonando

USER pythonando

ENV PYTHONUNBUFFERED 1

WORKDIR /home/pythonando/app

ENV PATH $PATH:/home/pythonando/.local/bin

COPY . /home/pythonando/app/

#COPY requirements.txt /home/osvaldosdj/app/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

#COPY . /home/osvaldosdj/app/