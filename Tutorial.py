# coding: utf-8

import pygame
import sys
import random
import os
from functions import *
from color import *
from pygame.locals import *
from Card import Card
from Sound import Sound
from Hand import Hand
from Field import Field
from Score import Score
from Rules import adjacent
from listOfCards import allCards
from Text import Text
from game import Application
pygame.init()

class Tutorial(Application):
    def __init__(self, width, height, screen=None, soundInstance=None,
                  boss=None):
        Application.__init__(width, height)
        self.main()
        
if __name__=='__main__':
    Tutorial(800, 600)
