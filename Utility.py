'''
Pygame has the function to finish the task
Use this function to lower the memory consumpution in maintaining the Rect object

pos:2 elements tuple.Elem means x,y in order
rect:4 elements tuple.Elem means left,top,right,bottom in order
''' 
def isInRect(pos,rect):
    x,y=pos
    left,top,right,bottom=rect
    if x>=left and x<=right and y>=top and y<=bottom:
        return True
    else:
        return False