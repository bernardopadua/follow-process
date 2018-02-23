#DJANGO Core
from django.contrib.auth.models import User
from django.db import models

#PYTHON Components
import hashlib
import datetime

class Process(models.Model):

    numero_processo = models.CharField(max_length=20, null=False, unique=True)
    dados_processo  = models.TextField(max_length=2000)

    class Meta:
        verbose_name        = ("Process")
        verbose_name_plural = ("Processes")
        ordering            = ("-numero_processo",)

    def __str__(self):
        return self.numero_processo

    def change_dados(self, pdados):
        self.dados_processo = pdados
        self.save()


class UserProcess(models.Model):
    
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    process    = models.ForeignKey(Process, on_delete=models.CASCADE)

    class Meta:
        verbose_name        = ('UserProcess')
        verbose_name_plural = ('UserProcesses')
        unique_together     = ('user', 'process',)

class RestrictProcess(models.Model):
    
    numero_processo = models.CharField(max_length=20, null=False, unique=True)

    class Meta:
        verbose_name        = ('RestrictProcess')
        verbose_name_plural = ('RestrictProcesses')

class UserAdditional(models.Model):

    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #TODO Future implementation
    last_check  = models.DateTimeField(auto_now_add=True)
    accesstoken = models.CharField(max_length=255) 

    class Meta:
        verbose_name        = ('UserAdditional')
        verbose_name_plural = ('UserAdditionals')

    def addtoken(self):
        now   = datetime.datetime.now()
        token = '{}{}'.format(self.user.username,now).encode('utf8')
        token = hashlib.sha1(token).hexdigest()
        self.accesstoken = token

    def getoken(self):
        return self.accesstoken
     
    def refresh_lastcheck(self):
        self.last_check = datetime.datetime.now()
        self.save()

    @staticmethod
    def getuser(token):
        return UserAdditional.objects.get(accesstoken=token)
