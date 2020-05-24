import ctypes
import os

import pygame

from game import projectile
from network import network_constants, network_player
from src.game import player

os.environ['SDL_VIDEO_WINDOW_POS'] = "{0},{1}".format(0, 0)  # setting full screen
window = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Last To Stand")
pygame.init()

background = pygame.image.load("images\\background.png")

BORDERS_TOP_LEFT = (0, 0)
# BORDERS_BOTTOM_RIGHT = (1920, 1080)
user32 = ctypes.windll.user32
BORDERS_BOTTOM_RIGHT = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

BORDERS = (BORDERS_TOP_LEFT, BORDERS_BOTTOM_RIGHT)
running = True

clock = pygame.time.Clock()


def draw_game_window(players):
    window.blit(background, (0, 0))
    for i in range(network_constants.MAX_NUM_OF_CLIENTS):
        if i > 0:
            continue
        if players[i].is_dead:
            print("player is dead")
            continue
        pygame.draw.circle(window, players[i].shadow.color,
                           (players[i].shadow.x, players[i].shadow.y),
                           players[i].shadow.radius)
        for bullet in players[i].bullets:
            if not bullet.move_projectile(BORDERS):
                players[i].bullets.remove(bullet)
            pygame.draw.rect(window, projectile.COLOR, (bullet.x, bullet.y, bullet.width, bullet.height))
        if players[i].walk_count + 1 >= 12:
            players[i].walk_count = 0
        if players[i].is_moving:
            window.blit(
                players[i].sprites[players[i].direction_to_index[players[i].current_direction]][
                    players[i].walk_count // 3],
                (players[i].x, players[i].y))
            players[i].walk_count += 1
        else:
            window.blit(players[i].directions[players[i].current_direction],
                        (players[i].x, players[i].y))

        if players[i].should_die(get_all_bullets(players)):
            # self.game_over()
            pass
    pygame.display.update()


def get_all_bullets(players):
    bullets = []
    for player in players:
        for bullet in player.bullets:
            bullets.append(bullet)
    return bullets


def main():
    global running
    player1 = network_player.NetworkPlayer(0, 0, BORDERS, 0)
    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False

        player1.move_by_keyboard(keys, mouse_buttons)
        print("the keys are: ", keys)
        draw_game_window([player1])
    pygame.quit()


if __name__ == "__main__":
    main()
