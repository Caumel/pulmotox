# Python 3.10 image
FROM python:3.10-buster

RUN apt-get update && apt-get upgrade -y

# Install pip requirements.txt
COPY . /pulmotox
WORKDIR /pulmotox
RUN pip install -r requirements.txt

# Add to PATH
ENV PYTHONPATH="/pulmotox:${PYTHONPATH}"