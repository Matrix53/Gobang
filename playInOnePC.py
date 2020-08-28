import pygame
from sys import exit
from Chess import Chess

def main():
    pygame.init()
    screen=pygame.display.set_mode((900,600))
    pygame.display.set_caption('单机对战')
    chess=Chess()

if __name__=='__main__':
    main()
