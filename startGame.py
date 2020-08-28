import pygame
from sys import exit

pygame.init()
textFont=pygame.font.SysFont('华文行楷',70)
screen=pygame.display.set_mode((500,600))

#show text in the pos of screen
#size:70 font:华文行楷 color:white range:(x,y) to (x+70*numOfWords,y+70)
def showText(text,pos):
    global textFont
    global screen
    textSurface=textFont.render(text,True,pygame.Color('white'))
    screen.blit(textSurface,pos)
    pygame.display.update()
    return

#Initialize and create the startup UI
def main():
    global screen
    pygame.init()
    pygame.display.set_caption('开始界面')
    screen.fill(pygame.Color('blue'))
    showText('单机对战',(115,100))
    showText('退出游戏',(115,200))
    return screen

#Test the module
if __name__=='__main__':
    tmpScreen=main()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()
        
        pygame.display.update()
