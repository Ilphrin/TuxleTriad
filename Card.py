# coding: utf-8

import pygame
import os
from functions import *
from color import *
from pygame.locals import *
from listOfCards import allCards, values
from About import About
from Text import *
from color import *


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
        
        self.values = []
        self.values.append(self.top)
        self.values.append(self.right)
        self.values.append(self.bottom)
        self.values.append(self.left)
        self.parseToInt()
        
        # Which element
        self.elementName = values[number][4]
        # Offensive or defensive. Unused for now
        self.type = values[number][5]
        
        self.modifierValue = 0
        self.inHand = 1
        
        getCard(self)
        self.rect = self.image.get_rect()
        if self.elementName != None:
            self.element, self.elementRect = loadElement(self.elementName)
            self.elementRect.topright = self.rect.topright
            self.elementRect.move_ip(-2, 2)
            self.image.blit(self.element, self.elementRect)


    def changeOwner(self):
        getCard(self)
        self.image.set_alpha()
    
    def addModifier(self, value):
        """Add bonus or malus to the card and draw the bonus on the card"""
        
        self.modifierValue = value
        if value > 0:
            value = "+" + str(value)
        else:
            value = str(value)
        self.modifier = Text(value, "rimouski sb.ttf", white, 60)
        self.modifierBack = Text(value, "rimouski sb.ttf", black, 60)
        #self.modifier.rect.topleft = self.rect.topleft
        self.modifier.rect.move_ip(35, 15)
        self.modifierBack.rect.move_ip(38, 18)
        self.image.blit(self.modifierBack.surface, self.modifierBack.rect)
        self.image.blit(self.modifier.surface, self.modifier.rect)
        
        for i in range(0, 4):
            self.values[i] += self.modifierValue

    def parseToInt(self):
        for i in range(0, 4):
            if (self.values[i] == 'A'):
                self.values[i] = 10
            else:
                self.values[i] = int(self.values[i])


    def __repr__(self):
        return "<Card at %s >" % (self.rect)
