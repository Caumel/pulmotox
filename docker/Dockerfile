# Python 3.10 image
FROM python:3.10-buster

# Install pip requirements.txt
COPY . /pulmotox
WORKDIR /pulmotox

RUN apt-get update && apt-get upgrade -y

RUN pip install -r requirements.txt

# Add to PATH
ENV PYTHONPATH="/pulmotox:${PYTHONPATH}"