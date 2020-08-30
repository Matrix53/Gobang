import pygame
import sys
import time
import socket
import tkinter
from tkinter import messagebox

import Utility
import Chess

def main():
    pygame.init()
    screen=pygame.display.set_mode((900,600))
    pygame.display.set_caption('联机对战')
    screen.fill(pygame.Color('white'))
    Utility.showText(screen,(150,270),60,'black','请使用控制台进行联机')
    chess=Chess.Chess(screen)
    tkinter.Tk().withdraw()

    #record player's name
    myName=input('请输入您的游戏昵称:')
    #use UDP to communicate. port:8001
    myAddress=(socket.gethostname(),8001)
    mySocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    mySocket.bind(myAddress)

    #choose to be the server or the client
    #1 represents the client(black side), and 2 represents the server(white side)
    print('\n请输入数字选择您的联机方式:')
    print('1.填入对方的IP地址主动联机')
    print('2.等待他人连接到本设备')
    choice=int(input('您的选择是:'))
    
    '''
    oppe is short for opposite in this file
    msg is short for message in this file
    exchange initial info in this part
    '''
    if choice==1:
        oppoAddress=(input('请输入对方的IP地址(对方此时必须处于等待状态):'),8001)
        mySocket.sendto(myName.encode(),oppoAddress)
        print('\n正在联机...')
        recvMsg=mySocket.recvfrom(1024)
        oppoName=recvMsg[0].decode()
    else:
        print('\n请等待他人的联机...')
        recvMsg=mySocket.recvfrom(1024)
        oppoAddress=recvMsg[1]
        oppoName=recvMsg[0].decode()
        mySocket.sendto(myName.encode(),oppoAddress)

    #perform initialization
    print('游戏开始!')
    chess.drawBackground()
    chess.drawBoard()
    font=pygame.font.SysFont('华文行楷',50)
    returnText=font.render('返回',True,pygame.Color('black'))
    screen.blit(returnText,(700,523))
    undoText=font.render('悔棋',True,pygame.Color('black'))
    screen.blit(undoText,(700,453))
    defeatText=font.render('认输',True,pygame.Color('black'))
    screen.blit(defeatText,(700,383))

    #choice has the same value as player
    if choice==1:
        chess.drawPlayer(1,myName)
    else:
        chess.drawPlayer(1,oppoName)

    '''
    start the game, and here're some msg instructions
    msg content(str):
        exit:it means the opponent exits the game
        win:it means the opponent chooses to give up
        undo:it means the opponent undoes a drop(only in your turn can you undo drops)
            admit:it means you admit the undoing request of the opponent
            reject:it means you reject the undoing request of the opponent
        x,y:it means the opponent drop a piece at (x,y)
    '''
    while True:

        #the server receives msg here
        if choice==2:
            while True:
                recvMsg=mySocket.recvfrom(1024)
                recvStr=recvMsg[0].decode()
                if recvStr=='exit':
                    screen.fill(pygame.Color('white'))
                    Utility.showText(screen,(240,270),60,'black','对方离开了游戏')
                    time.sleep(1)
                    mySocket.close()
                    return
                elif recvStr=='win':
                    messagebox.showinfo('提示','对方选择认输')
                    chess.drawWinner(choice,myName)
                    time.sleep(1)
                    mySocket.close()
                    return
                elif recvStr=='undo':
                    admitUndo=messagebox.askyesno('提示','对方请求悔棋，是否同意?')
                    if admitUndo:
                        mySocket.sendto('admit'.encode(),oppoAddress)
                        chess.undoDrop()
                        chess.undoDrop()
                    else:
                        mySocket.sendto('reject'.encode(),oppoAddress)
                    continue
                else:
                    x,y=map(int,recvStr.split(','))
                    chess.dropPiece((x,y),3-choice)
                    if chess.isWinner((x,y)):
                        chess.drawWinner(3-choice,oppoName)
                        time.sleep(1)
                        mySocket.close()
                        return
                    chess.drawPlayer(choice,myName)
                    break
        
        #use while loop to assure the player(server or client) doing an efficient operation
        alreadyDrop=False
        while True:
            #use for loop to deal with events
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    mySocket.sendto('exit'.encode(),oppoAddress)
                    mySocket.close()
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONUP:
                    #drop a piece
                    if chess.isInBoard(event.pos):
                        pos=chess.findPosInBoard(event.pos)
                        if chess.board[pos[0]][pos[1]]!=0:
                            continue
                        chess.dropPiece(pos,choice)
                        mySocket.sendto(str(pos).strip('()').encode(),oppoAddress)
                        if chess.isWinner(pos):
                            chess.drawWinner(choice,myName)
                            time.sleep(1)
                            mySocket.close()
                            return
                        chess.drawPlayer(3-choice,oppoName)
                        alreadyDrop=True
                        break
                    #return to main menu
                    elif Utility.isInRect(event.pos,(700,523,800,573)):
                        mySocket.sendto('exit'.encode(),oppoAddress)
                        mySocket.close()
                        return
                    #undo a drop
                    elif Utility.isInRect(event.pos,(700,453,800,503)):
                        mySocket.sendto('undo'.encode(),oppoAddress)
                        recvMsg=mySocket.recvfrom(1024)
                        recvStr=recvMsg[0].decode()
                        if recvStr=='admit':
                            chess.undoDrop()
                            chess.undoDrop()
                        continue
                    #give up the game
                    elif Utility.isInRect(event.pos,(700,383,800,433)):
                        mySocket.sendto('win'.encode(),oppoAddress)
                        chess.drawWinner(3-choice,oppoName)
                        time.sleep(1)
                        mySocket.close()
                        return
            #break the while loop
            if alreadyDrop:
                break

        
        #the client receives msg here
        if choice==1:
            while True:
                recvMsg=mySocket.recvfrom(1024)
                recvStr=recvMsg[0].decode()
                if recvStr=='exit':
                    screen.fill(pygame.Color('white'))
                    Utility.showText(screen,(240,270),60,'black','对方离开了游戏')
                    time.sleep(1)
                    mySocket.close()
                    return
                elif recvStr=='win':
                    messagebox.showinfo('提示','对方选择认输')
                    chess.drawWinner(choice,myName)
                    time.sleep(1)
                    mySocket.close()
                    return
                elif recvStr=='undo':
                    admitUndo=messagebox.askyesno('提示','对方请求悔棋，是否同意?')
                    if admitUndo:
                        mySocket.sendto('admit'.encode(),oppoAddress)
                        chess.undoDrop()
                        chess.undoDrop()
                    else:
                        mySocket.sendto('reject'.encode(),oppoAddress)
                    continue
                else:
                    x,y=map(int,recvStr.split(','))
                    chess.dropPiece((x,y),3-choice)
                    if chess.isWinner((x,y)):
                        chess.drawWinner(3-choice,oppoName)
                        time.sleep(1)
                        mySocket.close()
                        return
                    chess.drawPlayer(choice,myName)
                    break
        
        pygame.display.update()

#test the module
if __name__=='__main__':
    main()