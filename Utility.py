import pygame

'''
Pygame has the function to finish the task
Use this function to lower the memory consumpution in maintaining the Rect object

screenPos:2 elements tuple.Elem means x,y in order
rect:4 elements tuple.Elem means left,top,right,bottom in order
''' 
def isInRect(screenPos,rect):
    x,y=screenPos
    left,top,right,bottom=rect
    if x>=left and x<=right and y>=top and y<=bottom:
        return True
    else:
        return False

'''
Show text in the screenPos on the screen

screen:screen surface.
screenPos:2 elements tuple. (x,y) is the topleft of the text
size:an integer. Determine the size of the text
color:a string. Determine the color of the text
textfont:华文行楷
'''
def showText(screen,screenPos,size,color,text):
    font=pygame.font.SysFont('华文行楷',size)
    textSurface=font.render(text,True,pygame.Color(color))
    screen.blit(textSurface,screenPos)
    pygame.display.update()