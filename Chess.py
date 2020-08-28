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
    Background Color:(255,128,64)

'''
class Chess:
    #initialize the board
    def __init__(self,screenSurface):
        self.board=[[0 for i in range(0,15)] for j in range(0,15)]
        self.pieceStack=[]
        self.dotSequence=[(i//2*39+54,573 if (i%4==1 or i%4==2) else 27) for i in range(0,30)]
        self.dotSequence+=[(54 if (i%4==1 or i%4==2) else 600,573-i//2*39) for i in range(0,30)]
        self.screen=screenSurface

    def drawBoard(self):
        pygame.draw.lines(self.screen,pygame.Color('black'),False,self.dotSequence,2)
        pygame.display.update()

    def drawPiece(self,pos,player):
        if player==0:
            return
        elif player==1:
            pygame.draw.circle(self.screen,pygame.Color('black'),pos,14)
        else:
            pygame.draw.circle(self.screen,pygame.Color('white'),pos,14)
        pygame.display.update()
    
    def drawAllPieces(self):
        for x in range(0,15):
            for y in range(0,15):
                self.drawPiece((x,y),self.board[x][y])

    def drawPlayer(self,player,playerName=''):
        font=pygame.font.SysFont('华文行楷',30)

        if player==1:
            promptText=font.render('轮到黑方行棋',True,pygame.Color('black'))
        else:
            promptText=font.render('轮到白方行棋',True,pygame.Color('white'))
        self.screen.blit(promptText,(650,27))

        if playerName!='':
            nameText=font.render('玩家:'+playerName,True,pygame.Color('blue'))
            self.screen.blit(nameText,(650,67))

        pygame.display.update()

    #fill background with special brown
    def drawBackground(self):
        self.screen.fill((255,128,64))
        pygame.display.update()
    
    def isWinner(self,pos):
        pass

    def dropPiece(self,pos,player):
        self.pieceStack.append(pos)
        self.board[pos[0]][pos[1]]=player
        self.drawPiece(pos,player)

    def undoDrop(self):
        pos=self.pieceStack.pop()
        self.board[pos[0]][pos[1]]=0
        pygame.draw.circle(self.screen,(255,128,64),pos,14)
        pygame.draw.line(self.screen,pygame.Color('black'),(pos[0]-14,pos[1]),(pos[0]+14,pos[1]),2)
        pygame.draw.line(self.screen,pygame.Color('black'),(pos[0],pos[1]-14),(pos[0],pos[1]+14),2)
        pygame.display.update()

#The function is used to test the Chess Class
def unitTest():
    pygame.init()
    screen=pygame.display.set_mode((900,600))
    chess=Chess(screen)
    chess.drawBackground()
    chess.drawBoard()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
        pygame.display.update()

if __name__=='__main__':
    unitTest()