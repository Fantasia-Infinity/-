# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 22:57:11 2018

@author: Fantasia
"""

import pygame
import random

pgrow=0.003
pburn=0.00001
class Unit:
    def __init__(self,state):
        self.state=state#0空地 1树木 2燃烧 3灰烬
class Forest:
    def __init__(self,n):
        self.ground=[]
        self.n=n
        for i in range(n):
            self.ground.append([])
        for l in self.ground:
            for i in range(n):
                l.append(Unit(0))
    def z(self,x,y):
        return x,y-1
    def y(self,x,y):
        if y!=self.n-1:
            return x,y+1
        else:
            return x,0
    def s(self,x,y):
        return x-1,y
    def x(self,x,y):
        if x!=self.n-1:
            return x+1,y
        else:
            return 0,y
    def zs(self,x,y):
        return self.s(*self.z(x,y))
    def zx(self,x,y):
        return self.x(*self.z(x,y))
    def ys(self,x,y):
        return self.s(*self.y(x,y))
    def yx(self,x,y):
        return self.x(*self.y(x,y))
    fl=[z,y,s,x,zs,zx,ys,yx]
    def upper(self,x,y):
        state=self.ground[x][y].state
        if(state==0 or state==3):
            if(random.random()<pgrow):
                return Unit(1)
            else:
                return Unit(state)
        elif(state==1):
            nearburn=False
            for f in self.fl:
                if self.ground[f(self,x,y)[0]][f(self,x,y)[1]].state==2:
                    nearburn=True
                    break
            if(nearburn==True):
                return Unit(2)
            else:
                if(random.random()<pburn):
                    return Unit(2)
                else:
                    return Unit(1)
        elif(state==2):
            return Unit(3)
    def update(self):
        newground=[]
        for i in range(self.n):
            newground.append([])
        for l in newground:
            for i in range(self.n):
                l.append(Unit(0))
        for i in range(self.n):
            for j in range(self.n):
                newground[i][j]=self.upper(i,j)
        self.ground=newground
    
    
    

BLUE=(0,0,255)
BLACK=(0,0,0)
GREEN=(0,255,0)
RED=(255,0,0)
YR=(200,100,200)
GREY=(100,100,100)
R=(255,255,0)
print("please enter the width of ground")
n=int(input())
ge=5
dissurf=pygame.display.set_mode((n*ge,n*ge))
dissurf.fill(BLACK)
g=Forest(n)
def drawone(i,j,c):
    if c.ground[i][j].state==0:
        pygame.draw.rect(dissurf,BLACK,(i*ge,j*ge,ge-1,ge-1))
    elif c.ground[i][j].state==1:
        pygame.draw.rect(dissurf,GREEN,(i*ge,j*ge,ge-1,ge-1))
    elif c.ground[i][j].state==2:
        pygame.draw.rect(dissurf,RED,(i*ge,j*ge,ge-1,ge-1))
    elif c.ground[i][j].state==3:
        pygame.draw.rect(dissurf,GREY,(i*ge,j*ge,ge-1,ge-1))
   
while True:
    for event in  pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    g.update()
    for i in range(n):
        for j in range(n):
            drawone(i,j,g)
    pygame.display.update()
                
        
        
        
        
    