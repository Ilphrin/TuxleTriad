# coding: utf-8

import pygame
import sys
from pygame.locals import *
from Rules import *
from functions import *


class Field():
    """Create a 3x3 field"""
    def __init__(self, width, height, (cardWidth, cardHeight), boss):
        self.boss = boss
        self.x = width / 7
        self.y = height / 7
        self.width = width * 5 / 7
        self.height = height * 4 / 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface = pygame.Surface((self.width, self.height), SRCALPHA)
        
        x = 92
        y = 60
        self.positions = [
            # First line
            (2.53 * x, 1.6 * y), (3.75 * x, 1.6 * y), (4.98 * x, 1.6 * y),
            # Second line
            (2.53 * x, 4.0 * y), (3.75 * x, 4.0 * y), (4.98 * x, 4.0 * y),
            # Third line
            (2.53 * x, 6.4 * y), (3.75 * x, 6.4 * y), (4.98 * x, 6.4 * y)
            ]
        
        self.elementName = []
        self.elements = []
        self.elementSound = []
        elementary(self)
        self.drawElements()
        
        self.fieldRects = []
        self.fieldSurf = []
        lineField = []
        for i in self.positions:
            lineField.append(pygame.Rect(i, (cardWidth, cardHeight)))
            
            if len(lineField) == 3:
                self.fieldRects.append(lineField)
                lineField = []
                
    def squareClicked(self):
        coords = pygame.mouse.get_pos()
        if self.rect.collidepoint(coords):
            for line in range(len(self.fieldRects)):
                for square in range(len(self.fieldRects[line])):
                    if self.fieldRects[line][square].collidepoint(coords):
                        return line * 3 + square
        return -1
            
    def saveState(self):
        """Allow to save the state of the game, to play later or for IA to
        to know the situation"""
        
        self.state = []
        self.line = []
        
        index = 0
        filled = 0
        
        for line in self.fieldRects:
            for rect in line:
                filled = 0
                for card in self.boss.player1Hand.cards:
                    if card.rect.topleft == rect.topleft:
                        self.line.append(card)
                        filled = 1
                for card in self.boss.player2Hand.cards:
                    if card.rect.topleft == rect.topleft:
                        self.line.append(card)
                        filled = 1
                        
                if not filled:
                    self.line.append(None)

            self.state.append(self.line)
            self.line = []
    
    def drawElements(self):
        """Will draw the elements on the Field"""
        
        for i in range(9):
            if self.elementName[i] != None:
                elementSurf, elementRect = loadElement(self.elementName[i])
                elementRect.topright= \
                    self.positions[i]
                elementRect.move_ip(-40,-30)
                self.elements.append((elementSurf, elementRect))
            else:
                self.elements.append(None)
        self.update()
                
    def update(self):
        for elem in self.elements:
            if elem != None:
                self.surface.blit(elem[0] ,elem[1])
