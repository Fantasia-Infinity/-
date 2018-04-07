

# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 10:47:45 2018

@author: Fantasia
"""
import numpy as np


def sudoku_solver(sudoku):
    srows=[]
    scols=[]
    slocals=[]
    for i in range(9):
        srows.append(set(list(range(1,10))))
    for i in range(9):
        scols.append(set(list(range(1,10))))
    for i in range(9):
        slocals.append(set(list(range(1,10))))
    #对每一行/列/方框的取值集合进行初始化，一开始全都是包含了一到九 
    
    def placetolocalind(x,y):
        rindx=x//3
        rindy=y//3
        m=[[0,1,2],
           [3,4,5],
           [6,7,8]]
        ind=m[rindx][rindy]
        return ind
    #格子的位置到其对应的方框的索引值函数  因为行和列直接用其横纵坐标就能索引，而方框的索引值要经过处理得到
    #先对其横坐标和纵坐标分类分到0，1，2三个区间里 然后通过横区间和纵区间查询m来获得方框索引值
    #这个索引值用来找到上面对应的方框的可能取值集合
    
    def imposebound(x,y,value):
        srows[x].remove(value)
        scols[y].remove(value)
        localind=placetolocalind(x,y)
        slocals[localind].remove(value)
    #在一个格子填写一个值之后把这个值从对应的行/列/方框的可能取值集合中取出 这就是施加约束 
    
    def releasebound(x,y,value):
        srows[x].add(value)
        scols[y].add(value)
        localind=placetolocalind(x,y)
        slocals[localind].add(value)
    #对应的，当把一个值擦去的时候用来把这些约束去除

    def getdomain(x,y):
        localind=placetolocalind(x,y)
        return srows[x]&scols[y]&slocals[localind]
    #对给定位置求其可能的取值集合 通过对行/列/方框的三个集合求交实现
    
    def getdomainsize(x,y):
        localind=placetolocalind(x,y)
        return len(srows[x]&scols[y]&slocals[localind])
    #对给定位置求其取值集合大小
    
    def findMRVplace(sudoku):
        temp=-1,-1
        tempsize=9
        for i in range(9):
            for j in range(9):
                if sudoku[i][j]==0:
                    size=getdomainsize(i,j)
                    if size<tempsize:
                        tempsize=size
                        temp=i,j
        return temp
     #遍历所有格子，如果是空缺的则求出其可能取值集合的大小，取最小的那个位置并返回  
     
    def firstreference(sudoku):
        for i in range(9):
            for j in range(9):
                if sudoku[i][j]!=0:
                    imposebound(i,j,sudoku[i][j])
                    
    #在搜索开始前先对已经给出值的格子进行处理，把约束加到对应区域上
    def checkthestep(sudoku, x, y, value):
        def checkrow(sudoku,x,value):
            for i in range(9):
                if sudoku[x][i]==value:
                    return False
            return True
        def checkcol(sudoku,y,value):
            for i in range(9):
                if sudoku[i][y]==value:
                    return False
            return True
        def checklocal(sudoku,x,y,value):
            basex=3*(x//3)
            basey=3*(y//3)
            for i in range(basex,basex+3):
                for j in range(basey,basey+3):
                    if sudoku[i][j]==value:
                        return False
            return True
        return (checkrow(sudoku,x,value) and checkcol(sudoku,y,value) and checklocal(sudoku,x,y,value))
    #检查一步填写是否符合规则 通过分别检查其行/列/方框上的格子是否有重复完成
    
    def solver(sudoku):
        (thex,they)=findMRVplace(sudoku)
        if thex==-1 and they==-1:
            return True
        else:
            for value in getdomain(thex,they):
                if checkthestep(sudoku,thex,they,value):
                    sudoku[thex][they]=value
                    imposebound(thex,they,value)
                    if solver(sudoku):
                        return True
                    else:
                        sudoku[thex][they]=0
                        releasebound(thex,they,value)
            return False
     #回溯搜索 如果没有填的位置(寻找位置的函数返回坐标-1，-1)代表已经完成
     #否则找一个可能填法最少的位置，对其可能的取值进行搜索，搜索递归进行
     #如果某个位置填了某个值后后续搜索无法找到找到解，那么这个值被擦去，同时把对应的约束也消去，之后继续用其它值进行搜索
    
    firstreference(sudoku)
    #在开始前把已有的约束都加上
    
    if solver(sudoku):
        return sudoku
    #如果可解返回解
    else:
        for i in range(9):
            for j in range(9):
                sudoku[i][j]=-1
        return sudoku
    #如果不可解则填满-1
