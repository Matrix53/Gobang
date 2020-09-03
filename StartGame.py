import pygame
import sys
import os

#show text in the screenPos of screen
#size:70 font:华文行楷 color:white range:(x,y) to (x+70*numOfWords,y+70)
def showText(screen,text,screenPos,font):
    textSurface=font.render(text,True,pygame.Color('white'))
    screen.blit(textSurface,screenPos)

#Initialize and create the startup UI
def main():
    pygame.init()
    screen=pygame.display.set_mode((500,600))
    pygame.display.set_caption('开始界面')
    bgImg=pygame.image.load(os.getcwd()+'\source\img\star.jpg')
    screen.blit(bgImg,(0,0))

    font=pygame.font.SysFont('华文行楷',70)
    showText(screen,'单机对战',(115,0),font)
    showText(screen,'人机对战',(115,100),font)
    showText(screen,'联机对战',(115,200),font)
    showText(screen,'历史记录',(115,300),font)
    showText(screen,'视频欣赏',(115,400),font)
    showText(screen,'退出游戏',(115,500),font)
    
    pygame.display.update()

#Test the module
if __name__=='__main__':
    main()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
        
        pygame.display.update()
