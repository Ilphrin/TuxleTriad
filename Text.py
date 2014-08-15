# coding: utf-8

import pygame
import functions


class Text():
    def __init__(self, text, font, color, size):
        self.text = text
        self.size = size
        self.font = functions.getFont(font, self.size)
        self.color = color
        self.initialize()

    def initialize(self):
        self.surface = self.font.render(self.text, True, self.color).convert_alpha()
        self.rect = self.surface.get_rect()
        
    def changeFont(self, font = None):
        self.font = functions.getFont(font, self.size)            
            
    def changeColor(self):
        self.surface = self.font.render(self.text, True, self.color).convert_alpha()
        
    def get_rect(self):
        return self.surface.get_rect()
        
    def __repr__(self):
        return "Position topleft : {}\
                \nColor : {}\
                \nText : {}".format(self.rect.topleft, self.color, self.size)
