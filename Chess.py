import pygame
import sys
import os
import sqlite3
import datetime
import random

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

gameTime:
    A string. Represent the time of finishing the game.

dbCon:
    The connect object between database and program.

dbCur:
    The cursor object between database and program.

other settings:
    Board size:15*15  Grid length:39  Piece radius:14
    Top margin length:27  Left margin length:54  Gridlines' thickness:2
    Background Color:(255,128,64)  Database path:now\source\\record\PlayHistory.db

'''
class Chess:
    #initialize the board
    def __init__(self,screenSurface=None):
        self.board=[[0 for i in range(0,15)] for j in range(0,15)]
        self.pieceStack=[]
        self.dotSequence=[(i//2*39+54,573 if (i%4==1 or i%4==2) else 27) for i in range(0,30)]
        self.dotSequence+=[(54 if (i%4==1 or i%4==2) else 600,573-i//2*39) for i in range(0,30)]
        self.screen=screenSurface
        self.dbCon=sqlite3.connect(os.getcwd()+'\source\\record\PlayHistory.db')
        self.dbCur=self.dbCon.cursor()
        self.valJudge=[]
        self.blackPiece=pygame.image.load(os.getcwd()+'\source\img\\blackStone.png')
        self.whitePiece=pygame.image.load(os.getcwd()+'\source\img\\whiteStone.png')
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load(os.getcwd()+'\source\sound\drop.wav')

    #Close the connection to database
    def __del__(self):
        self.dbCur.close()
        self.dbCon.close()

    def drawBoard(self):
        pygame.draw.lines(self.screen,pygame.Color('black'),False,self.dotSequence,2)
        pygame.display.update()

    def drawPiece(self,screenPos,player):
        x,y=screenPos
        if player==0:
            return
        elif player==1:
            self.screen.blit(self.blackPiece,(x-14,y-14))
        else:
            self.screen.blit(self.whitePiece,(x-14,y-14))
        pygame.mixer.music.play()
        pygame.display.update()
    
    def drawAllPieces(self):
        for x in range(0,15):
            for y in range(0,15):
                screenPos=self.findPosInScreen(x,y)
                self.drawPiece(screenPos,self.board[x][y])

    def drawPlayer(self,player,playerName=''):
        font=pygame.font.Font(os.getcwd()+'\source\\font\华文行楷.ttf',30)

        pygame.draw.rect(self.screen,(255,128,64),pygame.Rect(650,27,180,30))
        if player==1:
            promptText=font.render('轮到黑方行棋',True,pygame.Color('black'))
        else:
            promptText=font.render('轮到白方行棋',True,pygame.Color('white'))
        self.screen.blit(promptText,(650,27))

        if playerName!='':
            nameText=font.render('玩家:'+playerName,True,pygame.Color('blue'))
            self.screen.blit(nameText,(650,67))

        pygame.display.update()

    def drawWinner(self,player,playerName=''):
        font=pygame.font.Font(os.getcwd()+'\source\\font\华文行楷.ttf',100)
        if player==1:
            winnerText=font.render('黑方胜',True,pygame.Color('red'))
        else:
            winnerText=font.render('白方胜',True,pygame.Color('red'))
        self.screen.blit(winnerText,(177,127))

        if playerName!='':
            font=pygame.font.Font(os.getcwd()+'\source\\font\华文行楷.ttf',40)
            playerText=font.render('玩家:'+playerName,True,pygame.Color('blue'))
            self.screen.blit(playerText,(177,237))

        pygame.display.update()

    #fill background with special brown
    def drawBackground(self):
        boardImg=pygame.image.load(os.getcwd()+'\source\img\\board.png')
        self.screen.fill((255,128,64))
        self.screen.blit(boardImg,(40,13))
        pygame.display.update()
    
    def drawPartBackground(self,pos):
        x,y=self.findPosInScreen(pos)
        boardImg=pygame.image.load(os.getcwd()+'\source\img\\board.png')
        self.screen.blit(boardImg,(x-15,y-15),pygame.Rect(x-55,y-28,30,30))
        pygame.draw.line(self.screen,pygame.Color('black'),(x-15,y),(x+15,y),2)
        pygame.draw.line(self.screen,pygame.Color('black'),(x,y-15),(x,y+15),2)
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
        screenPos=self.findPosInScreen(pos)
        self.drawPiece(screenPos,player)

    def undoDrop(self):
        pos=self.pieceStack.pop()
        self.board[pos[0]][pos[1]]=0
        self.drawPartBackground(pos)
    
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

    def findPosInScreen(self,pos):
        x,y=pos
        return (54+39*x,27+39*y)

    #Record the game into the database
    def recordGame(self,mode,color,result):
        self.dbCur.execute('create table if not exists history(time primary key,mode,color,result,game)')
        gameTime=datetime.datetime.now().strftime('%F %T')
        dotStr=self.listToStr()
        self.dbCur.execute('insert into history values(?,?,?,?,?)',(gameTime,mode,color,result,dotStr))
        self.dbCon.commit()
        
    #Read the game records from the database
    def getGameList(self):
        self.dbCur.execute('create table if not exists history(time primary key,mode,color,result,game)')
        self.dbCur.execute('select time,mode,color,result from history')
        gameList=[]
        for record in self.dbCur:
            gameList.append(record)
        gameList.sort(key=lambda x:datetime.datetime.strptime(x[0],'%Y-%m-%d %H:%M:%S'))
        gameList.reverse()
        return gameList

    def chooseGame(self,gameTime):
        self.dbCur.execute('select game from history where time="%s"'%gameTime)
        for record in self.dbCur:
            self.pieceStack=self.strToList(record[0])

    #Convert dotSequence to string to store
    def listToStr(self):
        dotStr=''
        for dot in self.pieceStack:
            dotStr+=str(dot[0])+','+str(dot[1])+':'
        return dotStr.strip(':')
    
    #Convert string to dotSequence to read
    def strToList(self,dotStr):
        dotSet=dotStr.split(':')
        dotList=[]
        for dot in dotSet:
            x,y=map(int,dot.split(','))
            dotList.append((x,y))
        return dotList
    
    #return a pos that AI wants to drop a piece in
    def askAIForPos(self):
        player=len(self.pieceStack)%2+1
        posList=[]
        maxVal=0
        for x in range(0,15):
            for y in range(0,15):
                if self.board[x][y]==0:
                    tmpVal=self.getValOfPos((x,y),player)
                    if tmpVal>maxVal:
                        posList.clear()
                        posList.append((x,y))
                        maxVal=tmpVal
                    elif tmpVal==maxVal:
                        posList.append((x,y))
        return random.choice(posList)

    #return the value of pos in the opinion of AI
    def getValOfPos(self,pos,player):
        x,y=pos
        sum=0
        sum+=self.valJudge[player-1][self.getPieceStr((x,y-3),(x,y-1))]
        sum+=self.valJudge[player-1][self.getPieceStr((x-3,y-3),(x-1,y-1))]
        sum+=self.valJudge[player-1][self.getPieceStr((x-3,y),(x-1,y))]
        sum+=self.valJudge[player-1][self.getPieceStr((x-3,y+3),(x-1,y+1))]
        sum+=self.valJudge[player-1][self.getPieceStr((x,y+3),(x,y+1))]
        sum+=self.valJudge[player-1][self.getPieceStr((x+3,y+3),(x+1,y+1))]
        sum+=self.valJudge[player-1][self.getPieceStr((x+3,y),(x+1,y))]
        sum+=self.valJudge[player-1][self.getPieceStr((x+3,y-3),(x+1,y-1))]
        return sum

    #get a string of pieces from pos1 to pos2
    def getPieceStr(self,pos1,pos2):
        ansStr=''
        x1,y1=pos1
        x2,y2=pos2
        deltaX,deltaY=(x2-x1)//2,(y2-y1)//2
        for step in range(0,3):
            if x1<0 or x1>14 or y1<0 or y1>14:
                ansStr+='3'
            else:
                ansStr+=str(self.board[x1][y1])
            x1+=deltaX
            y1+=deltaY
        return ansStr

    def openAI(self):
        with open(os.getcwd()+'\source\AI\\blackSideRef.txt','r') as ref:
            tmpDict={}
            for line in ref:
                pair=line.strip().split(':')
                tmpDict[pair[0]]=int(pair[1])
            self.valJudge.append(tmpDict)
        with open(os.getcwd()+'\source\AI\\whiteSideRef.txt','r') as ref:
            tmpDict={}
            for line in ref:
                pair=line.strip().split(':')
                tmpDict[pair[0]]=int(pair[1])
            self.valJudge.append(tmpDict)

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