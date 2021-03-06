# coding: utf-8

import pygame, sys
from color import *
from pygame.locals import *


class Hand():
    """Create a list of cards, and places it"""
    def __init__(self, cards, player):
        self.cards = cards
        # Coefficient for coord-Y of the cards
        I = 0
        DELTA = 80
        for card in self.cards:
            if player == 1:
                card.rect.center = (60, 100 + DELTA * I)
            elif player == -1:
                card.rect.center = (740, 100 + DELTA * I)
            card.rect = pygame.Rect([card.rect[0], card.rect[1],
                                      card.rect[2], DELTA])
            I += 1

    def cardsOwner(self):
        i = 0
        for card in self.cards:
            i += 1
        return i
        
    def getCard(self, coords):
        for i in range(len(self.cards)):
            if self.cards[i].rect.collidepoint(coords) and self.cards[i].inHand:
                return i
        return None
