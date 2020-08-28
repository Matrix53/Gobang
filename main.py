import pygame
from sys import exit
import startGame
import playInOnePC

screen=startGame.main()

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()
    
    pygame.display.update()