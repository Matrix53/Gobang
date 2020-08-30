import pygame
import sys

import Utility
import startGame
import playInOnePC
import playInLAN

startGame.main()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.MOUSEBUTTONUP:
            #mode:play in one PC
            if Utility.isInRect(event.pos,(115,100,395,170)):
                playInOnePC.main()
                startGame.main()

            #mode:play in LAN
            if Utility.isInRect(event.pos,(115,200,395,270)):
                playInLAN.main()
                startGame.main()

            #exit the game
            elif Utility.isInRect(event.pos,(115,300,395,370)):
                sys.exit()
    
    pygame.display.update()