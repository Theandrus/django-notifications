FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN mkdir /DjangoProject
WORKDIR /DjangoProject
ADD . /DjangoProject/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install mysqlclient
COPY . /DjangoProject/