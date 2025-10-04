from django.test import TestCase
from serverchecker.models import TrackedServer
from django.utils import timezone
from datetime import datetime

# Create your tests here.
class HypixelTest(TestCase):
    def setUp(self):
        self.server = TrackedServer.create_empty("hypixel.net")

    def test(self):
        from . import jobs
        print("Updating server")
        jobs.update_server(self.server)
        self.assertGreater(self.server.player_count, 10, "Player count not > 10")
        self.assertEqual(self.server.max_players, 200000, "Max players not 20000")
        self.assertFalse("Herobrine" in self.server.online_players, "Herobrine ingame")
        self.assertNotEqual(self.server.mc_version, '0.1', 'Version is 0.1')
        self.assertNotEqual(self.server.mc_motd, "This server hasn't been checked yet!", "MOTD not checked")
        self.assertFalse(self.server.mc_bedrock, "Is bedrock")
        self.assertGreater(self.server.mc_latency, 0, "Latency < 0")
        self.assertNotEqual(self.server.mc_favicon, "No favicon yet", "No favicon")
