import pygame
import functions


class Button():
    def __init__(self, text, font, color):
        self.text = text
        self.font = functions.getFont(font, 45)
        self.color = color
        self.initialize()

    def initialize(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
