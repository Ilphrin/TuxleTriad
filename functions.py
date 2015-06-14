# coding: utf-8

import pygame
import os
from pygame.locals import *

def loadImage(name):
    """Example:
    image, rect = loadImage("myPic.png") """

    image = pygame.image.load(os.path.join(os.getcwd(), name)).convert_alpha()
    rect = image.get_rect()
    return image, rect

def loadElement(name):
    """Example:
    image, rect = loadImage("myPic.png") """
    name = name + ".png"
    image = pygame.image.load(os.path.join(os.getcwd(), "element", name)).convert_alpha()
    rect = image.get_rect()
    return image, rect

def getFont(fontName, size):
    """ Example:
    fontName = getFont("font.ttf") """

    font = pygame.font.Font(os.path.join(os.getcwd(), "fonts", fontName), size)
    return font

def readFile():
    """Example:
    file = readFile("myFile.txt") """

    pathName = checkPath()
    if not configExist():
        setConfig((1.0,1.0))
    fileObject = open(pathName, "r")
    return fileObject.read()

def checkPath():
    """Create a path name for config file depending on location of the program"""
    
    currentPath = os.getcwd()
    if ("/usr" or "/opt") in currentPath:
        pathName = os.path.expanduser("~/.config/tuxle-triad/config.txt")
    else:
        pathName = os.path.join(os.getcwd(), "config.txt")
    
    return pathName

def configExist():
    """Verify if the program is an installed version, and so check if there
    is a configuration folder in ~/.config"""
    
    currentPath = os.getcwd()
    if ("/usr" or "/opt") in currentPath:
        pathName = os.path.expanduser("~/.config/tuxle-triad/")
        
        if not os.path.exists(pathName):
            os.makedirs(pathName)
            print "Creating a configuration folder at" + pathName
            open(os.path.join(pathName, "config.txt"), "w")
            return False
            
        return True
    else:
        return True

def getConfig(fileContent):
    """Example:
    sound, music = getConfig(file)"""
    
    if configExist():
        index = fileContent.find("=")
        index += 2
        soundVolume = float(fileContent[index:index + 4])
        # From the first digit of the value to the last digit.
        index = fileContent.find("=", index + 4)
        index += 2
        musicVolume = float(fileContent[index:index + 4])

        return soundVolume, musicVolume
    else:
        setConfig((1.0,1.0))

def setConfig(parameters):
    """Example:
    setConfig("config.txt", (sound,music)) """

    sound = parameters[0]
    music = parameters[1]
    if len(str(sound)) <= 4:
        if sound == 0:
            sound = str(sound) + ".0"
        elif sound == 1.0:
            pass
        param = str(sound)
        param = param[0:2] + "0"
        sound = param

    if len(str(music)) <= 4:
        if music == 0:
            music = str(music) + ".0"
        elif music == 1.0:
            pass
        param = str(music)
        param = param[0:2] + "0"
        music = param

    print "Sound : ", sound
    print "Music : ", music

    fileObject = open(checkPath(), "w")
    soundContent = "sound = " + str(sound) +\
                    "\nmusic = " + str(music)

    fileObject.write(soundContent)
    
def getCard(card):
    if card.owner == 1:
        File = os.path.join(os.getcwd(), "cards/" + card.name + "B.jpg")
        card.image = pygame.image.load(File)
    if card.owner == -1:
        File = os.path.join(os.getcwd(), "cards/" + card.name + "R.jpg")
        card.image = pygame.image.load(File)

def getHowTo(page):
    if page == 0:
        File = os.path.join(os.getcwd(), "howTo/First.png")
    elif page == 1:
        File = os.path.join(os.getcwd(), "howTo/Second.png")
    return File

def deactivate():
    """Deactivate MOUSEMOTION event and clean the queue"""
    pygame.event.set_blocked(MOUSEMOTION)
    pygame.event.clear()

def reactivate():
    """Get back MOUSEMOTION"""
    pygame.event.set_allowed(MOUSEMOTION)
