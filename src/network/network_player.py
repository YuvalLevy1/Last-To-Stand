from network.udp_client import UDPClient
from src.game.player import Player


class NetworkPlayer(Player):

    def __init__(self, x, y, map_borders, client_id):
        Player.__init__(x, y, map_borders)
        self.client_id = client_id  # the client's id. used to set the UDP port
        self.udp_client = UDPClient(client_id)  # sends the player's data in UDP protocol

    def send_info_udp(self):
        info = str((self.current_direction, self.is_moving)).encode()
        self.udp_client.send(info)

    def use_info_udp(self, info):
        info = eval(info.decode())
        if info[1]:
            self.move_by_direction(info[0])
            self.is_moving = True
        self.is_moving = False

    def get_info_tcp(self):
        info = str((self.x, self.y, self.hitbox, self.current_direction, self.walk_count, self.is_moving, self.shadow))
        return info

    def use_info_tcp(self, info):
        info = eval(info.decode())
        self.x = info[0]
        self.y = info[1]
        self.hitbox = info[2]
        self.current_direction = info[3]
        self.walk_count = info[4]
        self.is_moving = info[5]
        self.shadow = info[6]
