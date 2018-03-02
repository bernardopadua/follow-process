#REST FRAMEWORK Core
from rest_framework import viewsets, mixins, generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

#INTERNAL Components
from followprocess.process.tasks import notify_user_process, get_user_processes
from followprocess.process.models import Process, UserProcess
from .serializers import ProcessSerializer, UserProcessSerializer
from .permissions import IsOwnerOrReadOnly
from .utils import raise_error_message
from .exceptions import UserNotAuthorized

class UserProcessApiView(
        mixins.DestroyModelMixin, 
        mixins.CreateModelMixin, 
        generics.ListAPIView
    ):
    lookup_field       = 'pk'
    serializer_class   = UserProcessSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        query = None

        if self.request.user.is_staff:
            query     = UserProcess.objects.all()
            nprocesso = self.request.GET.get('nprocesso')

            if nprocesso:
                pr = Process.objects.get(numero_processo=nprocesso)
                query = query.filter(process=pr)
            #TODO Error trying to access this key.
            #elif self.kwargs["pk"] is not None:
            #    query = query.filter(pk=self.kwargs["pk"])

        else:
            query = UserProcess.objects.none()
        
        return query

    def perform_create(self, serializer):
        try:
            up = serializer.save(user=self.request.user)
        
            #Notify connected users to app
            notify_user_process.delay(up.process.pk)
        except:
            msg   = "The process is already attached to your user"
            error = raise_error_message(msg)
            raise ValidationError(error)

    def perform_destroy(self, serializer):
        try:
            up = self.get_object()
            if up.user == self.request.user:
                serializer.delete()
                #Notify connected users to app
                get_user_processes.delay(self.request.user.pk)
            else:
                msg   = "You can delete only attachment of a process you own."
                error = raise_error_message(msg)
                raise ValidationError(error)
        except:
            msg   = "Can't delete this attachment between User and Process."
            error = raise_error_message(msg)
            raise UserNotAuthorized(error)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ProcessApiView(viewsets.ModelViewSet):
    lookup_field       = 'pk'
    serializer_class   = ProcessSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
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
