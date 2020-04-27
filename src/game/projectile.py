COLOR = (174, 166, 0, 0)


class Projectile:
    def __init__(self, player):
        self.player = player  # the player who shot the projectile
        self.width = 5
        self.height = 10
        self.velocity = 15  # the amount of pixels the projectile moves each frame
        self.color = (174, 166, 0)  # the projectile's color (yellow)
        self.x = player.x + (player.width / 2)
        self.y = player.y + self.height
        self.initial_direction = player.current_direction  # the player's direction the moment he shot the projectile
        self.damage = 100

    def move_left(self, borders):
        if self.x - self.velocity > borders[0][0]:
            self.x -= self.velocity
            return True
        return False

    def move_right(self, borders):
        if self.x + self.width + self.velocity < borders[1][0]:
            self.x += self.velocity
            return True
        return False

    def move_down(self, borders):
        if self.y + self.height + self.velocity < borders[1][1]:
            self.y += self.velocity
            return True
        return False

    def move_up(self, borders):
        if self.y - self.velocity > borders[0][1]:
            self.y -= self.velocity
            return True
        return False

    def move_up_right(self, borders):
        if self.move_up(borders) and self.move_right(borders):
            return True
        return False

    def move_up_left(self, borders):
        if self.move_up(borders) and self.move_left(borders):
            return True
        return False

    def move_down_right(self, borders):
        if self.move_down(borders) and self.move_right(borders):
            return True
        return False

    def move_down_left(self, borders):
        if self.move_down(borders) and self.move_left(borders):
            return True
        return False

    # method should be called every frame once the projectile was shot until it returns False.
    # returns True if projectile should still exist or False if otherwise.
    # when the method returns False, projectile should be removed from the player's bullet list
    def move_projectile(self, borders):
        if self.initial_direction == "up":
            return self.move_up(borders)
        elif self.initial_direction == "up right":
            return self.move_up_right(borders)
        elif self.initial_direction == "right":
            return self.move_right(borders)
        elif self.initial_direction == "down right":
            return self.move_down_right(borders)
        elif self.initial_direction == "down":
            return self.move_down(borders)
        elif self.initial_direction == "down left":
            return self.move_down_left(borders)
        elif self.initial_direction == "left":
            return self.move_left(borders)
        elif self.initial_direction == "up left":
            return self.move_up_left(borders)
