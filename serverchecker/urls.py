from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("server/<str:ip>", views.check_server, name="server check"),
    path("force_check/<str:ip>", views.force_update_server, name="force server check"),
    path("enable_scheduler", views.enable_scheduler, name="enable scheduler"),
    path("scheduler_state", views.scheduler_state, name="scheduler state"),
    path("stop_scheduler", views.stop_scheduler, name="stop scheduler"),
]