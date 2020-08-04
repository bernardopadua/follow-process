#DJANGO Core
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import re_path, include
from django.views.generic import RedirectView

#INTERNAL Components
from followprocess.process import views as p_views

urlpatterns = [
    re_path(r'^$', RedirectView.as_view(pattern_name='homeapp', permanent=False), name="index"),
    re_path(r'^login$', 
        auth_views.LoginView.as_view(template_name='process/login.html'), 
        name='login'
    ),
    re_path(r'^home/$', p_views.home_app, name="homeapp"),
    re_path(r'^admin/', admin.site.urls, name='admin'),
    re_path(r'^api/', include('followprocess.process.api.urls'), name="process-api"),
]
