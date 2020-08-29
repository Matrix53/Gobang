import pygame
import sys

'''
Class Chess is used to represent the game, and here're some settings.

postion(pos):
    A Tuple. Represent the position of a piece in board, and pos[0] is the abscissa.
    The origin is on the left top, and the x-axis is horizontal.

screenPos:
    A tuple. Represent the position of a pixel in screen.

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
    
    #if player in pos wins, return True, else return False
    #Winning the game requires 5 pieces in the same color row in one line
    #search from (left,top) to (right,down) to judge whether the player wins
    def isWinner(self,pos):
        #find the scope
        x,y=pos
        player=self.board[x][y]
        top,down=max(0,y-4),min(14,y+4)
        left,right=max(0,x-4),min(14,x+4)

        #case1:search from (pos[0],top) to (pos[0],down)
        y,cnt=top,0
        while y<=down:
            if self.board[x][y]==player:
                cnt+=1
            else:
                cnt=0
            if cnt==5:
                return True
            y+=1
        
        #case2:search from (left,pos[1]) to (right,pos[1])
        x,y,cnt=left,pos[1],0
        while x<=right:
            if self.board[x][y]==player:
                cnt+=1
            else:
                cnt=0
            if cnt==5:
                return True
            x+=1
        
        #case3:search from lefttop to rightdown and assure the searching scope is a square
        deltaX,deltaY=pos[0]-left,pos[1]-top
        if deltaX<deltaY:
            x,y,cnt=left,pos[1]-deltaX,0
        else:
            x,y,cnt=pos[0]-deltaY,top,0

        while x<=right and y<=down:
            if self.board[x][y]==player:
                cnt+=1
            else:
                cnt=0
            if cnt==5:
                return True
            x+=1
            y+=1

        #case4:search from leftdown to righttop and assure the searching scope is a square
        deltaX,deltaY=pos[0]-left,down-pos[1]
        if deltaX<deltaY:
            x,y,cnt=left,pos[1]+deltaX,0
        else:
            x,y,cnt=pos[0]-deltaY,down,0

        while x<=right and y>=top:
            if self.board[x][y]==player:
                cnt+=1
            else:
                cnt=0
            if cnt==5:
                return True
            x+=1
            y-=1

        #case5:The player doesn't win
        return False

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
    
    def isInBoard(self,screenPos):
        x,y=screenPos
        if x>=40 and x<=614 and y>=13 and y<=587:
            return True
        else:
            return False

    #In this function,screenPos must be in board
    def findPosInBoard(self,screenPos):
        x,y=screenPos
        return (round((x-54)/39),round((y-27)/39))

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