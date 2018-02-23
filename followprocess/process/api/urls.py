#DJANGO Core
from django.urls import re_path, include

#REST FRAMEWORK Core
from rest_framework import routers

#INTERNAL Components
from followprocess.process.api import views as api_views

router = routers.DefaultRouter()
router.register(r"process", api_views.ProcessApiView, base_name="process")

urlpatterns = [
    re_path(r"v1/", include(router.urls)),
]