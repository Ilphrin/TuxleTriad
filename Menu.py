# coding: utf-8

import pygame
import os
import sys
import gettext
from functions import *
from color import *
from pygame.locals import *
from game import Application
from Sound import Sound
from Text import Text
from listOfCards import *
from Card import Card
pygame.init()


class Menu(pygame.sprite.Sprite):
    def __init__(self, width, height):
        self.FONT = "Playball.ttf"
    
        # We create the window
        self.width = width
        self.height = height
        fullscreen = 0
        self.dimension = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.dimension,  fullscreen)
        pygame.display.set_caption("TuxleTriad")

        self._load_translation()

        elemText = [_("Play"), _("Options"), _("Rules"), _("About"),
                         _("Quit Game")]
        self.menu = []
        for elem in elemText:
            self.menu.append(Text(elem, self.FONT, white, 40))

        posx = 400
        posy = 400 - (60 * len(elemText))

        for elem in self.menu:
            elem.rect.center = ((posx, posy))
            posy += 100

        self.bkgrnd, self.bkgrndRect = loadImage("background.jpg")
        self.bkgrndRect = self.bkgrnd.get_rect()

        # The Clock of the game, to manage the frame-rate
        self.clock = pygame.time.Clock()
        self.fps = 60

        # We start the Sound object, playing music and sounds.
        self.sound = Sound()

        # Needed to keep track of the game if we do a pause during the game.
        self.app = None
        

        self.main()

    def main(self):
        pygame.event.clear()
        while 1:
            self.screen.blit(self.bkgrnd, self.bkgrndRect)
            for i in range(len(self.menu)):
                self.screen.blit(self.menu[i].surface, self.menu[i].rect)

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    self.clicked()
                elif event.type == QUIT:
                    self.quitGame()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def quitGame(self):
        setConfig("config.txt", self.sound.volume)
        pygame.quit()
        sys.exit()

    def clicked(self):
        for button in self.menu:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                if button.text == _(u"Play"):
                    self.play()
                elif button.text == _(u"Options"):
                    self.options()
                elif button.text == _(u"Rules"):
                    print "Rules!"
                elif button.text == _(u"About"):
                    self.about()
                elif button.text == _(u"Quit Game"):
                    self.quitGame()
         

    def play(self):
        """User clicked on "Play" """
        if self.app != None:
            texts = [_("Continue"),_("Adventure"), _("Solo"),
                        _("Hot Seat"), _("Back")]
        else:
            texts = [_("Adventure"), _("Solo"),  _("Hot Seat"), _("Back")]    
        length = len(texts)
        if self.app != None:
            textPos = [(250, 100), (250,200), (250, 300), (250,400),
                        (550, 500)]
        else:
            textPos = [(250, 100), (250,200), (250, 300), (550, 500)]
        elements = []
        
        for i in range(length):
            elements.append(Text(texts[i], self.FONT, white, 45))
            elements[i].rect.topleft = textPos[i]
            
        while 1:
            self.screen.blit(self.bkgrnd, self.bkgrndRect)
            for i in range(length):
                self.screen.blit(elements[i].surface, elements[i].rect)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    coordinates = pygame.mouse.get_pos()
                    for i in range(length):
                        if elements[i].rect.collidepoint(coordinates):
                            if elements[i].text == _("Adventure"):
                                print "Adventure!"
                            elif elements[i].text == _("Solo"):
                                print "Solo!"
                            elif elements[i].text == _("Hot Seat"):
                                self.hotSeat()
                            elif elements[i].text == _("Back"):
                                self.main()
                            elif elements[i].text == _("Continue"):
                                self.app.main()
                    
    def options(self):
        pygame.event.clear()
        texts = [_(u"Audio"), _(u"Sounds"), _(u"Music"), _(u"Back")]
        length = len(texts)
        textsPos = [(320, 100), (100, 200), (100, 300), (500, 450)]
        elements = []

        for i in range(length):
            elements.append(Text(texts[i], self.FONT, white, 50))
            elements[i].rect.topleft = textsPos[i]

        bar1, bar1Rect = loadImage("barSound.jpg")
        bar2, bar2Rect = loadImage("barSound.jpg")
        bar1Rect.topleft = (300, 220)
        bar2Rect.topleft = (300, 320)
        bars = [bar1Rect, bar2Rect]

        # X coordinates, relative to the bar's, of beginning and ending
        # of each volume cursor.
        MIN_VOLUME = 15
        MAX_VOLUME = 240

        # X absolute coordinates of the volume cursor.
        MIN = bars[0].x + MIN_VOLUME
        MAX = bars[0].x + MAX_VOLUME

        cursor1, cursor1Rect = loadImage("cursorSound.png")
        cursor2, cursor2Rect = loadImage("cursorSound.png")
        cursor1Rect.topleft = \
          (bar1Rect.x + 225 * self.sound.soundVolume, bar1Rect.y - 23)
        cursor2Rect.topleft = \
          (bar2Rect.x + 225 * self.sound.musicVolume, bar2Rect.y - 23)
        cursors = [cursor1Rect, cursor2Rect]

        while 1:
            self.screen.blit(self.bkgrnd, self.bkgrndRect)
            self.screen.blit(bar1, bar1Rect)
            self.screen.blit(bar2, bar2Rect)
            self.screen.blit(cursor1, cursors[0])
            self.screen.blit(cursor2, cursors[1])
            for i in range(length):
                self.screen.blit(elements[i].surface, elements[i].rect)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quitGame()
                elif event.type == MOUSEBUTTONDOWN:
                    mousex, mousey = pygame.mouse.get_pos()
                    for i in range(len(cursors)):
                        if cursors[i].collidepoint((mousex, mousey)):
                            while pygame.event.poll().type != MOUSEBUTTONUP:
                                mousex, mousey = pygame.mouse.get_pos()
                                if MIN <= mousex <= MAX:
                                    cursors[i].centerx = mousex
                                elif mousex > bars[i].x + MAX_VOLUME:
                                    cursors[i].centerx = bars[i].x + MAX_VOLUME
                                else:
                                    cursors[i].centerx = bars[i].x + MIN_VOLUME
                                volume = cursors[i].centerx - MIN
                                if volume != 0:
                                    volume = (volume / 2.25) / 100.0
                                assert (0.0 <= volume <= 1.0)

                                if i == 0:
                                    self.sound.soundVolume = volume
                                    self.sound.playPutCard()
                                elif i == 1:
                                    self.sound.musicVolume = volume
                                self.sound.update()

                                self.screen.blit(self.bkgrnd, self.bkgrndRect)
                                self.screen.blit(bar1, bar1Rect)
                                self.screen.blit(bar2, bar2Rect)
                                self.screen.blit(cursor1, cursors[0])
                                self.screen.blit(cursor2, cursors[1])
                                for j in range(4):
                                    self.screen.blit(elements[j].surface,\
                                                      elements[j].rect)
                                pygame.display.flip()

                    if elements[3].rect.collidepoint((mousex, mousey)):
                        self.main()

                pygame.display.update()
                
    def about(self):
        page = 1
        allPage = []
        pageList = []
        index = 0
        for number in range(len(allCards)):
            pageList.append(Card(number, 1))
            index += 1
            if index == 3 :
                allPage.append(pageList)
                del pageList
                pageList = []
                index = 0

        maxPage = len(allPage)
        txtPage = str(page) + "/" + str(maxPage)

        navigation = [_("Back"), _("Next"), _("Quit"), "Programming:", 
                    "Kevin \"Ilphrin\" Pellet", "Graphics:", "Yunero Kisapsodos", txtPage]
        navigationPos = [(80,550), (650,550), (660,40), (630, 100),
                    (640, 130), (630, 200), (640, 230), (350,550)]
        elements = []
        for i in range(len(navigation)):
            if 2 < i < 7:
                size = 18
            else:
                size = 30
            elements.append(Text(navigation[i], self.FONT, white, size))
            elements[i].rect.topleft = navigationPos[i]

        cardPos = [(50,50), (50,200), (50, 350)]

        while 1:
            self.screen.blit(self.bkgrnd, self.bkgrndRect)
            for element in elements:
                self.screen.blit(element.surface,element.rect)

            for elem in range(len(allPage[page-1])):
                card = allPage[page-1][elem]
                card.rect.topleft = cardPos[elem]
                card.About.rect.topleft = card.rect.topright
            
            for elem in allPage[page-1]:
                self.screen.blit(elem.image, elem.rect)
                self.screen.blit(elem.About.surface, elem.About.rect)
            
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    coords = pygame.mouse.get_pos()
                    
                    for button in elements:
                        if button.rect.collidepoint(coords):
                            if button.text == _("Back"):
                                if page > 1:
                                    page -= 1
                            if button.text == _("Next"):
                                if page < maxPage:
                                    page += 1
                            if button.text == _("Quit"):
                                self.main()
                            txtPage = str(page) + "/" + str(maxPage)
                            elements[7] = Text(txtPage, self.FONT, white, 30)
                            elements[7].rect.topleft = navigationPos[7]
                if event.type == QUIT:
                    self.quitGame()

            pygame.display.flip()
           
    def _load_translation(self):
        base_path = os.path.dirname(os.path.dirname(sys.argv[0]))
        directory = os.path.join(base_path, 'translations')
        
        params = {
                    'domain': 'TuxleTriad',
                    'fallback': True
                 }
        
        if os.path.isdir(directory):
            params.update({'localedir':directory})
        
        translation = gettext.translation(**params)
        
        translation.install("ngettext")
        
    def solo(self):
        """1vsIA mode"""
        print "Solo!"
        
    def adventure(self):
        """Adventure mode against IA"""
        print "Adventure!"
        
    def hotSeat(self):
        """1vs1 mode"""
        if self.app != None:
            del self.app
            Application(800, 600, self.screen, self.sound, self)
        else:
            Application(800, 600, self.screen, self.sound, self)

Menu(800, 600)
