import ctypes

import pygame

map_background = pygame.image.load("images\\background.png")


BORDERS_TOP_LEFT = (0, 0)
BORDERS_BOTTOM_RIGHT = (720, 480)
user32 = ctypes.windll.user32
# BORDERS_BOTTOM_RIGHT = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
BORDERS = (BORDERS_TOP_LEFT, BORDERS_BOTTOM_RIGHT)
spawn_points = [(BORDERS_BOTTOM_RIGHT[0] // 5, BORDERS_BOTTOM_RIGHT[1] // 5),
                (BORDERS_BOTTOM_RIGHT[0] // 5 * 4, BORDERS_BOTTOM_RIGHT[1] // 5),
                (BORDERS_BOTTOM_RIGHT[0] // 5, BORDERS_BOTTOM_RIGHT[1] // 5 * 4),
                (BORDERS_BOTTOM_RIGHT[0] // 5 * 4, BORDERS_BOTTOM_RIGHT[1] // 5 * 4)]
