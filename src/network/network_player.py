import pygame

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
            self.move_by_direction(info[2])
            self.is_moving = True
        self.is_moving = False

    def send_info(self):
        info = str((self.x, self.y, self.current_direction, self.is_moving))
        self.udp_client.send(info)

    def move_by_keyboard(self, keys, mouse_buttons):
        self.is_moving = True

        if keys[pygame.K_a] and keys[pygame.K_w]:
            self.move_up_left(self.map_borders)
            self.is_moving = True
            self.walk_count += 1
            self.send_info()

        elif keys[pygame.K_a] and keys[pygame.K_s]:
            self.move_down_left(self.map_borders)
            self.is_moving = True
            self.walk_count += 1
            self.send_info()

        elif keys[pygame.K_d] and keys[pygame.K_w]:
            self.move_up_right(self.map_borders)
            self.is_moving = True
            self.walk_count += 1
            self.send_info()

        elif keys[pygame.K_d] and keys[pygame.K_s]:
            self.move_down_right(self.map_borders)
            self.is_moving = True
            self.walk_count += 1
            self.send_info()

        elif keys[pygame.K_a]:
            self.move_left(self.map_borders)
            self.is_moving = True
            self.walk_count += 1
            self.send_info()

        elif keys[pygame.K_d]:
            self.move_right(self.map_borders)
            self.is_moving = True
            self.walk_count += 1
            self.send_info()

        elif keys[pygame.K_s]:
            self.move_down(self.map_borders)
            self.is_moving = True
            self.walk_count += 1
            self.send_info()

        elif keys[pygame.K_w]:
            self.move_up(self.map_borders)
            self.is_moving = True
            self.walk_count += 1
            self.send_info()
        else:
            self.walk_count = 0
            self.is_moving = False

        if mouse_buttons[0]:
            self.shoot()
