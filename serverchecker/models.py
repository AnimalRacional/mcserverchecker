from django.db import models
from django.utils import timezone

# Create your models here.
class TrackedServer(models.Model):
    ip=models.CharField(max_length=128, primary_key=True)
    last_checked=models.DateTimeField("last checked")
    max_players=models.IntegerField("max players")
    online_players=models.JSONField("online players", default=list, blank=True)
    player_count=models.IntegerField("player count", default=0)
    player_history=models.JSONField("player history", default=list, auto_created=True, blank=True)
    mc_version=models.CharField("minecraft version", max_length=32)
    mc_motd=models.TextField("motd")
    mc_bedrock=models.BooleanField("bedrock")
    mc_latency=models.FloatField("ping")
    mc_favicon=models.TextField("image")
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
            mc_favicon = mc_favicon
        )
