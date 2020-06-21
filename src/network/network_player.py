from network.udp_client import UDPClient
from src.game.player import Player


class NetworkPlayer(Player):

    def __init__(self, x, y, map_borders, client_id):
        Player.__init__(self, x, y, map_borders)
        self.client_id = client_id  # the client's id. used to set the UDP port
        self.udp_client = UDPClient(client_id)  # sends the player's data in UDP protocol

    def use_info(self, info):
        info = eval(info)
        if info[len(info) - 1]:
            self.x = info[0]
            self.y = info[1]
            self.is_moving = True
            self.move_by_direction(info[2])
        else:
            self.walk_count = 0
            self.is_moving = False

    def send_info(self):
        info = str((self.x, self.y, self.current_direction, self.is_moving))
        self.udp_client.send(info)
