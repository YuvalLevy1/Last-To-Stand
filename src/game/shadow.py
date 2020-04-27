class Shadow:
    def __init__(self, player):
        self.x = int(player.x + player.width / 2) + 4
        self.y = player.y + player.height - 5
        self.radius = 20  # the circles radius
        self.color = (30, 50, 30)  # the matching color to the background
        self.player = player  # the player who cast the shadow

    # the method updates the shadow's x and y according to the location
    # of the player. should be called every time the player is moving.
    def update_shadow(self):
        self.x = int(self.player.x + self.player.width / 2) + 4
        self.y = self.player.y + self.player.height - 5
