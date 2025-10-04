from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("server/<str:ip>", views.check_server, name="server check"),
    path("enable_scheduler", views.enable_scheduler, name="enable scheduler")
]