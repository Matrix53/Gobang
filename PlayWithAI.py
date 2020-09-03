import pygame
import sys
import tkinter
import time
from tkinter import messagebox

import Utility
import Chess

def main():
    pygame.init()
    screen=pygame.display.set_mode((900,600))
    pygame.display.set_caption('人机对战')
    chess=Chess.Chess(screen)
    chess.drawBackground()
    chess.drawBoard()
    Utility.showText(screen,(700,523),50,'blue','返回')
    Utility.showText(screen,(700,453),50,'blue','悔棋')
    pygame.display.update()

    tkinter.Tk().withdraw()
    isBlack=messagebox.askyesno('询问','是否要执黑棋先行')
    chess.openAI()

    while True:
        if not isBlack:
            pos=chess.askAIForPos()
            chess.dropPiece(pos,1)
            if chess.isWinner(pos):
                chess.drawWinner(1)
                chess.recordGame('人机对战','我方执白','黑方胜')
                time.sleep(1)
                return

        alreadyDrop=False
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONUP:
                    #return to main menu
                    if Utility.isInRect(event.pos,(700,523,800,573)):
                        return

                    #undo a drop
                    elif Utility.isInRect(event.pos,(700,453,800,503)):
                        chess.undoDrop()
                        chess.undoDrop()

                    #drop a piece
                    elif chess.isInBoard(event.pos):
                        pos=chess.findPosInBoard(event.pos)
                        if chess.board[pos[0]][pos[1]]!=0:
                            continue
                        chess.dropPiece(pos,1 if isBlack else 2)
                        if chess.isWinner(pos):
                            if isBlack:
                                chess.drawWinner(1)
                                chess.recordGame('人机对战','我方执黑','黑方胜')
                            else:
                                chess.drawWinner(2)
                                chess.recordGame('人机对战','我方执白','白方胜')
                            time.sleep(1)
                            return
                        alreadyDrop=True
                        break
            pygame.display.update()
            if alreadyDrop:
                break

        if isBlack:
            pos=chess.askAIForPos()
            chess.dropPiece(pos,2)
            if chess.isWinner(pos):
                chess.drawWinner(2)
                chess.recordGame('人机对战','我方执黑','白方胜')
                time.sleep(1)
                return

#test the module
if __name__=='__main__':
    main()