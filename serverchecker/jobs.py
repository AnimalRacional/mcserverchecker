import schedule
import threading
import time
from .models import TrackedServer
from django.utils import timezone
import datetime
import mcstatus

def update_server(server: TrackedServer) -> bool:
    try:
        js = mcstatus.JavaServer.lookup(server.ip)
        status = js.status()
        for p in server.online_players:
            if not p in server.player_history:
                server.player_history.append(p)
        server.max_players = status.players.max
        server.player_count = status.players.online
        if(isinstance(status.players.sample, list)):
            server.online_players = [p.name for p in status.players.sample]
            print(f"Online players: {server.online_players}")
        server.mc_version = status.version.name
        server.mc_motd = status.motd.raw.__str__()
        server.mc_bedrock = status.motd.bedrock
        server.mc_latency = status.latency
        if isinstance(status.icon, str):
            server.mc_favicon = status.icon
        server.last_checked = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
        print(f"Finished updating {server.ip}!")
        return True
    except ConnectionRefusedError:
        print(f"Couldn't connect to {server.ip}!")
        server.last_checked = timezone.make_aware(datetime.datetime.now(), timezone.get_current_timezone())
        return False

def check_servers():
    servers = TrackedServer.objects.order_by("last_checked")[:10]
    print(f"Checking servers! It's currently {datetime.datetime.now()}")
    for i in servers:
        print(f"Checking {i.ip}, last checked at {i.last_checked}")
        update_server(i)
        i.save()



def start_scheduler():
    print("Starting scheduler!")
    cease_run = threading.Event()
    class ScheduleThread(threading.Thread):
        def run(self):
            while not cease_run.is_set():
                schedule.run_pending()
                time.sleep(1)
    
    schedule_thread = ScheduleThread()
    schedule_thread.start()
    return cease_run

def schedule_jobs():
    schedule.every(10).seconds.do(check_servers)

