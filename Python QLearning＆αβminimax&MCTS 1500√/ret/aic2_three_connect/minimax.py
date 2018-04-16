import connect
import numpy as np 
import copy
import random
import RandomAgent as ra
import matplotlib.pyplot as plt  

K=200
env = connect.Connect(verbose=False)
env.reset(first_player='o')
env.act(action=1)
print(env.grid[::-1])
env.change_turn()

class Environment:
    def __init__(self):
        self.game=connect.Connect(verbose=False)
        self.game.reset(first_player='o')
    
    def choiceRandAction(self):
        available=self.game.available_actions
        return available[random.randint(0,len(available.tolist())-1)]
    
    def makeRandAction(self):
        action=self.choiceRandAction()
        self.game.act(action)

    def makeEnvAction(self,isfirst):
        if isfirst:
            self.game.reset(first_player='o')
            self.makeRandAction()
            self.game.change_turn()
        else:
            if self.game.was_winning_move('x'):
                self.game.reset(first_player='o')
                self.makeRandAction()
                self.game.change_turn()
            elif self.game.grid_is_full():#means a draw
                self.game.reset(first_player='o')
                self.makeRandAction()
                self.game.change_turn()
            else:
                self.makeRandAction()
                self.game.change_turn()


class minimaxAgent:
    def __init__(self,environment=Environment()):
        self.environment=environment
        self.resultlist=[]
        self.count=0
    
    def AlphaBetaMinimax(self,recenv,player,alpha,beta):
        previous_player=recenv.game.other_player[player]
        if recenv.game.was_winning_move(previous_player):
            if previous_player=='o':
                self.count+=1
                return {'R':-1,'A':'over'}
            elif previous_player=='x':
                self.count+=1
                return {'R':1,'A':'over'}
        elif recenv.game.grid_is_full():
            self.count+=1
            return {'R':0,'A':'over'}
        else:
            if player=='x':#looking for max
                availableActions=recenv.game.available_actions.copy()
                retaction='init'
                for action in availableActions:
                    newenv=copy.deepcopy(recenv)
                    newenv.game.act(action)
                    newenv.game.change_turn()
                    actionvalue=self.AlphaBetaMinimax(newenv,'o',alpha,beta)['R']
                    if actionvalue>alpha:
                        alpha=actionvalue
                        retaction=action
                    if alpha>=beta:
                        break
                return {'R':alpha,'A':retaction}
            if player=='o':#looking for min
                availableActions=recenv.game.available_actions.copy()
                retaction='init'
                for action in availableActions:
                    newenv=copy.deepcopy(recenv)
                    newenv.game.act(action)
                    newenv.game.change_turn()
                    actionvalue=self.AlphaBetaMinimax(newenv,'x',alpha,beta)['R']
                    if actionvalue<beta:
                        beta=actionvalue
                        retaction=action
                    if beta<=alpha:
                        break
                return {'R':beta,'A':retaction}

    def getChoiceAction(self):
        return self.AlphaBetaMinimax(self.environment,'x',-10,+10)['A']

    def makeAction(self):
        action=self.getChoiceAction()
        self.environment.game.act(action)
        self.environment.game.change_turn()


    def play_a_game(self):#return the result of the game(win:1,lose:-1,draw:0)#############测不出胜负全平！！！！
        def judgeGameState():
            if self.environment.game.player_at_turn=='o' and self.environment.game.was_winning_move('x'):
                return win#player_at_turn is after a change made by previousActionner,so'o'means previous action is made my agent
            elif self.environment.game.player_at_turn=='x' and  self.environment.game.was_winning_move('o'):
                return lose
            elif self.environment.game.grid_is_full():
                return draw
            else:
                return running

        self.environment.game.reset(first_player='o')
        running=10
        win=1
        lose=-1
        draw=0#four kinds of game states
        step=0
        while(True):
            if step==0:
                isfirst=True
            else:
                isfirst=False
            self.environment.makeEnvAction(isfirst)
            newgamestate=judgeGameState()

            if newgamestate==win:
                return win
            elif newgamestate==lose:
                return lose
            elif newgamestate==draw:
                return draw

            self.makeAction()
            newgamestate=judgeGameState()
  
            if newgamestate==win:
                return win
            elif newgamestate==lose:
                return lose
            elif newgamestate==draw:
                return draw
            step+=1
    
    def trainAndShow(self,k=K,n=20,m=10):
        def play_m_games_and_sum_up():
            summary=0
            newminimaxAgent=minimaxAgent()
            for i in range(m):
                summary=summary+newminimaxAgent.play_a_game()
            return summary

        self.environment.game.reset(first_player='o')
        self.environment.makeEnvAction(True)
        for i in range(k):
            res=play_m_games_and_sum_up()
            print(res)
            self.resultlist.append(res)


def draw(resultlist,randlist):
    x=list(range(len(resultlist))) 
    plt.figure()  
    plt.plot(x,resultlist,'r', label='Q-learning')
    plt.plot(x,randlist,'b',label='Random Agent')
    plt.xlabel("k")  
    plt.ylabel("value")  
    plt.savefig("returnminimax.jpg")  
#a=minimaxAgent()
#print(a.AlphaBetaMinimax(env,'x',-10,+10))
#print(a.count)
            
agentnum=1

agentlsit=[]
randomagentlist=[]

for i in range(agentnum):
    agent=minimaxAgent()#####
    agentlsit.append(agent)
for agent in agentlsit:
    agent.trainAndShow()

for i in range(agentnum):
    agent=ra.randomAgent()#####
    randomagentlist.append(agent)
for agent in randomagentlist:
    agent.trainAndShow()

def sumagentlistresult():
    retlist=[]
    for i in range(K):
        retlist.append(0)
    for agent in agentlsit:
        retlist = map(lambda x, y: x + y, retlist,agent.resultlist)
    retlist=list(map(lambda x:x/agentnum,retlist))
    return retlist

def sumrandomagentlistresult():
    retlist=[]
    for i in range(K):
        retlist.append(0)
    for agent in randomagentlist:
        retlist = map(lambda x, y: x + y, retlist,agent.resultlist)
    retlist=list(map(lambda x:x/agentnum,retlist))
    return retlist

retlist=sumagentlistresult()
randomlist=sumrandomagentlistresult()
draw(retlist,randomlist)

