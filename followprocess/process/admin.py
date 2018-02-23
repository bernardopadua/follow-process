from django.contrib import admin
from .models import Process, UserProcess, UserAdditional, RestrictProcess

admin.site.register(Process)
admin.site.register(UserProcess)
admin.site.register(UserAdditional)
admin.site.register(RestrictProcess)