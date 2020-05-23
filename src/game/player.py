import time

import pygame

from src.game import player_sprite, shadow
from src.game import projectile


class Player:
    def __init__(self, x, y, map_borders):
        self.x = x
        self.y = y
        self.width = 35
        self.height = 80
        self.velocity = 7  # the amount of pixels the player moves each frame
        self.hitbox = [x + 3, y + 3, x + 29, y + 70]  # the player's real size.
        # should be a list built like in the follow example: [top_left_x, top_left_y, bottom_right_x, bottom_right_y]
        self.directions = {"down": pygame.image.load(
            "images\\player\\player_down0.PNG"),
            "up": pygame.image.load("images\\player\\player_up0.PNG"),
            "left": pygame.image.load(
                "images\\player\\player_left0.PNG"),
            "right": pygame.image.load(
                "images\\player\\player_right0.PNG"),
            "up left": pygame.image.load(
                "images\\player\\player_up_left0.PNG"),
            "up right": pygame.image.load(
                "images\\player\\player_up_right0.PNG"),
            "down left": pygame.image.load(
                "images\\player\\player_down_left0.PNG"),
            "down right": pygame.image.load(
                "images\\player\\player_down_right0.PNG")}

        """ directions is a dictionary that contains the default image for all of the player's directions. if the
         player is standing still, the default image will be drawn according to the players direction. """

        self.direction_to_index = {"up": 0,
                                   "up right": 1,
                                   "right": 2,
                                   "down right": 3,
                                   "down": 4,
                                   "down left": 5,
                                   "left": 6,
                                   "up left": 7}

        self.current_direction = "down"  # the player's current direction. can be: "right" / "left" / "up" / "down"
        self.walk_count = 0  # counts how many steps the player walked in the current direction
        self.sprites = player_sprite.sprites  # the player's sprite sheet
        self.is_moving = False  # whether or not the player is moving
        self.health_points = 100
        self.bullets = []  # contains the bullets the player shot
        self.last_bullet_time = -1  # the last time a bullet was fired, used to set fire rate
        self.is_dead = False
        self.shadow = shadow.Shadow(self)
        self.map_borders = map_borders

        self.directions_to_functions = {"up": self.move_up,
                                        "up right": self.move_up_right,
                                        "right": self.move_right,
                                        "down right": self.move_down_right,
                                        "down": self.move_down,
                                        "down left": self.move_down_left,
                                        "left": self.move_left,
                                        "up left": self.move_up_left

                                        }

    def move_left(self, borders):
        self.current_direction = "left"
        if self.x - self.velocity > borders[0][0]:
            self.x -= self.velocity
            self.hitbox[0] -= self.velocity
            self.hitbox[2] -= self.velocity
            self.update_shadow()
            return True
        return False

    def move_right(self, borders):
        self.current_direction = "right"
        if self.x + self.width + self.velocity < borders[1][0]:
            self.x += self.velocity
            self.hitbox[0] += self.velocity
            self.hitbox[2] += self.velocity
            self.update_shadow()
            return True
        return False

    def move_down(self, borders):
        self.current_direction = "down"
        if self.y + self.height + self.velocity < borders[1][1]:
            self.y += self.velocity
            self.hitbox[1] += self.velocity
            self.hitbox[3] += self.velocity
            self.update_shadow()
            return True
        return False

    def move_up(self, borders):
        self.current_direction = "up"
        if self.y - self.velocity > borders[0][1]:
            self.y -= self.velocity
            self.hitbox[1] -= self.velocity
            self.hitbox[3] -= self.velocity
            self.update_shadow()
            return True
        return False

    def move_up_right(self, borders):
        if self.move_up(borders) and self.move_right(borders):
            self.current_direction = "up right"
            return True
        if self.current_direction == "up":
            self.move_right(borders)
        elif self.current_direction == "right":
            self.current_direction = "up"
        return False

    def move_up_left(self, borders):
        if self.move_up(borders) and self.move_left(borders):
            self.current_direction = "up left"
            return True
        if self.current_direction == "up":
            self.move_left(borders)
        elif self.current_direction == "left":
            self.current_direction = "up"
        return False

    def move_down_right(self, borders):
        if self.move_down(borders) and self.move_right(borders):
            self.current_direction = "down right"
            return True
        if self.current_direction == "down":
            self.move_right(borders)
        elif self.current_direction == "right":
            self.current_direction = "down"
        return False

    def move_down_left(self, borders):
        if self.move_down(borders) and self.move_left(borders):
            self.current_direction = "down left"
            return True
        if self.current_direction == "down":
            self.move_left(borders)
        elif self.current_direction == "left":
            self.current_direction = "down"
        return False

    '''
        *******************************************
        * should be called repeatedly during game *
        *******************************************
    '''

    def move_by_keyboard(self, keys, mouse_buttons):

        if keys[pygame.K_a] and keys[pygame.K_w]:
            self.move_up_left(self.map_borders)
            self.is_moving = True

        elif keys[pygame.K_a] and keys[pygame.K_s]:
            self.move_down_left(self.map_borders)
            self.is_moving = True

        elif keys[pygame.K_d] and keys[pygame.K_w]:
            self.move_up_right(self.map_borders)
            self.is_moving = True

        elif keys[pygame.K_d] and keys[pygame.K_s]:
            self.move_down_right(self.map_borders)
            self.is_moving = True

        elif keys[pygame.K_a]:
            self.move_left(self.map_borders)
            self.is_moving = True

        elif keys[pygame.K_d]:
            self.move_right(self.map_borders)
            self.is_moving = True

        elif keys[pygame.K_s]:
            self.move_down(self.map_borders)
            self.is_moving = True

        elif + keys[pygame.K_w]:
            self.move_up(self.map_borders)
            self.is_moving = True
        else:
            self.walk_count = 0
            self.is_moving = False

        if mouse_buttons[0]:
            self.shoot()

    def shoot(self):
        if time.clock() - self.last_bullet_time > 0.3:
            self.bullets.append(projectile.Projectile(self))
            self.last_bullet_time = time.clock()

    def should_die(self, bullets):  # determine whether a bullet hit the player or not
        for bullet in bullets:
            if bullet.player != self:
                if self.hitbox[0] <= bullet.x <= self.hitbox[2]:
                    if self.hitbox[1] <= bullet.y <= self.hitbox[3]:
                        self.is_dead = True
                        return True

    def move_by_direction(self, direction):
        self.directions_to_functions[direction](self.map_borders)

    def update_shadow(self):
        self.shadow.update_shadow()
