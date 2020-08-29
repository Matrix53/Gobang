import pygame
from sys import exit
from Chess import Chess

def main():
    pygame.init()
    screen=pygame.display.set_mode((900,600))
    pygame.display.set_caption('单机对战')

    chess=Chess(screen)
    chess.drawBackground()
    chess.drawBoard()

    font=pygame.font.SysFont('华文行楷',50)
    returnText=font.render('返回',True,pygame.Color('black'))
    screen.blit(returnText,(700,523))
    undoText=font.render('悔棋',True,pygame.Color('black'))
    screen.blit(undoText,(700,453))
    defeatText=font.render('认输',True,pygame.Color('black'))
    screen.blit(defeatText,(700,383))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                x,y=event.pos
                if chess.isInBoard(event.pos):
                    pass
                
        
        pygame.display.update()

#test the module
if __name__=='__main__':
    main()
