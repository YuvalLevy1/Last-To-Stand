import ast
import os

import pygame

from game import game_map
from network import tcp_client, udp_client, network_player, network_constants


class Game:
    window_height = 1080
    window_width = 1920

    def __init__(self):
        self.screen = None
        self.opponents = None  # his online opponents
        self.players = None  # all players, the main player and his opponents
        self.running = False  # whether the game is running or not
        self.background = game_map.map_background  # the image that should be displayed as background
        self.BORDERS_TOP_LEFT = (0, 0)  # the x and y coordinates for the screen's top left corner
        self.BORDERS_BOTTOM_RIGHT = (Game.window_width, Game.window_height)  # the x and y coordinates for
        # the screen's bottom right corner
        self.BORDERS = (self.BORDERS_TOP_LEFT, self.BORDERS_BOTTOM_RIGHT)  # the x and y coordinates for
        # the screen's corners
        self.clock = pygame.time.Clock()  # used to set the game ticks per second
        self.tcp_client = tcp_client.TCPClient()
        self.player_id = None
        self.udp_client = None

    def draw_game_window(self):
        self.screen.blit(self.background, (0, 0))

    def game_over(self):  # detects whether the player is dead and closes the game.
        self.running = False
        self.tcp_client.disconnect()
        print("disconnecting from server")

    def connect_to_server(self):
        self.tcp_client.connect_to_server()
        print("connected to server")
        data = self.tcp_client.receive()
        return data

    def init_game(self):  # initializing game variables
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{0},{1}".format(0, 0)  # setting full screen
        self.screen = pygame.display.set_mode((Game.window_width, Game.window_height))
        pygame.display.set_caption("Last To Stand")
        pygame.init()
        data = self.connect_to_server()
        self.player_id = self.receive_tcp_from_server()
        return data

    def receive_tcp_from_server(self):
        return self.tcp_client.receive()

    def by_event(self, event):
        """ callback after events """
        if event.type == event.QUIT:
            if self.players[self.player_id].udp_client:
                self.players[self.player_id].udp_client.send("Bye")
            self.running = False

    def tcp_update(self, data):
        data = (data.decode()).strip()

        if data.startswith("We need to wait to"):  # we got "Wait to start:0" or "Wait to start:1"
            print(data.decode())

        elif data.startswith("id"):
            self.player_id = int(data.split(":")[1])

        elif data == "starting":
            self.udp_client = udp_client.UDPClient(self.player_id)
            spawn_points = game_map.spawn_points
            player = network_player.NetworkPlayer(spawn_points[self.player_id][0], spawn_points[self.player_id][1],
                                                  self.BORDERS, self.player_id)
            self.players[self.player_id] = player
        elif data == "Bye":
            self.running = False
            self.udp_client.disconnect()
        elif data.startswith("update"):
            data = data.split(":")[1]
            data = eval(data)
            for i in range(len(self.players)):
                self.players[i].use_info_tcp(data[i])

    def init_players(self):
        spawn_points = game_map.spawn_points
        for i in range(network_constants.MAX_NUM_OF_CLIENTS):
            if i != self.player_id:
                enemy = network_player.NetworkPlayer(spawn_points[i][0], spawn_points[i][1],
                                                     self.BORDERS, i)
                self.players[i] = enemy

    def execute(self):
        self.init_game()

        self.by_event(pygame.event.get())


def main():
    pass


if __name__ == '__main__':
    main()
