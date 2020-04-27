import pygame

import os

from game import game_map
from network import tcp_client


class Game:

    window_height = 1080
    window_width = 1920

    def __init__(self):
        self.screen = None
        self.player = None  # the main player
        self.opponents = None  # his online opponents
        self.players = None  # all players, the main player and his opponents
        self.running = False  # whether the game is running or not
        self.background = game_map.map_background  # the image that should be displayed as background
        self.BORDERS_TOP_LEFT = (0, 0)  # the x and y coordinates for the screen's top left corner
        self.BORDERS_BOTTOM_RIGHT = (Game.window_width, Game.window_height)
        # the x and y coordinates for the screen's bottom right corner
        self.BORDERS = (self.BORDERS_TOP_LEFT, self.BORDERS_BOTTOM_RIGHT)
        self.clock = pygame.time.Clock()  # used to set the game ticks per second
        self.tcp_client = tcp_client.TCPClient()

    def draw_game_window(self):
        self.screen.blit(self.background, (0, 0))  # the method responsible for drawing on the screen.

    def get_all_living_players(self):
        players = [self.player]
        for opponent in self.opponents:
            if not opponent.is_dead:
                players.append(opponent)
        return players

    def game_over(self):  # detects whether the player is dead and closes the game.
        self.running = False
        self.tcp_client.disconnect()
        print("disconnecting from server")

    def connect_to_server(self):
        self.tcp_client.connect_to_server()
        print("connecting to server")

    def init_game(self):  # initializing game variables
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{0},{1}".format(0, 0)  # setting full screen
        self.screen = pygame.display.set_mode((Game.window_width, Game.window_height))
        pygame.display.set_caption("Last To Stand")
        pygame.init()
        self.connect_to_server()
