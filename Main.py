import pygame
import sys

import Utility
import StartGame
import PlayInOnePC
import PlayWithAI
import PlayInLAN
import WatchVideo
import ReviewHistory

StartGame.main()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.MOUSEBUTTONUP:
            #mode:play in one PC
            if Utility.isInRect(event.pos,(115,0,395,70)):
                PlayInOnePC.main()
                StartGame.main()

            #mode:play with AI
            elif Utility.isInRect(event.pos,(115,100,395,170)):
                PlayWithAI.main()
                StartGame.main()

            #mode:play in LAN
            elif Utility.isInRect(event.pos,(115,200,395,270)):
                PlayInLAN.main()
                StartGame.main()

            #mode:review history
            elif Utility.isInRect(event.pos,(115,300,395,370)):
                ReviewHistory.main()
                StartGame.main()
            
            #mode:watch video
            elif Utility.isInRect(event.pos,(115,400,395,470)):
                WatchVideo.main()
                StartGame.main()

            #exit the game
            elif Utility.isInRect(event.pos,(115,500,395,570)):
                sys.exit()
    
    pygame.display.update()