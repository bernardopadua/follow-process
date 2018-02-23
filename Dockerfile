#docker build -t bernardo/follow-process:1.0

FROM python:3.6
MAINTAINER Bernardo Padua bernactkj@gmail.com

#Setting up the essential components
#RUN curl -sL https://deb.nodesource.com/setup_9.x | bash - && \
#    apt-get update && \
#    apt-get install -y nodejs && \
#    apt-get install -y git && \
#    apt-get install -y build-essential

#Adding files
ADD ./requirements.txt ./requirements.txt
ADD . /follow-process
ADD ./entrypoints ./entrypoints

#Setting up frameworks
RUN pip install -r requirements.txt

RUN chmod +x entrypoints/entry.worker.sh
RUN chmod +x entrypoints/entry.daphne.sh

EXPOSE 8000