from network.udp_client import UDPClient
from src.game.player import Player


class NetworkPlayer(Player):

    def __init__(self, x, y, map_borders, client_id):
        Player.__init__(self, x, y, map_borders)
        self.client_id = client_id  # the client's id. used to set the UDP port
        self.udp_client = UDPClient(client_id)  # sends the player's data in UDP protocol

    def use_info(self, info):
        info = eval(info)
        if info[1]:
            self.move_by_direction(info[0])
            self.is_moving = True
        self.is_moving = False

    def send_info(self):
        info = str((self.current_direction, self.is_moving))
        self.udp_client.send(info)
