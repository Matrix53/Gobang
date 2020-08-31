import re
import requests
import webbrowser 
import pygame
import sys
import random
from bs4 import BeautifulSoup

import Utility

'''
refresh the info showed to player
choose videos randomly from the bilibili searching engine
there'll be 10 records showed in the screen at the same time

screen:A screen surface which you want to show info in
return:A website URL(str) list corresponds to the info
'''
def refreshInfo(screen):
    screen.fill(pygame.Color('white'))
    Utility.showText(screen,(210,485),70,'blue','刷新')
    Utility.showText(screen,(550,485),70,'blue','返回')
    page=str(random.randint(1,50))
    webSourceCode=requests.get('https://search.bilibili.com/video?keyword=五子棋&page='+page).text
    webSoup=BeautifulSoup(webSourceCode,'lxml')
    webList=[]
    for tag in webSoup.find_all(attrs={'target':"_blank",'class':"img-anchor"}):
        Utility.showText(screen,(50,100+len(webList)*35),25,'black',tag.attrs['title'][:30])
        webList.append(tag.attrs['href'].strip('/'))
        if len(webList)>=10:
            break
    return webList

def main():
    pygame.init()
    screen=pygame.display.set_mode((900,600))
    pygame.display.set_caption('视频欣赏')
    webList=refreshInfo(screen)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                #refresh the info
                if Utility.isInRect(event.pos,(210,485,350,555)):
                    webList=refreshInfo(screen)

                #return to the main menu
                elif Utility.isInRect(event.pos,(550,485,690,555)):
                    return

                #use browser to browse the web
                elif Utility.isInRect(event.pos,(50,100,800,440)):
                    webbrowser.open(webList[(event.pos[1]-100)//35])

        pygame.display.update()

#test the module
if __name__=='__main__':
    main()