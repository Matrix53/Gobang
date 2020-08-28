import pygame

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
    The name of a player. Only used in PVP mode.

screen:
    The screen surface. Length:900 Height:600

'''
class Chess:
    #initialize the board
    def __init__(self):
        self.board=[[0 for i in range(0,15)] for j in range(0,15)]
        self.pieceStack=[]

    def drawBoard(self):
        pass

    def drawPiece(self,pos):
        pass
    
    def drawAllPieces(self):
        pass

    def drawPlayer(self,player,playerName=''):
        pass

    #fill background with special brown
    def drawBackground(self,screen):
        screen.fill((255,128,64))
    
    def isWinner(self,pos):
        pass

    def dropPiece(self,pos,player):
        pass

    def undoDrop(self):
        pass

#The function is used to test the Chess Class
def unitTest():
    pass

if __name__=='__main__':
    unitTest()