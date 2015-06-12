# coding: utf-8

import pygame
import os
from color import *
from pygame.locals import *


class Score(pygame.sprite.Sprite):
    def __init__(self, score, player, width, height):

        super(pygame.sprite.Sprite).__init__(Score)
        self.score = int(score)
        self.color = None
        self.player = player
        self.bossHeight = height
        self.bossWidth = width
        self.size = 70
        self.update()

    def update(self):

        self.score = int(self.score)
        self.whatColor()
        self.score = str(self.score)
        scoreFont = pygame.font.Font('./fonts/Dearest.ttf', self.size)
        # We need to convert it to do the condition in 'self.wharColor'
        # and 'scoreFont.rend' only takes 'str' as argument
        self.surface = scoreFont.render(self.score, True, self.color)
        self.rect = self.surface.get_rect()
        if self.player == 1:
            self.rect.center = (55, self.bossHeight - 50)
        elif self.player == -1:
            self.rect.center = (self.bossWidth - 55, self.bossHeight - 50)

    def whatColor(self):
        self.size = 80
        if self.score < 6:
            self.color = white
        elif self.score < 8:
            self.color = aqua
        elif self.score < 10:
            self.color = blueGreen
        else:
            self.color = lime
            self.size = 100

    def updateScore(self, score):
        self.score = score

    def __repr__(self):
        return "<Score de ", str(self.player), "= ", str(self.score)

