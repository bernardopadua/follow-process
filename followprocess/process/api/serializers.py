#REST FRAMEWORK Core
from rest_framework import serializers

#INTERNAL Components
from followprocess.process.models import Process, UserProcess, RestrictProcess
from .utils import raise_error_message

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Process
        fields = ['pk', 'numero_processo', 'dados_processo']
        read_only_fields = ['pk']

    def validate_numero_processo(self, value):
        query = RestrictProcess.objects.filter(numero_processo=value)
        
        if query.exists():
            msg   = "This 'numero_processo' is restricted."
            error = raise_error_message(msg)
            raise serializers.ValidationError(error)
        
        return value
