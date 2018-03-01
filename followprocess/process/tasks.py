#CELERY Core
from celery import shared_task
from django.core import serializers
from django.contrib.auth.models import User
from django.db import Error, IntegrityError

#CHANNELS Components
from channels.layers import get_channel_layer
from asgiref.sync import AsyncToSync

#PYTHON Components
import json
import time
import logging

#INTERNAL Models
from followprocess.process.models import Process, UserProcess, UserAdditional, RestrictProcess

#DJANGO logging instance
logger = logging.getLogger(__name__)

@shared_task
def get_user_processes(puser):
    user      = User.objects.get(pk=puser)
    processes = UserProcess.objects.filter(user=user)
    processes = [d.process for d in processes]

    if len(processes) == 0:
        processes = list()

    result = {
        "type": "process.respond",
        "processes": serializers.serialize('json', processes)
    }
    
    # Channel back to Consumer
    channel = get_channel_layer()
    AsyncToSync(channel.group_send)(
        user.username,
        result
    )

@shared_task
def create_process(puser, nprocesso, dprocesso):
    user = User.objects.get(pk=puser)
    rp   = RestrictProcess.objects.filter(numero_processo=nprocesso)

    if rp.exists():
        notify_user_error.delay(puser, "This numero_processo is restricted!")

    try:
        pr = Process(numero_processo=nprocesso, dados_processo=dprocesso)
        pr.save()

        up = UserProcess(user=user, process=pr)
        up.save()
    except IntegrityError as e:
        notify_user_error.delay(puser, "The 'numero_processo' typed is already been in use.")
    except Error as e:
        logger.error(str(e))

    get_user_processes.delay(puser)

@shared_task
def change_process(nprocesso, dprocesso):
    up = UserProcess.objects.filter(pk=nprocesso)
    pr = Process.objects.get(pk=nprocesso)
    
    try:
        pr.change_dados(dprocesso)

        if len(up) > 1:
            for us in up:
                get_user_processes.delay(us.pk)
        else:
            get_user_processes.delay(up[0].pk)
    except Error as e:
        logger.error(str(e))

@shared_task
def delete_process(puser, nprocesso):
    pr = Process.objects.get(pk=nprocesso)
    
    try:
        pr.delete()
        get_user_processes.delay(puser)
    except Error as e:
        logger.error(str(e))

@shared_task
def notify_user_process(process_pk, user=None):
    pr  = Process.objects.get(pk=process_pk)
    prs = UserProcess.objects.filter(process=pr)

    for p in prs:
        us = p.user
        get_user_processes.delay(us.pk)

@shared_task
def notify_user_error(puser, msg):
    user      = User.objects.get(pk=puser)
    result = {
        "type": "user.error",
        "error": msg
    }
    
    # Channel back to Consumer
    channel = get_channel_layer()
    AsyncToSync(channel.group_send)(
        user.username,
        result
    )