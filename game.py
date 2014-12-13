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
from listOfCards import allCards  # The list of all the cards
from Text import Text
pygame.init()


class Application():
    """Main class of the game, manage the window"""
    def __init__(self, width, height, screen=None, soundInstance=None,
                  boss=None):
        # We create the window
        self.width = width
        self.height = height
        if screen == None:
            self.screen = pygame.display.set_mode((self.width, self.height))
        else:
            self.screen = screen

        if soundInstance == None:
            self.Sound = Sound()
        else:
            self.Sound = soundInstance

        self.background, self.backgroundRect = loadImage("background.jpg")

        # We keep the Menu instance if we are running TuxleTriad from Menu.py
        if boss != None:
            self.boss = boss
            self.boss.app = self
            self.FONT = self.boss.FONT
        else:
            self.boss = None
            self.FONT = "Dearest.ttf"

        # The Clock of the game, to manage the frame rate
        self.clock = pygame.time.Clock()
        self.fps = 60
        # We generate two Hand and draw 5 cards from each
        # to have an entire Hand of Card
        # For player 1
        self.player1Hand = self.randomHand(1)
        # For player 2
        self.player2Hand = self.randomHand(-1)

        # We create the Score
        self.scorePlayer1 = Score("5", 1, self.width, self.height)
        self.scorePlayer2 = Score("5", -1, self.width, self.height)

        # With this variable, we cannot do anything until the animation
        # played is finished.
        self.animation = 0

        # If we have to play the animation in different directions
        self.sensAnimation = 0
        self.player = 1

        self.position = None
        self.CARD = None
        self.infoCARD = None

        # We create the field of the game, 3x3.
        sizeCard = self.player1Hand.cards[0].image.get_size()
        self.field = Field(self.width, self.height, sizeCard, self)
        self.emptyCase = 9

        self.alphaAnimation = 255

        # Manage the winner congratulations font
        self.winner = Text("", self.FONT, white, 60)

        # Manage the display of the name of the card selected
        self.cardName = None

        # Do we show the name of the card selected?
        self.selectedCardName = 1


    def update(self):
        """Updates all the sprites on the window"""
        self.screen.blit(self.background, self.background.get_rect())
        self.screen.blit(self.field.surface, self.field.rect)
        
        for card in self.player1Hand.cards:
            self.screen.blit(card.image, card.rect)

        for card in self.player2Hand.cards:
            self.screen.blit(card.image, card.rect)

        self.scorePlayer1.update()
        self.scorePlayer2.update()
        self.screen.blit(self.scorePlayer1.surface, self.scorePlayer1.rect)
        self.screen.blit(self.scorePlayer2.surface, self.scorePlayer2.rect)
        if self.winner.text != "":
            self.winner.changeText()
            self.screen.blit(self.winner.surface, self.winner.rect)
        
        if self.selectedCardName != 0:
            self.showName(1)
            self.showName(-1)

        if self.cardName != None:
                self.screen.blit(self.backCard, self.backCardRect)
                self.screen.blit(self.cardName.surface, self.cardName.rect)
                self.cardName = None
        
        if self.infoCARD == None:
        # If we aren't showing the about popup. Because About need to blit one
        # more thing before doing the following commands.
            pygame.display.flip()
            self.clock.tick(self.fps)

    def main(self):
        """Main part handling the game"""
        self.cardsOwner()
        self.update()
        while 1:
            if self.animation == 1:
                # We continue the animation
                self.putCard()
                self.update()
            else:
                # We over the animation and now the next player have to play.
                if self.sensAnimation == 1:
                    self.player = self.player * -1
                    self.sensAnimation = 0

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP and self.animation == 0:
                    if event.button == 3 and self.winner.text == "":
                        if self.getCard(0):
                            self.showAbout()
                    if self.winner.text == "" and event.button == 1:
                        self.infoCARD = None
                        self.playCard()
                elif event.type == QUIT:
                    audio = [self.Sound.soundVolume, self.Sound.musicVolume]
                    setConfig(audio)
                    self.field.saveState()
                    pygame.quit()
                    sys.exit()
                else:
                    # We get the status of all key on keyboard.
                    # Then we select the one at place 27: Escape.
                    # We can do this only if we ran the game
                    # with Menu.py and not directly from main.py
                    if pygame.key.get_pressed()[27] and self.boss != None:
                        self.boss.main()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def playCard(self):
        """When player has to play a card"""

        coords = pygame.mouse.get_pos()

        if self.getCard(self.player):
            self.selectedCard()
        if not self.CARD == None:
        # If we clicked on a card.
        # We wait for the event 'MOUSEBUTTONUP', so first we clean the
        #queue event. Then we deactivate the MOUSEMOTION event, because
        #it causes the card to be put randomly on the field!
        #We wait an event, for example a touch on the keyboard
        #pressed, or MOUSEBUTTONUP, but not only, and we reactivate
        #MOUSEMOTION, we could need it later.
            self.deactivate()
            if not self.animation:
                pygame.event.wait()
            while pygame.event.peek(MOUSEBUTTONUP) and not self.animation:
                pass
            self.reactivate()
            # If the player clicked on the field this time, we test
            #each cases of the Field.
            FieldRect = self.field.fieldRects
            if self.field.rect.collidepoint(pygame.mouse.get_pos()):
                for line in range(len(FieldRect)):
                    for case in range(len(FieldRect[line])):
                        if FieldRect[line][case]\
                                .collidepoint(pygame.mouse.get_pos()):
                            self.Case = self.field.fieldRects[line][case]
                            if not self.caseFilled():
                                self.numberCase = (line*3)+case
                                self.animation = 1
                                self.putCard()
                                self.cardsOwner()
                            return
            else:
                self.deselectedCard()
                self.CARD = None

    def putCard(self):
        """Animation of a card put on the field"""

        if self.CARD.inHand == 1:
        # We check if self..CARD is in the player's Hand
            self.Sound.playPutCard()

        # We drop the card off the Hand
        if self.CARD.inHand == 1:
            self.CARD.inHand = 0

        # Depending of the direction of the animation, we make the card
        # being invisible or visible again.
        if self.sensAnimation == 0:
            self.alphaAnimation -= 25
            self.CARD.image.set_alpha(self.alphaAnimation)
            self.CARD.rect.centerx += 2 * self.player
        elif self.sensAnimation == 1:
            self.alphaAnimation += 25
            self.CARD.image.set_alpha(self.alphaAnimation)

        # We change the position of the card and the animation's direction
        if self.CARD.image.get_alpha() == 5:
            self.CARD.rect = self.Case
            self.sensAnimation = 1

        if self.CARD.image.get_alpha() == 255 and self.sensAnimation == 1:
            # We have put the card on the field and the animation is over.
            # We compare the elements to give potential malus/bonus.
            # And we have to look if that card captured some of the 
            # ennemy's. 
            self.animation = 0
            caseElement = self.field.elementName[self.numberCase]
            if caseElement != None:
                self.Sound.playElement(caseElement)
            if self.CARD.elementName == caseElement \
            and caseElement != None:
                self.CARD.addModifier(1)
            else:
                if caseElement != None:
                    self.CARD.addModifier(-1)
            adjacentCards = self.getAdjacent()
            capturedCard = adjacent(self.CARD, adjacentCards)
            self.changeOwner(capturedCard)
            self.emptyCase -= 1
            self.CARD = None

        if self.emptyCase == 0:
            self.winAnimation()

    def selectedCard(self):
        """Player has selected a card
        But not yet a place on the field"""
        for i in range(5):
            self.CARD.rect.centerx += 4 * self.player
            self.update()

    def deselectedCard(self):
        """Finally, the player wants an other card"""
        for i in range(5):
            self.CARD.rect.centerx -= 4 * self.player
        self.CARD = None
        self.update()

    def deactivate(self):
        """Deactivate MOUSEMOTION event and clean the queue"""
        pygame.event.set_blocked(MOUSEMOTION)
        pygame.event.clear()

    def reactivate(self):
        """Get back MOUSEMOTION"""
        pygame.event.set_allowed(MOUSEMOTION)

    def caseFilled(self):
        """Say if there is already a card in the case"""
        for card in self.player1Hand.cards:
            if card.rect == self.Case:
                return 1
        for card in self.player2Hand.cards:
            if card.rect == self.Case:
                return 1
        return 0

    def cardsOwner(self):
        """Which cards is owned by who?"""
        cardPlayer = 0
        for card in self.player1Hand.cards:
            if card.owner == self.player:
                cardPlayer += 1
        for cards in self.player2Hand.cards:
            if cards.owner == self.player:
                cardPlayer += 1
        if self.player == 1:
            self.scorePlayer1.updateScore(cardPlayer)
            self.scorePlayer2.updateScore(10 - cardPlayer)
        elif self.player == -1:
            self.scorePlayer1.updateScore(10 - cardPlayer)
            self.scorePlayer2.updateScore(cardPlayer)

    def getAdjacent(self):
        """Get all the adjacent cards of the first one put"""
        posx, posy = self.CARD.rect.topleft
        adjacentCards = [None, None, None, None]
        if self.player == 1:
            for card in self.player2Hand.cards:
                if card.inHand == 0:
                    if card.rect.collidepoint((posx, posy - 144)):
                        # We first look at the card on the top
                        adjacentCards[0] = card

                    if card.rect.collidepoint((posx + 113, posy)):
                        # We look at the card on the right
                        adjacentCards[1] = card

                    if card.rect.collidepoint((posx, posy + 144)):
                        # We look at the card on the bottom
                        adjacentCards[2] = card

                    if card.rect.collidepoint((posx - 113, posy)):
                        # We look at the card on the left
                        adjacentCards[3] = card
        elif self.player == -1:
            for card in self.player1Hand.cards:
                if card.inHand == 0:
                    if card.rect.collidepoint((posx, posy - 144)):
                        # We first look at the card on the top
                        adjacentCards[0] = card

                    if card.rect.collidepoint((posx + 113, posy)):
                        # We look at the card on the right
                        adjacentCards[1] = card

                    if card.rect.collidepoint((posx, posy + 144)):
                        # We look at the card on the bottom
                        adjacentCards[2] = card

                    if card.rect.collidepoint((posx - 113, posy)):
                        # We look at the card on the left
                        adjacentCards[3] = card
        return adjacentCards

    def changeOwner(self, cards):
        for card in cards:
            if card.owner == 1:
                self.player1Hand.cards.remove(card)
                self.player2Hand.cards.append(card)
            if card.owner == -1:
                self.player2Hand.cards.remove(card)
                self.player1Hand.cards.append(card)
            self.capturedAnimation(card)
        self.cardsOwner()

    def capturedAnimation(self, card):
        """Shows a little animation when capturing card"""
        # We want the sound of the card put played before doing anything more
        self.update()
        while (pygame.mixer.get_busy()):
            pass

        # self.Sound.capturedCard.play()
        width = card.rect.width  # we expect 113. If not please change format.
        height = card.image.get_rect().height  # Here we expect 139.
        topleft = list(card.rect.topleft)
        step = 16

        while(width != 1):
            width -= step
            topleft[0] += step / 2
            getCard(card)
            card.image = pygame.transform.scale(card.image, (width, height))
            card.rect = card.image.get_rect()
            card.rect.topleft = topleft
            self.update()

        card.owner *= -1
        card.changeOwner()

        while (width != 113):
            width += step
            topleft[0] -= step / 2
            getCard(card)
            card.image = pygame.transform.scale(card.image, (width, height))
            card.rect = card.image.get_rect()
            card.rect.topleft = topleft
            self.update()
        
        # If card has a bonus or malus, we have to re-draw it on the card
        if card.modifierValue != 0:
            card.image.blit(card.modifierBack.surface, card.modifierBack.rect)
            card.image.blit(card.modifier.surface, card.modifier.rect)

    def winAnimation(self):
        """Show who won the game"""
        if self.scorePlayer1.score > self.scorePlayer2.score:
            self.winner.text = _("Blue win!")
            self.winner.rect.topleft = self.backgroundRect.midtop
            self.winner.rect.x -= 20
            self.winner.color = blue
        elif self.scorePlayer2.score > self.scorePlayer1.score:
            self.winner.text = _("Red win!")
            self.winner.rect.topright = self.backgroundRect.midtop
            self.winner.rect.x += 20
            self.winner.color = red
        else:
            self.winner.text = _("Equality!")
            self.winner.rect.topleft = self.backgroundRect.midtop
            self.winner.color = white
        
        self.winner.changeColor()
        self.winner.rect.y += 10
        
    def getCard(self, player):
        """Return the card at pygame.mouse.get_pos() coordinates """
        coords = pygame.mouse.get_pos()
        if player == 1:
            for card in self.player1Hand.cards:
                if card.rect.collidepoint(coords) and card.inHand:
                    self.CARD = card
                    return 1
        elif player == -1:
            for card in self.player2Hand.cards:
                if card.rect.collidepoint(coords) and card.inHand:
                    self.CARD = card
                    return 1
        elif player == 0:
            #Case if we get a right-click, then we want to print the About 
            #popup even if it is an ennemy's card
            for card in self.player1Hand.cards:
                if card.rect.collidepoint(coords) and card.inHand:
                    self.infoCARD = card.About
                    return 1
            for card in self.player2Hand.cards:
                if card.rect.collidepoint(coords) and card.inHand:
                    self.infoCARD = card.About
                    return 1         
        return 0
        
    def showAbout(self):
        """Show some info on the card if we do a right-click on it"""
        width = 0
        quit = 0
        maxWidth = 450
        COLORRED = (100,0,0,125)
        COLORBLUE = (0,0,100,125)
        if self.infoCARD.boss.owner == 1:
            COLOR = COLORBLUE
        elif self.infoCARD.boss.owner == -1:
            COLOR = COLORRED

        background = pygame.Surface((width, 140), SRCALPHA)
        rect = background.get_rect()
        background.fill(COLOR)

        if self.infoCARD.boss.owner == 1:
            rect.topleft = self.infoCARD.boss.rect.topright
        elif self.infoCARD.boss.owner == -1:
            rect.topright = self.infoCARD.boss.rect.topleft
        while 1:
            self.update()
            self.screen.blit(background,rect)
            pygame.display.flip()
            self.clock.tick(self.fps)
            
            if width < maxWidth and quit == 0:
                width += 25
                background = pygame.Surface((width, 140), SRCALPHA)
                rect = background.get_rect()
                background.fill(COLOR)
                if self.infoCARD.boss.owner == 1:
                    rect.topleft = self.infoCARD.boss.rect.topright
                elif self.infoCARD.boss.owner == -1:
                    rect.topright = self.infoCARD.boss.rect.topleft
                    
            if quit == 1:
                width -= 25
                background = pygame.Surface((width, 140), SRCALPHA)
                rect = background.get_rect()
                background.fill(COLOR)
                if self.infoCARD.boss.owner == 1:
                    rect.topleft = self.infoCARD.boss.rect.topright
                elif self.infoCARD.boss.owner == -1:
                    rect.topright = self.infoCARD.boss.rect.topleft
            
            if width == 0:
                if quit == 1:
                    self.update()
                    return
                quit = 1
        
            for event in pygame.event.get():
                if width == 0:
                    self.infoCARD = None
                    self.update()
                    return 0
                if event.type == MOUSEBUTTONUP:
                    quit = 1
                elif event.type == QUIT:
                    audio = [self.Sound.soundVolume, self.Sound.musicVolume]
                    setConfig(audio)
                    pygame.quit()
                    sys.exit()
                    
            if width == maxWidth and quit == 0:
                background.fill(COLOR)
                background.blit(self.infoCARD.surface, self.infoCARD.rect)
                
        
        return 0


    def randomHand(self, player):
        """Get a random set of cards for 'player'. Return a Hand object"""
        Cards = []
        listCards = [card for card in range(len(allCards))]
        random.shuffle(listCards)
        
        for i in range(5):
            number = listCards[0]
            Cards.append(Card(number, player))
            listCards.remove(number)
        
        return Hand(Cards, player)
    
    
    def showName(self, player):
        """Show the name of the card selected at the bottom of the window"""
        self.backCard, self.backCardRect = loadImage("name.png")
        
        if player == 1:
            for card in self.player1Hand.cards:
                if card == self.CARD:
                    name = self.CARD.name
                    self.cardName = Text(name, self.FONT, white, 40)
        elif player == -1:
            for card in self.player2Hand.cards:
                if card == self.CARD:
                    name = self.CARD.name
                    self.cardName = Text(name, self.FONT, white, 40)
    
        if self.cardName != None:
            self.cardName.rect.midbottom = self.backgroundRect.midbottom
            self.cardName.rect.y -= 10
            self.backCardRect.center = self.cardName.rect.center
        
if __name__ == '__main__':
    Application(800, 600).main()
