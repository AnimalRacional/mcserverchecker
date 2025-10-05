from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from .models import TrackedServer

# Create your views here.
def index(request):
    servers = TrackedServer.objects.order_by("-last_checked")
    context = { "servers": servers }
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
        #return HttpResponse("Success")
        return render(request, "servers/force_check.html", context)
    print("Tried to access force_check without permission")
    raise Http404

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