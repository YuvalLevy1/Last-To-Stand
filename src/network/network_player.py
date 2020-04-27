from src.game.player import Player
from network.udp_client import UDPClient


class NetworkPlayer(Player):

    def __init__(self, x, y, width, height, velocity, client_id):
        Player.__init__(x, y, width, height, velocity)
        self.client_id = client_id
        self.udp_client = UDPClient(client_id)
