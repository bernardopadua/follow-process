#DJANGO Core
from django.urls import re_path, include

#REST FRAMEWORK Core
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

#INTERNAL Components
from followprocess.process.api import views as api_views

router = routers.DefaultRouter()
router.register(r"process", api_views.ProcessApiView, basename="process")

userprocess = api_views.UserProcessApiView.as_view()

urlpatterns = [
    re_path(r"v1/", include(router.urls)),
    #TODO Implement it in the API Root. Tip: Extends > BaseRouter() 
    re_path(r"v1/user_process/$", userprocess, name="user_process"),
    re_path(r"v1/user_process/(?P<pk>\d+)/$", userprocess, name="delete_user_process"),
    
    #FP-15 JWT TOKEN
    re_path(r'get-token/$', obtain_jwt_token),
    re_path(r'please-is-my-token-valid-sir/', verify_jwt_token),
]