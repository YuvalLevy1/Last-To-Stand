import os
import time

import pygame

from game import game_map, projectile
from network import tcp_client, udp_client, network_player, network_constants


class Game:

    def __init__(self):
        self.screen = None
        self.waiting_to_start = True
        self.players = None  # all players, the main player and his opponents
        self.player = None
        self.running = False  # whether the game is running or not
        self.background = game_map.map_background  # the image that should be displayed as background
        # the screen's corners
        self.clock = pygame.time.Clock()  # used to set the game ticks per second
        self.tcp_client = tcp_client.TCPClient(self)
        self.player_id = None
        self.udp_client = None

    def init_game(self):  # initializing variables
        data = self.connect_to_server()
        self.tcp_client.start()
        data = data.split(":")
        self.player_id = int(data[1])
        self.udp_client = udp_client.UDPClient(self.player_id)
        self.players = setup_players()
        self.player = self.players[self.player_id]

    def init_screen(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "{0},{1}".format(0, 0)  # setting full screen
        self.screen = pygame.display.set_mode((game_map.BORDERS_BOTTOM_RIGHT[0], game_map.BORDERS_BOTTOM_RIGHT[1]))
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
                if self.player_id == i:
                    continue
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

    def draw_game_window(self, players):
        self.screen.blit(self.background, (0, 0))
        for i in range(network_constants.MAX_NUM_OF_CLIENTS):
            if players[i].is_dead:
                print("player is dead")
                continue
            pygame.draw.circle(self.screen, players[i].shadow.color,
                               (players[i].shadow.x, players[i].shadow.y),
                               players[i].shadow.radius)
            for bullet in players[i].bullets:
                if not bullet.move_projectile(game_map.BORDERS):
                    players[i].bullets.remove(bullet)
                pygame.draw.rect(self.screen, projectile.COLOR, (bullet.x, bullet.y, bullet.width, bullet.height))
            if players[i].walk_count + 1 >= 12:
                players[i].walk_count = 0
            if players[i].is_moving:
                print("drawing sprint")
                try:
                    self.screen.blit(
                        players[i].sprites[players[i].direction_to_index[players[i].current_direction]][
                            players[i].walk_count // 3],
                        (players[i].x, players[i].y))
                except Exception:
                    players[i].walk_count = 0
                # players[i].walk_count += 1
            else:
                self.screen.blit(self.players[i].directions[self.players[i].current_direction],
                                 (self.players[i].x, self.players[i].y))

            if self.player.should_die(get_all_bullets(self.players)):
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
        time.sleep(1)

    game.init_screen()
    pygame.init()
    time.perf_counter()
    last_time = -1
    while game.running:
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            game.by_event(event)

        game.player.move_by_keyboard(keys, mouse_buttons)
        time.sleep(network_constants.UPDATE_SPEED)
        game.player.send_info()
        game.draw_game_window(game.players)

        if time.perf_counter() - last_time > 1:
            print(game.player.is_moving)
            last_time = time.perf_counter()
        game.clock.tick(30)

    print("done")
    pygame.quit()


if __name__ == '__main__':
    main()
