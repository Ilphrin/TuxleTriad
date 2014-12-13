# coding: utf-8

import pygame
import sys
import os
from pygame.locals import *
from functions import *


class Sound():
    """Create and manage the Audio settings of the game"""
    def __init__(self):
        self.folder = os.getcwd()
        pygame.mixer.music.load(os.path.join(self.folder, \
                        "musics", "Olga_Scotland_-_Glass_Pumpa_.ogg"))
        pygame.mixer.music.play(-1, 1.0)

        self.fPutCard = os.path.join(self.folder, "sounds","putCard.ogg")
        self.fSlctCard = os.path.join(self.folder, "sounds", "capturedCard.ogg")
        self.clic = os.path.join(self.folder, "sounds", "clic.ogg")
        self.element = None

        self.sounds()
        
        File = readFile()
        
        configExist()
        self.soundVolume, self.musicVolume = getConfig(File)

        self.Channel = pygame.mixer.find_channel()
        self.Channel.set_volume(1.0)
        self.update()

    def sounds(self):
        self.putcard = pygame.mixer.Sound(self.fPutCard)
        self.capturedCard = pygame.mixer.Sound(self.fSlctCard)
        self.clicMenu = pygame.mixer.Sound(self.clic)

    def update(self):
        self.putcard.set_volume(self.soundVolume)
        self.clicMenu.set_volume(self.soundVolume)
        #self.capturedCard.set_volume(self.soundVolume)
        pygame.mixer.music.set_volume(self.musicVolume)
        self.volume = [self.soundVolume, self.musicVolume]

    def playPutCard(self):
        if not pygame.mixer.get_busy():
            self.Channel.play(self.putcard)

    def playElement(self, element):
        self.element = os.path.join(self.folder, "sounds", "Elements",
            (element + ".ogg"))
        print self.element
        if not pygame.mixer.get_busy():
            self.element = pygame.mixer.Sound(self.element)
            self.Channel.play(self.element)

