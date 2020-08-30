import pygame
import sys
import time

import Chess
import Utility

def main():
    pygame.init()
    screen=pygame.display.set_mode((900,600))
    pygame.display.set_caption('单机对战')

    chess=Chess.Chess(screen)
    chess.drawBackground()
    chess.drawBoard()

    font=pygame.font.SysFont('华文行楷',50)
    returnText=font.render('返回',True,pygame.Color('black'))
    screen.blit(returnText,(700,523))
    undoText=font.render('悔棋',True,pygame.Color('black'))
    screen.blit(undoText,(700,453))
    defeatText=font.render('认输',True,pygame.Color('black'))
    screen.blit(defeatText,(700,383))

    chess.drawPlayer(1)
    pygame.display.update()

    #use player to control which side is going to drop pieces
    #1 means black side. 2 means white side. the same as Chess.py
    player=1

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONUP:
                #drop a piece
                if chess.isInBoard(event.pos):
                    pos=chess.findPosInBoard(event.pos)
                    if chess.board[pos[0]][pos[1]]==3-player:
                        continue
                    chess.dropPiece(pos,player)
                    if chess.isWinner(pos):
                        chess.drawWinner(player)
                        time.sleep(1)
                        return
                    player=3-player
                    chess.drawPlayer(player)

                #return to main menu
                elif Utility.isInRect(event.pos,(700,523,800,573)):
                    return

                #undo a drop
                elif Utility.isInRect(event.pos,(700,453,800,503)):
                    chess.undoDrop()
                    player=3-player
                    chess.drawPlayer(player)

                #one side give up
                elif Utility.isInRect(event.pos,(700,383,800,433)):
                    chess.drawWinner(3-player)
                    time.sleep(1)
                    return
                
        pygame.display.update()

#test the module
if __name__=='__main__':
    main()
