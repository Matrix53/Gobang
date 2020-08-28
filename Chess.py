import pygame
import sys

'''
Class Chess is used to represent the game, and here're some settings.

postion:
    A Tuple. Represent the position of a piece, ans pos[0] is the abscissa.
    The origin is on the left top, and the x-axis is horizontal.

player:
    An integer. 1 means the black side, 2 means the white side, 0 means nothing.
    The black side always drops pieces first.

board:
    A 2D list of int. board[x][y] means which side the piece in (x,y) is belonged to.

pieceStack:
    A stack of pos. The stack is used to record the game and implement undoing a drop.

playerName:
    The name of a player. Only be used in PVP mode.

screen:
    The screen surface. Length:900 Height:600

dotSequence:
    A list of pos. Only be used to draw the board.

other settings:
    Board size:15*15  Grid length:39  Piece radius:14
    Top margin length:27  Left margin length:54  Gridlines' thickness:2

'''
class Chess:
    #initialize the board
    def __init__(self):
        self.board=[[0 for i in range(0,15)] for j in range(0,15)]
        self.pieceStack=[]
        self.dotSequence=[(i//2*39+54,573 if (i%4==1 or i%4==2) else 27) for i in range(0,30)]
        self.dotSequence+=[(54 if (i%4==1 or i%4==2) else 600,573-i//2*39) for i in range(0,30)]

    def drawBoard(self,screen):
        pygame.draw.lines(screen,pygame.Color('black'),False,self.dotSequence,2)
        pygame.display.update()

    def drawPiece(self,pos,player):
        pass
    
    def drawAllPieces(self):
        pass

    def drawPlayer(self,player,playerName=''):
        pass

    #fill background with special brown
    def drawBackground(self,screen):
        screen.fill((255,128,64))
        pygame.display.update()
    
    def isWinner(self,pos):
        pass

    def dropPiece(self,pos,player):
        pass

    def undoDrop(self):
        pass

#The function is used to test the Chess Class
def unitTest():
    pygame.init()
    screen=pygame.display.set_mode((900,600))
    chess=Chess()
    chess.drawBackground(screen)
    chess.drawBoard(screen)

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
        pygame.display.update()

if __name__=='__main__':
    unitTest()