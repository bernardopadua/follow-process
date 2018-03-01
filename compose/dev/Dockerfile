FROM python:3.6

#Adding files
COPY ./requirements/requirements_base.txt ./requirements.txt
ADD . /follow-process

COPY ./compose/dev/entrypoint/entry.worker.sh /entry.worker.sh
RUN chmod +x /entry.worker.sh

COPY ./compose/dev/entrypoint/entry.startdjango.sh /entry.startdjango.sh
RUN chmod +x /entry.startdjango.sh

#Installing components
RUN pip install -r requirements.txt

WORKDIR /follow-process

EXPOSE 8000