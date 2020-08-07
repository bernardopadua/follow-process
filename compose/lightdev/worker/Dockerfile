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
RUN wget -O /tmp/entry.installing.tools.sh https://gist.githubusercontent.com/bernardopadua/66b917b558a566873070db02ab2bf76e/raw/c9bcb77bd3eefa157d4f3baa996d1a60393aede4/entry.installing.sh \
 && chmod +x /tmp/entry.installing.tools.sh \
 && ./tmp/entry.installing.tools.sh

#Creating project from git
RUN git clone --single-branch --branch development https://github.com/bernardopadua/follow-process.git

#Minor steps to complete && installing python modules
RUN wget -O /tmp/entry.django.sh https://gist.githubusercontent.com/bernardopadua/479208f7e0b11fa86180ffd90d005618/raw/22ef580aa3fb836b2e4bc647f1572f14e1ba1cf3/entry.django.sh \
 && chmod +x /tmp/entry.django.sh \
 && wget -O /tmp/entry.worker.sh https://gist.githubusercontent.com/bernardopadua/ed69d8003712ba334ef2a104168df074/raw/12bb79e5332bbeb1fbadc824b3e573fe25584545/entry.worker.sh \
 && chmod +x /tmp/entry.worker.sh \
 && pip install -r ./follow-process/requirements/requirements_base.txt
#--

# BOTH

#Running DEV server
EXPOSE 8000
WORKDIR /follow-process

ENTRYPOINT [ "/tmp/entry.worker.sh" ]
#--
