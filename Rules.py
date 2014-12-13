# coding: utf-8

# In this file we will code the functions that will manage the game's rules.
# To use them, we will just import the file in the application and
# get the return values.

def adjacent(card, others):
    """Classic rule, compare the card put with the others already here, and
     return the ones that need to be changed."""
    returnList = []
    if others[0] != None and card.values[0] > others[0].values[2]:
        # The card on the top
        returnList.append(others[0])
    if others[1] != None and card.values[1] > others[1].values[3]:
        # The card on the right
        returnList.append(others[1])
    if others[2] != None and card.values[2] > others[2].values[0]:
        # The card on the bottom
        returnList.append(others[2])
    if others[3] != None and card.values[3] > others[3].values[1]:
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

def elementary(Field):
    """Optional Rule. Generate element randomly on each case of the Field."""
    
    import random
    
    listElement = ['earth', 'fire', 'holy', 'ice', 'poison', 'thunder',
                    'water', 'wind', None, None, None, None, None, None, None,
                    None, None, None, None]
    # There is 'None' x time to give more chance that there isn't element

    for i in range(0,9):
        element = random.randint(0, len(listElement)-1)
        Field.elementName.append(listElement[element])
    for i in range(0,9):
        Field.elementSound.append(listElement[i])


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
