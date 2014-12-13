# coding: utf-8

import os
import sys
import pygame
from pygame.locals import *
from Text import Text


class About():
    def __init__(self, name, boss):
        self.file = name + ".txt"    
        self.boss = boss

        directory = os.path.join(os.getcwd(), "cards/about/"+self.file)
        fileObject = open(directory, "r")
        
        white = (255,255,255)
        font = "rimouski sb.ttf"

        self.name = Text(fileObject.readline()[:-1], font, white, 18)
        self.nameRect = self.name.get_rect()
        self.nameRect.topleft = (5,5)
        # Description must be in length less than 66 characters
        self.description = Text(fileObject.readline()[:-1], font, white, 14)
        self.descriptionRect = self.description.get_rect()
        self.descriptionRect.topleft = (5, 30)
        self.initialRelease = Text(fileObject.readline()[:-1], font, white, 12)
        self.initialReleaseRect = self.initialRelease.get_rect()
        self.initialReleaseRect.topleft = (5, 120)
        self.license = Text(fileObject.readline()[:-1], font, white, 12)
        self.licenseRect = self.license.get_rect()
        self.licenseRect.topleft = (135, 120)
        self.surface = pygame.Surface((450, 140), SRCALPHA)
        self.surface.fill((0,0,0,125))
        self.rect = self.surface.get_rect()
        self.surface.blit(self.name.surface, self.nameRect)
        self.surface.blit(self.description.surface, self.descriptionRect)
        self.surface.blit(self.initialRelease.surface, self.initialReleaseRect)
        self.surface.blit(self.license.surface, self.licenseRect)
        

        
        
        
    def __repr__(self):
        output = self.name + "\n" + self.description + "\n" + \
                        self.initialRelease + "\t\t" + self.license + "\n"
        output = str(output)
        return output
