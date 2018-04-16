import connect
import random
import copy
import numpy as np
import matplotlib.pyplot as plt
import RandomAgent as ra

K=200
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

            
class MemoryUnit:
    def __init__(self,state):
        self.state=state
        self.actionValues={0:0,1:0,2:0,3:0,4:0}

    def getmaxAction(self,available_actions):
        maxvalue=-1
        maxaction=-1
        for action in available_actions:
            if self.actionValues[action]>=maxvalue:
                maxvalue=self.actionValues[action]
                maxaction=action
        return maxaction
    
    def getmaxActionValue(self):
        maxvalue=-1
        for action in self.actionValues:
            if self.actionValues[action]>=maxvalue:
                maxvalue=self.actionValues[action]   
        return maxvalue

    def setActionValue(self,action,value):#if there is the memrory about a state,can use this method to update the value of its action 
        self.actionValues[action]=value



'''
class randomAgent:
    def __init__(self,environment=Environment()):
        self.environment=environment
        self.resultlist=[]
    
    def getChoiceAction(self):
        available_actions=self.environment.game.available_actions.tolist()
        return available_actions[random.randint(0,len(available_actions)-1)] 

    def makeAction(self):
        action=self.getChoiceAction()
        self.environment.game.act(action)
        self.environment.game.change_turn()


    def play_a_game(self):#return the result of the game(win:1,lose:-1,draw:0)#############测不出胜负全平！！！�?
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
            newrandomAgent=randomAgent()
            for i in range(m):
                summary=summary+newrandomAgent.play_a_game()
            return summary

        self.environment.game.reset(first_player='o')
        self.environment.makeEnvAction(True)
        for i in range(k):
            res=play_m_games_and_sum_up()
 #           print(res)
            self.resultlist.append(res)
    




'''






class Agent:
    def __init__(self,environment=Environment()):
        self.workmemory={}#previous{'state':xxx,'action':yyy]
        self.longtermmemory=[]#list of MemoryUnit
        self.environment=environment
        self.γ=0.7
        self.α=0.7
        self.ε=0.05
        self.resultlist=[]
    def searchMemory(self,state):#return a MemoryUnit
        result=False
        for unit in self.longtermmemory:
            if self.stateEq(state,unit.state):
                result=unit
                break
        return result
    
    def editMemory(self,MemoryUnit,action,value):
        MemoryUnit.setActionValue(action,value)

    def addMemory(self,state,action,value):#called in the case that when a state first insert into memory
        newMemoryUnit=MemoryUnit(state)
        newMemoryUnit.actionValues[action]=value
        self.longtermmemory.append(newMemoryUnit)

    def stateEq(self,state1,state2):#state is a numpy array
        return (state1==state2).all()

    def getChoiceAction(self):#get a choose action from a given state
        memory=False
        memory=self.searchMemory(self.environment.game.grid)
        if memory==False:
            available_actions=self.environment.game.available_actions.tolist()
            return available_actions[random.randint(0,len(available_actions)-1)]
        else:
            if random.random()>self.ε:
                return memory.getmaxAction(self.environment.game.available_actions.tolist())#########
            else:
                available_actions=self.environment.game.available_actions.tolist()
                return available_actions[random.randint(0,len(available_actions)-1)]
    
    def getNowstate(self):#get the state of the env now
        return self.environment.game.grid
    
    def makeAction(self):
        action=self.getChoiceAction()
        self.workmemory={'state':copy.deepcopy(self.getNowstate()),'action':copy.deepcopy(action)}#let the workmemory be the state-action pair just have made
        self.environment.game.act(action)
        self.environment.game.change_turn()

    def getReward(self):#only deal with the case that the agent action is not a winning move or draw move(that means the enemy have just made a action)
        R=0
        memoryReward=0#init two part of reward
        '''
        if self.environment.game.was_winning_move('o'):
            R=-1
            memoryReward=0
        elif self.environment.game.grid_is_full():
            R=0
            memoryReward=0
        else:
        '''
        R=0
        nowstate=self.getNowstate()
        findMemoryUnit=self.searchMemory(nowstate)
        if findMemoryUnit==False:
            memoryReward=0
        else:
            memoryReward=findMemoryUnit.getmaxActionValue()
        return {'R':R,'memoryreward':memoryReward}


    def learn(self,reward):#learn by init and add memoryUnit into memory or edit existed memoryUnit
        R=reward['R']
        memoreward=reward['memoryreward']
        prevoiusState=self.workmemory['state']
        prevoiusAction=self.workmemory['action']
        findMemoryUnit=self.searchMemory(prevoiusState)
        if findMemoryUnit==False:
            initvalue=self.α*(R+self.γ*memoreward)
            self.addMemory(prevoiusState,prevoiusAction,initvalue)
        else:
            oldvalue=findMemoryUnit.actionValues[prevoiusAction]
            newvalue=(1-self.α)*oldvalue+self.α*(R+self.γ*memoreward)
            self.editMemory(findMemoryUnit,prevoiusAction,newvalue)

    def interact(self):#a interact include decide a action,make the action,the action of env(enemy),and learn from reward.
        if self.environment.game.grid_is_full():#the action that enemy draw
            reward={'R':0,'memoryreward':0}
            self.learn(reward)
            self.environment.game.reset(first_player='o')
            self.environment.makeEnvAction(True)

        self.makeAction()

        if self.environment.game.was_winning_move('x'):
            reward={'R':1,'memoryreward':0}
            self.learn(reward)
            self.environment.makeEnvAction(True)
        elif self.environment.game.grid_is_full():#means a draw
            reward={'R':0,'memoryreward':0}
            self.learn(reward)
            self.environment.makeEnvAction(True)
        else:
            self.environment.makeEnvAction(False)
            if self.environment.game.grid_is_full():#the action that enemy draw
                reward={'R':0,'memoryreward':0}
                self.learn(reward)
                self.environment.game.reset(first_player='o')
                self.environment.makeEnvAction(True)
            elif self.environment.game.was_winning_move('o'):
                reward={'R':-1,'memoryreward':0}
                self.learn(reward)
                self.environment.game.reset(first_player='o')
                self.environment.makeEnvAction(True)
            else:
                reward=self.getReward()
                self.learn(reward)

    def play_a_game(self):#return the result of the game(win:1,lose:-1,draw:0)
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
            newAgent=Agent()
            newAgent.longtermmemory=copy.deepcopy(self.longtermmemory)
            for i in range(m):
                summary=summary+newAgent.play_a_game()
            return summary

        self.environment.game.reset(first_player='o')
        self.environment.makeEnvAction(True)
        for i in range(k):
            for j in range(n):
                self.interact()
            res=play_m_games_and_sum_up()
 #           print(res)
            self.resultlist.append(res)


def draw(resultlist,randlist):
    x=list(range(len(resultlist))) 
    plt.figure()  
    plt.plot(x,resultlist,'r', label='Q-learning')
    plt.plot(x,randlist,'b',label='Random Agent')
    plt.xlabel("k")  
    plt.ylabel("value")  
    plt.savefig("return.jpg")  
''' 
agentnum=3

agentlsit=[]
randomagentlist=[]

for i in range(agentnum):
    agent=Agent()#####
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

'''
