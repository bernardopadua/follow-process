#DJANGO Core
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.models import User

#INTERNAL Components
from followprocess.process.models import Process, UserAdditional

#PYTHON Components
import json

def http_res_json(json, stcode):
    res = HttpResponse(json, content_type='application/json', status=stcode)
    res['Access-Control-Allow-Origin'] = '*'
    return res

@login_required
def home_app(req):

    up = UserAdditional.objects.filter(user=req.user)
    if len(up) == 0:
        up = UserAdditional(user=req.user)
    else:
        up = up[0]

    response = None

    try:
        up.addtoken()
        up.save()
        response = render(
            req, 
            'process/test_channels.html', 
            {
                "token": up.getoken()
            }
        )
    except Exception as e:
        response = HttpResponseBadRequest(str(e))

    return response