#REST FRAMEWORK Core
from rest_framework import permissions

#INTERNAL Components
from followprocess.process.models import UserProcess

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        User only can update or delete your own Process.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        #Check if the user owns the process.
        up = UserProcess.objects.filter(user=request.user, process=obj)
        if up.exists():
            return True

        return False