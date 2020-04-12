# pull official base image
FROM python:3.7.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install wheel
RUN pip install -r requirements.txt
RUN pip install gunicorn

# copy project
COPY . /usr/src/app/
