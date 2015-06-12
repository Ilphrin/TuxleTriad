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
from Buttons import Button
from listOfCards import *
from Card import Card
pygame.init()


class Menu(pygame.sprite.Sprite):
    def __init__(self, width, height):
        self.FONT = "Playball.ttf"
    
        # We create the window
        self.width = width
        self.height = height
        fullscreen = pygame.NOFRAME
        self.dimension = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.dimension,  fullscreen)
        pygame.display.set_caption("TuxleTriad")

        self._load_translation()


        self.bkgrnd, self.bkgrndRect = loadImage("background.jpg")
        self.bkgrndRect = self.bkgrnd.get_rect()

        # The Clock of the game, to manage the frame-rate
        self.clock = pygame.time.Clock()
        self.fps = 80

        # We start the Sound object, playing music and sounds.
        self.sound = Sound()

        # Needed to keep track of the game if we do a pause during the game.
        self.app = None
        

        self.main()

    def main(self):
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
        pygame.event.clear()

        while 1:
            self.updateMenu()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    self.clicked()
                elif event.type == QUIT:
                    self.quitGame()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def updateMenu(self):
        self.screen.blit(self.bkgrnd, self.bkgrndRect)
        for i in range(len(self.menu)):
            self.screen.blit(self.menu[i].surface, self.menu[i].rect)

    def quitGame(self):
        setConfig(self.sound.volume)
        pygame.quit()
        sys.exit()
    
    def oldMenu(self):
        while(1):
            for button in self.menu:
                button.rect.centerx -= 20
                if (button.rect.centerx <= - 700):
                    return;
            self.updateMenu()
            pygame.display.flip()

    def clicked(self):
        for button in self.menu:
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                self.sound.clicMenu.play()
                if button.text == _(u"Quit Game"):
                    self.quitGame()
                self.oldMenu()
                if button.text == _(u"Play"):
                    self.play()
                elif button.text == _(u"Options"):
                    self.options()
                elif button.text == _(u"Rules"):
                    self.rules()
                elif button.text == _(u"About"):
                    self.about()
                self.main()
         

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
        self.menu = []
        for i in range(length):
            self.menu.append(Text(texts[i], self.FONT, white, 45))
            self.menu[i].rect.topleft = textPos[i]
            
        while 1:
            self.updateMenu()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    coordinates = pygame.mouse.get_pos()
                    for i in range(length):
                        if self.menu[i].rect.collidepoint(coordinates):
                            self.sound.clicMenu.play()
                            self.oldMenu()
                            if self.menu[i].text == _("Adventure"):
                                return
                            elif self.menu[i].text == _("Solo"):
                                return
                            elif self.menu[i].text == _("Hot Seat"):
                                self.hotSeat()
                            elif self.menu[i].text == _("Back"):
                                return
                            elif self.menu[i].text == _("Continue"):
                                self.app.main()
                    
    def options(self):
        pygame.event.clear()
        texts = [_("Audio"), _("Sounds"), _("Music"), _("Back")]
        length = len(texts)
        textsPos = [(320, 100), (100, 200), (100, 300), (550, 500)]
        self.menu = []

        for i in range(length):
            self.menu.append(Text(texts[i], self.FONT, white, 50))
            self.menu[i].rect.topleft = textsPos[i]

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
                self.screen.blit(self.menu[i].surface, self.menu[i].rect)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quitGame()
                elif event.type == MOUSEBUTTONDOWN:
                    mousex, mousey = pygame.mouse.get_pos()
                    for i in range(len(bars)):
                        if bars[i].collidepoint((mousex, mousey)):
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
                                    self.screen.blit(self.menu[j].surface,\
                                                      self.menu[j].rect)
                                pygame.display.flip()

                    if self.menu[3].rect.collidepoint((mousex, mousey)):
                        del bar1, bar2, bars, cursor1, cursor2, cursors
                        self.oldMenu()
                        self.sound.clicMenu.play()
                        return

                pygame.display.update()
                
    def about(self):
        page = 1
        allPage = []
        pageList = []
        index = 0
        for number in range(len(allCards)):
            pageList.append(Card(number, 1))
            index += 1
            if index == 3 or number == (len(allCards) or len(allCards)-1):
                allPage.append(pageList)
                del pageList
                pageList = []
                index = 0

        maxPage = len(allPage)
        txtPage = str(page) + "/" + str(maxPage)

        navigation = [_("Back"), _("Next"), _("Quit"),
                    "Programming:", "Kevin \"Ilphrin\" Pellet",
                    "Graphics:", "Yunero Kisapsodos",
                    txtPage]
        navigationPos = [(80,550), (650,550), (660,40), (630, 100),
                    (640, 130), (630, 200), (640, 230), (350,550)]
        self.menu = []
        for i in range(len(navigation)):
            if 2 < i < 7:
                size = 12
                font = "rimouski sb.ttf"
            else:
                font = self.FONT
                size = 30
            self.menu.append(Text(navigation[i], font, white, size))
            self.menu[i].rect.topleft = navigationPos[i]

        cardPos = [(50,50), (50,200), (50, 350)]

        while 1:
            self.screen.blit(self.bkgrnd, self.bkgrndRect)
            for element in self.menu:
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
                    
                    for button in self.menu:
                        if button.rect.collidepoint(coords):
                            if button.text == _("Back"):
                                if page > 1:
                                    page -= 1
                                    self.sound.putcard.play()
                            if button.text == _("Next"):
                                if page < maxPage:
                                    page += 1
                                    self.sound.putcard.play()
                            if button.text == _("Quit"):
                                self.oldMenu()
                                return
                            txtPage = str(page) + "/" + str(maxPage)
                            self.menu[7] = Text(txtPage, self.FONT, white, 30)
                            self.menu[7].rect.topleft = navigationPos[7]
                if event.type == QUIT:
                    self.quitGame()

            pygame.display.flip()
            
    def rules(self):
        tutorialButton = Button(_(u"Tutorial"), self.FONT, white)
        howtoButton = Button(_(u"How To"), self.FONT, white)
        backButton = Button(_(u"Back"), self.FONT, white)
        
        tutorialButton.rect.topleft = (250, 100)
        howtoButton.rect.topleft = (250, 200)
        backButton.rect.topleft = (550, 500)
        self.menu = []
        self.menu.append(tutorialButton)
        self.menu.append(howtoButton)
        self.menu.append(backButton)
        
        while (1):
            self.updateMenu()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    coords = pygame.mouse.get_pos()
                    for i in range(len(self.menu)):
                        if self.menu[i].rect.collidepoint(coords):
                            self.oldMenu()
                            if self.menu[i].text == _(u"Tutorial"):
                                self.main()
                            elif self.menu[i].text == _(u"How To"):
                                self.HowTo()
                                return
                            elif self.menu[i].text == _(u"Back"):
                                self.main()
                elif event.type == QUIT:
                    self.quitGame()
            pygame.display.flip()
             
    def HowTo(self):
        backButton = Button(_("Back"), self.FONT, white)
        prevButton = Button(_("Prev"), self.FONT, white)
        nextButton = Button(_("Next"), self.FONT, white)
        page = 1
        maxPage = 2
        pageList = []
        for i in range(maxPage):
            pageList.append(pygame.image.load(getHowTo(i)))
        
        pageRect = pageList[i - 1].get_rect()
        pageRect.topleft = (-20, 0)
        backButton.rect.topleft = (600, 40)
        prevButton.rect.topleft = (80, 550)
        nextButton.rect.topleft = (660, 550)
        self.menu = []
        self.menu.append(backButton)
        self.menu.append(prevButton)
        self.menu.append(nextButton)
                
        while (1):
            self.updateMenu()
            self.screen.blit(pageList[page - 1], pageRect)

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    coords = pygame.mouse.get_pos()
                    if backButton.rect.collidepoint(coords):
                        self.oldMenu()
                        return
                    elif prevButton.rect.collidepoint(coords) and page > 1:
                        page -= 1
                    elif nextButton.rect.collidepoint(coords) and page < maxPage:
                        page += 1
                elif event.type == QUIT:
                    self.quitGame()
            pygame.display.flip()
            
        
        
    def _load_translation(self):
        base_path = os.getcwd()
        directory = os.path.join(base_path, 'translations')
        print "Loading translations at: ", directory

        params = {
                    'domain': 'tuxle-triad',
                    'fallback': True
                 }
        
        if os.path.isdir(directory):
            params.update({'localedir': directory})
        
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
            Application(800, 600, self.screen, self.sound, self).main()
        else:
            Application(800, 600, self.screen, self.sound, self).main()

Menu(800, 600)
