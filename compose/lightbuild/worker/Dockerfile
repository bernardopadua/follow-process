FROM alpine:latest

#Maintaning legacy code.

# LOCAL

#Create trivial app folder
#RUN mkdir follow-process \
# && mkdir follow-process/followprocess \
# && mkdir follow-process/scripts
#--

#Including/Copying main folders
#COPY ./requirements/requirements_base_light.txt ./tmp/requirements.txt
#ADD manage.py /follow-process
#ADD followprocess /follow-process/followprocess
#--

#Installing resources && installing python modules
#COPY ./compose/lightdev/entryinstalling/entry.installing.tools.sh ./follow-process/scripts/
#COPY ./compose/lightdev/entrypoint/entry.django.sh ./follow-process/scripts/

#RUN chmod +x ./follow-process/scripts/entry.installing.tools.sh \
# && cp ./follow-process/scripts/entry.django.sh /tmp/entry.django.sh \
# && chmod +x /tmp/entry.django.sh \
# && ./follow-process/scripts/entry.installing.tools.sh \
# && pip install -r ./tmp/requirements.txt
#--

# ONLINE

#Installing resources ONLINE
RUN wget -O /tmp/entry.installing.tools.sh https://raw.githubusercontent.com/bernardopadua/follow-process/development/compose/lightdev/entryinstalling/entry.installing.tools.sh \
 && chmod +x /tmp/entry.installing.tools.sh \
 && ./tmp/entry.installing.tools.sh

#Creating project from git
RUN git clone --single-branch --branch development https://github.com/bernardopadua/follow-process.git

#Minor steps to complete && installing python modules
RUN chmod +x ./follow-process/compose/lightdev/entrypoint/entry.django.sh \
 && chmod +x ./follow-process/compose/lightdev/entrypoint/entry.worker.sh \
 && pip install -r ./follow-process/requirements/requirements_base.txt
#--

# BOTH

#Running DEV server
WORKDIR /follow-process

ENTRYPOINT [ "./compose/lightdev/entrypoint/entry.worker.sh" ]
#--
