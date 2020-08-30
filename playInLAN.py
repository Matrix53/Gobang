import pygame
import sys
import time
import socket

import Utility
import Chess

def main():
    screen=pygame.display.set_mode(900,600)
    pygame.display.set_caption('联机对战')

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
        
        pygame.display.update()

#test the module
if __name__=='__main__':
    main()