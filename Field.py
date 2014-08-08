# -*- coding: utf-8 -*-

import pygame
import sys
from pygame.locals import *


class Field():
    """Crée un terrain de 3x3 cases"""
    def __init__(self, width, height, (cardWidth, cardHeight)):
        self.x = width / 7
        self.y = height / 7
        self.width = width * 5 / 7
        self.height = height * 4 / 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((self.width, self.height))
        x = 92
        y = 60
        self.positions = [
            # First column
            (2.53 * x, 1.6 * y), (2.53 * x, 4.0 * y), (2.53 * x, 6.4 * y),
            # Second column
            (3.75 * x, 1.6 * y), (3.75 * x, 4.0 * y), (3.75 * x, 6.4 * y),
            # Third column
            (4.98 * x, 1.6 * y), (4.98 * x, 4.0 * y), (4.98 * x, 6.4 * y)
            ]
        self.fieldRects = []
        self.fieldSurf = []
        for i in self.positions:
            self.fieldRects.append(pygame.Rect(i, (cardWidth, cardHeight)))
