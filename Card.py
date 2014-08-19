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
        self.image = None
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
        getCard(self)
        self.rect = self.image.get_rect()

    def changeOwner(self, position):
        getCard(self)
        self.image.set_alpha()


    def __repr__(self):
        return "<Card at %s >" % (self.rect)
