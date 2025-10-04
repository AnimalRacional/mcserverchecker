from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from .models import TrackedServer

# Create your views here.
def index(request):
    servers = TrackedServer.objects.order_by("-last_checked")[:10]
    context = { "servers": servers }
    return render(request, "servers/index.html", context)

def check_server(request, ip):
    try:
        server = TrackedServer.objects.get(ip=ip)
        context = {"server": server}
        print(f"motd: {server.mc_motd}")
    except TrackedServer.DoesNotExist:
        raise Http404("No such server.")
    if(request.user.is_authenticated):
        print(f"user: {request.user.is_staff}")
        pass
    return render(request, "servers/check_server.html", context)

stop_scheduler_event = None

def enable_scheduler(request):
    global stop_scheduler_event
    if(request.user.is_authenticated):
        if(request.user.is_staff):
            from . import jobs
            if stop_scheduler_event == None:
                jobs.schedule_jobs()
                stop_scheduler_event = jobs.start_scheduler()
            else:
                stop_scheduler_event.set()
                stop_scheduler_event = jobs.start_scheduler()
            
            return HttpResponse("Activated scheduler")
        else:
            raise Http404
    else:
        raise Http404