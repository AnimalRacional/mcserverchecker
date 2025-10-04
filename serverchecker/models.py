from django.db import models
import json

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
    
