# coding: utf-8

import pygame
import os
from functions import *
from color import *
from pygame.locals import *
from listOfCards import allCards, values
from About import About


class Card(pygame.sprite.Sprite):
    """Manages the cards in the game"""
    def __init__(self, number, owner):
        super(pygame.sprite.Sprite).__init__(Card)
        self.owner = owner
        self.number = number
        self.name = allCards[self.number]
        #self.verso = carteVerso
        self.About = About(self.name, self)

        # We put the numbers of the card according to listeCartes.py
        self.top = values[number][0]
        self.right = values[number][1]
        self.bottom = values[number][2]
        self.left = values[number][3]
        # Which element
        self.element = values[number][4]
        # Offensive or defensive
        self.type = values[number][5]
        self.inHand = 1
        if self.owner == 1:
            File = os.path.join(os.getcwd(), "cards/" + self.name + "B.jpg")
            self.image = pygame.image.load(File)
            # We put the Surfaces object on video memory. Faster, but there is
            # less memory in video memory than CPU memory
            self.image.convert(self.image.get_bitsize(), pygame.HWSURFACE)
        if self.owner == -1:
            File = os.path.join(os.getcwd(), "cards/" + self.name + "R.jpg")
            self.image = pygame.image.load(File)
            # We put the Surfaces object on video memory. Faster, but there is
            # less memory in video memory than CPU memory
            self.image.convert(self.image.get_bitsize(), pygame.HWSURFACE)
        self.rect = self.image.get_rect()

    def changeOwner(self, position):
        getCard(self)
        self.image.set_alpha()
        #self.rect.center = (position[0], position[1])
        # If 0, then it belongs to player 1, background color is blue.
        # If 1, then it belongs to player 2, background color is red.


    def __repr__(self):
        return "<Card at %s >" % (self.rect)
