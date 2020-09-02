import pygame
import tkinter
import sys
import time
from tkinter import messagebox

import Chess
import Utility

#review the chosen game record
def reviewGame(chess,gameTime):
    chess.chooseGame(gameTime)
    chess.drawBackground()
    chess.drawBoard()
    Utility.showText(chess.screen,(700,383),50,'blue','上一步')
    Utility.showText(chess.screen,(700,453),50,'blue','下一步')
    Utility.showText(chess.screen,(700,523),50,'blue','返回')
    num=0

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                #previous drop
                if Utility.isInRect(event.pos,(700,383,850,423)):
                    if num==0:
                        messagebox.showinfo('提示','没有上一步了')
                    else:
                        num-=1
                        chess.drawPartBackground(chess.pieceStack[num])

                #next drop
                elif Utility.isInRect(event.pos,(700,453,850,503)):
                    if num==len(chess.pieceStack):
                        messagebox.showinfo('提示','没有下一步了')
                    else:
                        chess.drawPiece(chess.findPosInScreen(chess.pieceStack[num]),num%2+1)
                        num+=1
                
                #return to select games
                elif Utility.isInRect(event.pos,(700,523,800,573)):
                    return

#show game info on the screen
def showInfo(screen,gameList,page,gameSum):
    screen.fill(pygame.Color('white'))
    Utility.showText(screen,(100,485),70,'blue','上一页')
    Utility.showText(screen,(370,485),70,'blue','下一页')
    Utility.showText(screen,(660,485),70,'blue','返回')
    left=(page-1)*10
    right=min(left+9,gameSum-1)
    for record in range(left,right+1):
        Utility.showText(screen,(125,70+40*(record-left)),30,'black',(' '*4).join(gameList[record]))
    return right-left+1

#select a specific game from datebase and review it
def main():
    pygame.init()
    screen=pygame.display.set_mode((900,600))
    pygame.display.set_caption('历史记录')

    chess=Chess.Chess(screen)
    tkinter.Tk().withdraw()
    gameList=chess.getGameList()
    gameSum=len(gameList)
    maxPage=gameSum//10+1 if gameSum%10 else gameSum//10
    page=1

    if maxPage==0:
        messagebox.showinfo('提示','当前没有历史记录')
        return
    recordCnt=showInfo(screen,gameList,page,gameSum)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                #turn to previous page
                if Utility.isInRect(event.pos,(100,485,310,555)):
                    if page==1:
                        messagebox.showinfo('提示','没有上一页了')
                    else:
                        page-=1
                        recordCnt=showInfo(screen,gameList,page,gameSum)
                
                #turn to next page
                elif Utility.isInRect(event.pos,(370,485,580,555)):
                    if page==maxPage:
                        messagebox.showinfo('提示','没有下一页了')
                    else:
                        page+=1
                        recordCnt=showInfo(screen,gameList,page,gameSum)

                #return to main menu
                elif Utility.isInRect(event.pos,(660,485,800,555)):
                    return
                
                #choose a specific game record
                elif Utility.isInRect(event.pos,(125,70,790,70+recordCnt*40)):
                    num=(event.pos[1]-70)//40
                    reviewGame(chess,gameList[(page-1)*10+num][0])
                    showInfo(screen,gameList,page,gameSum)
        
        pygame.display.update()

#test the module
if __name__=='__main__':
    main()