import os

import pygame

from src.game import player

os.environ['SDL_VIDEO_WINDOW_POS'] = "{0},{1}".format(0, 0)  # setting full screen
window = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Last To Stand")
pygame.init()

background = pygame.image.load("images\\background.png")

BORDERS_TOP_LEFT = (0, 0)
BORDERS_BOTTOM_RIGHT = (1920, 1080)
BORDERS = (BORDERS_TOP_LEFT, BORDERS_BOTTOM_RIGHT)

running = True

clock = pygame.time.Clock()


def redraw_game_window(players):
    window.blit(background, (0, 0))
    for player in players:
        if player.is_dead or player.should_die(get_all_bullets(players)):
            continue
        pygame.draw.circle(window, player.shadow.color, (player.shadow.x, player.shadow.y), player.shadow.radius)
        for bullet in player.bullets:
            if not bullet.move_projectile(BORDERS):
                player.bullets.remove(bullet)
            pygame.draw.rect(window, (174, 166, 0), (bullet.x, bullet.y, bullet.width, bullet.height))
        if player.walk_count + 1 >= 12:
            player.walk_count = 0
        if player.is_moving:
            window.blit(player.sprites[player.direction_to_index[player.current_direction]][player.walk_count // 3],
                        (player.x, player.y))
            player.walk_count += 1
        else:
            window.blit(player.directions[player.current_direction], (player.x, player.y))
    pygame.display.update()


def get_all_bullets(players):
    bullets = []
    for player in players:
        for bullet in player.bullets:
            bullets.append(bullet)
    return bullets


def main():
    global running
    player1 = player.Player(0, 0, 35, 80, 7)
    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False

        if keys[pygame.K_a] and keys[pygame.K_w]:
            player1.move_up_left(BORDERS[0])
            player1.is_moving = True

        elif keys[pygame.K_a] and keys[pygame.K_s]:
            player1.move_down_left(BORDERS[0], BORDERS[1])
            player1.is_moving = True

        elif keys[pygame.K_d] and keys[pygame.K_w]:
            player1.move_up_right(BORDERS[0], BORDERS[1])
            player1.is_moving = True

        elif keys[pygame.K_d] and keys[pygame.K_s]:
            player1.move_down_right(BORDERS[1])
            player1.is_moving = True

        elif keys[pygame.K_a]:
            player1.move_left(BORDERS[0])
            player1.is_moving = True

        elif keys[pygame.K_d]:
            player1.move_right(BORDERS[1])
            player1.is_moving = True

        elif keys[pygame.K_s]:
            player1.move_down(BORDERS[1])
            player1.is_moving = True

        elif+ keys[pygame.K_w]:
            player1.move_up(BORDERS[0])
            player1.is_moving = True
        else:
            player1.walk_count = 0
            player1.is_moving = False

        if mouse_buttons[0]:
            player1.shoot()
        redraw_game_window([player1])
    pygame.quit()


if __name__ == "__main__":
    main()
