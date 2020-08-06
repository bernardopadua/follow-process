FROM alpine:latest

#Create trivial app folder
RUN mkdir follow-process \
 && mkdir follow-process/followprocess \
 && mkdir follow-process/data \
 && mkdir follow-process/scripts
#--

#Including/Copying main folders
COPY ./requirements/requirements_base_light.txt ./tmp/requirements.txt
ADD manage.py /follow-process
ADD followprocess /follow-process/followprocess
#--

#Mirroing data
VOLUME ["follow-process/data"]
#--

#Installing resources
COPY ./compose/lightdev/entryinstalling/entry.installing.tools.sh ./follow-process/scripts/
COPY ./compose/lightdev/entrypoint/entry.django.sh ./follow-process/scripts/

RUN chmod +x ./follow-process/scripts/entry.installing.tools.sh \
 && chmod +x ./follow-process/scripts/entry.django.sh \
 && ./follow-process/scripts/entry.installing.tools.sh \
 && pip install -r /tmp/requirements.txt
#--

#Running DEV server
EXPOSE 8000
WORKDIR /follow-process

ENTRYPOINT [ "./scripts/entry.django.sh" ]
#--
