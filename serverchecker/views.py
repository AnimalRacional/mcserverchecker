from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from .models import TrackedServer
from . import jobs


# Create your views here.
def index(request):
    servers = TrackedServer.objects.order_by("-last_checked")
    context = { "servers": servers, "admin": request.user.is_authenticated and request.user.is_staff }
    return render(request, "servers/index.html", context)

def check_server(request, ip):
    try:
        server = TrackedServer.objects.get(ip=ip)
        context = {"server": server, "admin": False}
    except TrackedServer.DoesNotExist:
        raise Http404("No such server.")
    if(request.user.is_authenticated and request.user.is_staff):
        context["admin"] = True
    return render(request, "servers/check_server.html", context)

def force_update_server(request, ip):
    if(request.user.is_authenticated and request.user.is_staff):
        from . import jobs
        print(f"Forcing update for {ip}")
        context = None
        try:
            server = TrackedServer.objects.get(ip=ip)
            result = jobs.update_server(server)
            server.save()
            context = { "ip": ip, "update_result": result }
        except TrackedServer.DoesNotExist:
            raise Http404("No such server.")
        return render(request, "servers/force_check.html", context)
    print("Tried to access force_check without permission")
    raise Http404

def enable_scheduler(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            jobs.start_jobs()
            context = { "message": "Activated scheduler" }
            return render(request, "servers/scheduler_message.html", context)
        else:
            raise Http404
    else:
        raise Http404
    

def stop_scheduler(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if jobs.jobs_running():
                context = { "message": "Stopping scheduler" }
                jobs.cancel_jobs()
            else:
                context = { "message": "The scheduler is already stopped" }
            return render(request, "servers/scheduler_message.html", context)
    raise Http404

def scheduler_state(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if jobs.jobs_running():
                context = { "message": "Scheduler is ongoing" }
            else:
                context = { "message": "Scheduler is stopped" }
            return render(request, "servers/scheduler_message.html", context)
    raise Http404

