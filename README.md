# PORTFOLIO-ASSIGNMENT-CS325
######Author: Madison Woy
##Introduction
LIGHT_UP.py is an implementation of the 'light-up' game which is an example of an np-complete
problem. This program will allow the user to play the game and then verify their solution.

 - The program will verify a given solution but cannot verify if no input is given.
 - The program will check for the simplest 'unsolvable' boards and will reset itself if one is generated
     - NOTE: it is still possible for the game to display an 'unsolvable' board, for the program
            to only display solvable boards it would need to be able to solve a board on its own
            which has been shown to be NP-complete

##Implementation
To install needed packages please run the following in the terminal (assuming pip is installed):
        pip install PyQt5
Instructions to install pip can be found here:
        https://pip.pypa.io/en/stable/installing/
##Game Rules
###Goal
The goal of "Light Up" is to place lights on a given board so that all the tiles on the board are lit
###Limitations
Lights can be placed on any white square with the following exceptions:
    - Two lights cannot be in the same row or column unless a black square falls in between them
    - A black tile with a value in it MUST have the same number of lights surrounding it as the value of the tile
        - Ex: A black tile containing a "0" cannot have a light in any of its 4 adjacent tiles
        _ Ex: A black tile containing a "1" must have at least one light in any of its 4 adjacent tiles
###User Interface
**White Tiles:** Tiles that are not lights and are not affected by a beam of light
**Black Tiles:** Tiles that cannot be interacted with, any beam of light that hits a black square will break
**Orange Tiles:** Tiles that are lights, will emit a beam of light until a black square or the edge of the board is reached
**Red Tiles:** Tiles that are lights but are invalid due to the fact that they are on the same row or column as another light
**Gray Tiles:** Tiles that are adjacent to a black square that has too many lights adjacent to it