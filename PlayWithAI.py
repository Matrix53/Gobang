import pygame
import sys

import Utility

def main():
    pygame.init()
    screen=pygame.display.set_mode((900,600))
    pygame.display.set_caption('人机对战')
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                pass
        pygame.display.update()

#test the module
if __name__=='__main__':
    main()