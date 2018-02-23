#REST FRAMEWORK Core
from rest_framework import viewsets, mixins, generics, permissions, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

#INTERNAL Components
from followprocess.process.tasks import notify_user_process, get_user_processes
from followprocess.process.models import Process, UserProcess
from .serializers import ProcessSerializer
from .permissions import IsOwnerOrReadOnly
from .utils import raise_error_message

class ProcessApiView(viewsets.ModelViewSet):
    lookup_field       = 'pk'
    serializer_class   = ProcessSerializer
    #queryset          = Process.objects.all() get_queryset

    def get_queryset(self):
        query     = Process.objects.all()
        nprocesso = self.request.GET.get('nprocesso')
        dprocesso = self.request.GET.get('dprocesso')

        if nprocesso:
            query = query.filter(numero_processo=nprocesso)
        elif dprocesso:
            query = query.filter(dados_processo__icontains=dprocesso)
        
        return query

    def perform_create(self, serializer):
        user = self.request.user

        pr = serializer.save() #Saving Process
        up = UserProcess(user=user, process=pr) #Attaching process to user
        up.save()
        
        #Notify connected users to app
        notify_user_process.delay(pr.pk)
