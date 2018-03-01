FROM python:3.6

#Adding files
COPY ./requirements/requirements_base.txt ./requirements_base.txt
COPY ./requirements/requirements_prod.txt ./requirements.txt
ADD . /follow-process

COPY ./compose/dev/entrypoint/entry.worker.sh /entry.worker.sh
RUN chmod +x /entry.worker.sh

COPY ./compose/dev/entrypoint/entry.startdjango.sh /entry.gunicorn.sh
RUN chmod +x /entry.gunicorn.sh

#Installing components
RUN pip install -r requirements.txt

WORKDIR /follow-process

EXPOSE 8000