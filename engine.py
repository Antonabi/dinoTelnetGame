"""
A really crappy "game engine". (only renders stuff)
"""

import numpy as np
from typing import List

class Object:
    """
    A game object.
    """
    def __init__(self, characters: List[str], xPos, yPos) -> None:
        self.characters = characters

        self.xPos = xPos
        self.yPos = yPos

        # the velocity has to be used in the game. The engine (that only renders) doesnt have a physics system.
        self.yVelocity = 0
        self.xVelocity = 0

    @property
    def _fixedXPos(self): # the xPos on grid
        return int(self.xPos)

    @property
    def _fixedYPos(self): # the yPos on grid
        return int(self.yPos)

class Window:
    """
    A game window.
    """
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height

        self.objects: List[Object] = []

    def addObject(self, characters: List[str], xPos: int, yPos: int):
        """
        Adds an object to the object list of the window.

        :params:
        `charaters`: A list of characters (strings) that get displayed from top to bottom.
        `xPos`: The x position. Can also be a float. Will get rounded to int.
        `xPos`: The y position. ^

        :returns:
        The newly created `engine.Object` object.
        """
        object = Object(characters, xPos, yPos)

        self.objects.append(object)
        return object

    def render(self) -> str:
        """
        Renders the window with all its objects.
        :returns:
        The rendered view of the window.
        """
        renderedTiles = np.full((self.height, self.width), " ", dtype=str) # create empty grid for characters
        for object in self.objects:
            for characterPos, character in enumerate(object.characters): # for characters of the Object
                if 0 <= object._fixedYPos-characterPos < self.height and 0 <= object._fixedXPos < self.width: # if the character is in the grid
                    renderedTiles[object._fixedYPos-characterPos, object._fixedXPos] = character # place character in the spot it belongs

        return "\n".join(["".join(row) for row in renderedTiles]) # combines all rows to a string