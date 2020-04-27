import pygame

import os

from network import tcp_client


class Game:
    def __init__(self):
        self.screen = None
        self.player = None  # the main player
        self.opponents = None  # his online opponents
        self.players = None  # all players, the main player and his opponents
        self.running = False  # whether the game is running or not
        self.background = None  # the image that should be displayed as background
        self.BORDERS_TOP_LEFT = (0, 0)  # the x and y coordinates for the screen's top left corner
        self.BORDERS_BOTTOM_RIGHT = (1920, 1080)  # the x and y coordinates for the screen's bottom right corner
        self.BORDERS = (self.BORDERS_TOP_LEFT, self.BORDERS_BOTTOM_RIGHT)
        self.clock = None  # used to set the game ticks per second
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

    def connect_to_server(self):
        self.tcp_client.connect_to_server()
        print("connecting to server")

    def init_game(self):  # initializing game variables
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{0},{1}".format(0, 0)  # setting full screen
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Last To Stand")
        pygame.init()
        self.background = pygame.image.load("images\\background.png")
        self.clock = pygame.time.Clock()
        self.connect_to_server()

