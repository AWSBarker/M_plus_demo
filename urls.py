# main base.html.menu for home.views
from django.urls import path
from . import views
from .views import Home2, Home, Tool_IMEI, Library

urlpatterns = [
    path('', Home.as_view(), name ='home'),
    path('eliot/bp', views.eliot, name='eliot'),
    path('home2', Home2.as_view(), name='home2'),
    path('m1/mhub', views.m1s, name='m1s'),
    path('m2/mhub', views.m2s, name='m2s'),
    path('m3/mhub', views.m3s, name='m3s'),
    path('m4/mhub', views.m4s, name='m4s'),
    path('alarm/alarm', views.alarms, name='alarms'),
    path('library', Library.as_view(), name='library'),
    path('help', views.help, name='help'),
    path('tools', views.tools, name='tools'),
    path('tools/gmon', views.tools_gmon, name='tools_gmon'),
    path('tools/vs_rep', views.tools_vs_rep, name='tools_vs_rep'),
    path('tools/orgs', views.tools_orgs, name='tools_orgs'),
    path('tools/imei', Tool_IMEI.as_view(), name='tools_imei'),
    path('tools/json', views.tools_json, name='tools_json'),
    path('tools/uptime', views.tools_uptime, name='tools_uptime'),
    path('tools/bad_date', views.tools_bad_date, name='tools_bad_date'),
    path('tools/file_download', views.tools_file_download, name='tools_file_download'),
#    path('tools/alert_email', views.send_alert_email, name='send_alert_email'),
]
