# coding: utf-8

# In this file we will code the functions that will manage the game's rules.
# To use them, we will just import the file in the application and
# get the return values.


def adjacent(card, others):
    # Classic rule, compare the card put with the others already here, and
    # return the ones that need to be changed.
    returnList = []
    if others[0] != None and card.top > others[0].bottom:
        # The card on the top
        returnList.append(others[0])
    if others[1] != None and card.right > others[1].left:
        # The card on the right
        returnList.append(others[1])
    if others[2] != None and card.bottom > others[2].top:
        # The card on the bottom
        returnList.append(others[2])
    if others[3] != None and card.left > others[3].right:
        # The card on the left
        returnList.append(others[3])
    return returnList


#def opened():
    # Basic rule, we can see the cards in the opposant's hand

#def plusCombination():
    # Non-basic rule, we test each combination of pair of adjacent
    #cards and test if, when we add the value of each element of
    #a combination, the results are the same. If it is, then all cards
    #are won by the player who put the card

#def elementary():
    # Règle supplémentaire. On génère des éléments
    #aléatoirement à chaque position et on les place
    #sur les cases.


#def style():
    # Règle supplémentaire pour les carte faible.
    #Deux types: soit la carte est offensive, dans ce
    #cas elle reçoit +1 quand c'est elle qui attaque?
    #Soit elle est défensive, dans ce cas elle reçoit
    #un bonus quand on l'attaque.

#def diagonal():
    # Règle supplémentaire, peut remplacer la règle 'adjacent'.
    #On compare la carte posée avec les cartes qui sont à ses
    #diagonales.

#def closed():
    # Règle supplémentaire, peut remplacer la règle 'open'.
    #On ne peut pas voir les cartes dans la main de l'adversaire.'
