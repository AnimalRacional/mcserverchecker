from django.db import models
from django.utils import timezone
from datetime import datetime

def get_early_datetime():
    timezone.make_aware(datetime.fromtimestamp(1), timezone.get_current_timezone())

# Create your models here.
class TrackedServer(models.Model):
    ip=models.CharField(max_length=128, primary_key=True)
    last_checked=models.DateTimeField("last checked", default=get_early_datetime)
    max_players=models.IntegerField("max players", default=-1)
    online_players=models.JSONField("online players", default=list, blank=True)
    player_count=models.IntegerField("player count", default=0)
    player_history=models.JSONField("player history", default=list, auto_created=True, blank=True)
    mc_version=models.CharField("minecraft version", max_length=32, default='empty')
    mc_motd=models.TextField("motd", default="no motd yet")
    mc_bedrock=models.BooleanField("bedrock", default=False)
    mc_latency=models.FloatField("ping", default=-1)
    mc_favicon=models.TextField("image", default='-')
    last_check_result=models.BooleanField("last check worked",default=False)
    label=models.CharField(blank=True, max_length=128, default="")
    def __str__(self):
        return f"{self.ip}"
    @staticmethod
    def create_empty(ip):
        from datetime import datetime
        last_checked =  timezone.make_aware(datetime.now(), timezone.get_current_timezone())
        max_players = -1
        online_players = ["Herobrine"]
        player_count = -1
        player_history = []
        mc_version = '0.1'
        mc_motd = "This server hasn't been checked yet!"
        mc_bedrock = True
        mc_latency = -1
        mc_favicon = "No favicon yet"
        last_check_result = False
        return TrackedServer.objects.create(
            ip = ip,
            last_checked = last_checked,
            max_players = max_players,
            online_players = online_players,
            player_count = player_count,
            player_history = player_history,
            mc_version = mc_version,
            mc_motd = mc_motd,
            mc_bedrock = mc_bedrock,
            mc_latency = mc_latency,
            mc_favicon = mc_favicon,
            last_check_result = last_check_result
        )
