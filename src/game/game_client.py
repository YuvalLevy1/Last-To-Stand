import os
import time

import pygame

from game import game_map, projectile
from network import tcp_client, udp_client, network_player, network_constants


class Game:
    window_height = 1080
    window_width = 1920

    def __init__(self):
        self.screen = None
        self.waiting_to_start = True
        self.opponents = None  # his opponents
        self.players = None  # all players, the main player and his opponents
        self.player = None
        self.running = False  # whether the game is running or not
        self.background = game_map.map_background  # the image that should be displayed as background
        self.BORDERS_TOP_LEFT = (0, 0)  # the x and y coordinates for the screen's top left corner
        self.BORDERS_BOTTOM_RIGHT = (Game.window_width, Game.window_height)  # the x and y coordinates for
        # the screen's bottom right corner
        self.BORDERS = (self.BORDERS_TOP_LEFT, self.BORDERS_BOTTOM_RIGHT)  # the x and y coordinates for
        # the screen's corners
        self.clock = pygame.time.Clock()  # used to set the game ticks per second
        self.tcp_client = tcp_client.TCPClient(self)
        self.player_id = None
        self.udp_client = None

    def init_game(self):  # initializing variables
        data = self.connect_to_server()
        data = data.split(":")
        self.player_id = int(data[1])
        self.udp_client = udp_client.UDPClient(self.player_id)
        self.players = setup_players()
        self.opponents = self.players
        self.player = self.players[self.player_id]
        self.opponents.remove(self.player)

    def init_screen(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{0},{1}".format(0, 0)  # setting full screen
        self.screen = pygame.display.set_mode((Game.window_width, Game.window_height))
        pygame.display.set_caption("Last To Stand")

    def tcp_update(self, data):
        data = data.strip()

        if data.startswith("We need to wait to"):  # we got "Wait to start:0" or "Wait to start:1"
            print(data)

        elif data == "starting":
            self.running = True
            self.waiting_to_start = False
        elif data == "ok":
            self.running = False
            self.udp_client.disconnect()
        elif data.startswith("update"):
            data = data.split(":")[1]
            data = eval(data)
            for i in range(len(self.players)):
                self.players[i].use_info(data[i])
        elif "disconnect" in data:
            disconnect_id = int(data.split(":")[1])
            self.players[disconnect_id].is_dead = True

        else:
            print(data)

    def by_event(self, event):
        """ callback after events """
        if event.type == pygame.QUIT:
            if self.players[self.player_id].udp_client:
                self.players[self.player_id].udp_client.send("Bye")
            self.running = False

    def draw_game_window(self):
        self.screen.blit(self.background, (0, 0))
        for player in self.players:
            if player.is_dead:
                continue
            pygame.draw.circle(self.screen, player.shadow.color, (player.shadow.x, player.shadow.y),
                               player.shadow.radius)
            for bullet in player.bullets:
                if not bullet.move_projectile(self.BORDERS):
                    player.bullets.remove(bullet)
                pygame.draw.rect(self.screen, projectile.COLOR, (bullet.x, bullet.y, bullet.width, bullet.height))
            if player.walk_count + 1 >= 12:
                player.walk_count = 0
            if player.is_moving:
                self.screen.blit(
                    player.sprites[player.direction_to_index[player.current_direction]][player.walk_count // 3],
                    (player.x, player.y))
                player.walk_count += 1
            else:
                self.screen.blit(player.directions[player.current_direction], (player.x, player.y))

            if self.player.should_die(get_all_bullets(self.opponents)):
                self.game_over()
        pygame.display.update()

    def game_over(self):
        """
        should be called if the player died.
        disconnects from server and shuts down the game
        :return:
        """
        self.running = False
        pygame.quit()
        print("disconnecting from server")

    def connect_to_server(self):
        self.tcp_client.connect_to_server()
        print("connected to server")
        client_id = self.tcp_client.receive()
        return client_id

    def receive_tcp_from_server(self):
        return self.tcp_client.receive()


def setup_players():
    players = []
    for i in range(network_constants.MAX_NUM_OF_CLIENTS):
        players.append(network_player.NetworkPlayer(game_map.spawn_points[i][0],
                                                    game_map.spawn_points[i][1],
                                                    game_map.BORDERS,
                                                    i))
    return players


def get_all_bullets(players):
    bullets = []
    for player in players:
        for bullet in player.bullets:
            bullets.append(bullet)
    return bullets


def main():
    game = Game()
    game.init_game()
    while game.waiting_to_start:
        game.tcp_update(game.receive_tcp_from_server())

    game.init_screen()
    pygame.init()

    while game.running:
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            game.by_event(event)
        game.player.move_by_keyboard(keys, mouse_buttons)
        game.player.send_info()
        game.draw_game_window()
    print("done")
    pygame.quit()


if __name__ == '__main__':
    main()
