import connect
import numpy as np 
import copy
import random
import math
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
            

class MCTNode:
    def __init__(self,state,player):
        self.state=state
        self.player=player
        self.availableActions=state.available_actions
        self.father=None
        self.childdict={}# key为动作，值为子节点
        self.count=0
        self.playerwins={'o':0,'x':0}
        self.C=0.05
    
    def getmaxaction(self):
        maxval=0
        retaction=None
        for key in self.childdict:
            child=self.childdict[key]
            #val=child.playerwins[self.player]/child.count
            val=child.count
            if val>maxval:
                retaction=key
        return retaction
    
    def getstatevalue(self):
        return self.playerwins[self.player]/self.count

    def incwin(self,player):
        self.playerwins[player]=self.playerwins[player]+1


    def backpropagation(self,winner):
        if self.father==None:
            if winner=='draw':
                self.count+=1
            else:
                self.count+=1
                self.incwin(self.player)
        else:
            if winner=='draw':
                self.count+=1
                self.father.backpropagation(winner)
            else:
                self.count+=1
                self.incwin(self.player)
                self.father.backpropagation(winner)
    
    def getUCB(self,player):
        if self.count==0:
            return 0
        else:
            return self.playerwins[player]/self.count+self.C*math.sqrt(math.log(self.father.count)/self.count)
    
    def select(self,player):
        maxval=-1
        thenode=None
        retaction=None#少了检查是否事终止节点的分支
        if self.state.grid_is_full():
            return {'node':self,'action':'draw'}
        elif self.state.was_winning_move(self.state.other_player[self.state.player_at_turn]):
            return {'node':self,'action':self.state.other_player[self.state.player_at_turn]}
        for action in self.availableActions:
            if action in self.childdict:
                child=self.childdict[action]
                childUCB=child.getUCB(player)#################
                if maxval<=childUCB:
                    thenode=child
                    retaction=action
                    maxval=childUCB
            else:
                thenode=self
                retaction=action
                return {'node':thenode,'action':retaction}
        return thenode.select(player)
        
    
    def expansion(self,action):#return the child that new expan
        newstate=copy.deepcopy(self.state)
        newstate.act(action)
        newstate.change_turn()
        newchild=MCTNode(newstate,newstate.player_at_turn)
        newchild.father=self
        self.childdict[action]=newchild
        return newchild
    
    def simulation(self):
        newenv=copy.deepcopy(self.state)
        if newenv.was_winning_move(newenv.other_player[self.player]):
            return newenv.other_player[self.player]
        elif newenv.grid_is_full():
            return 'draw'
        else:
            while(True):
                available=newenv.available_actions
                action=available[random.randint(0,len(available.tolist())-1)]
                newenv.act(action)
                if newenv.was_winning_move(newenv.player_at_turn):
                    return newenv.player_at_turn
                elif newenv.grid_is_full():
                    return 'draw'
                newenv.change_turn()
            


class MCTSAgent:
    def __init__(self,environment=Environment()):
        self.environment=environment
        self.resultlist=[]
    
    def MCTS(self,env,player):
        root=MCTNode(copy.deepcopy(env),player)#the state of tree node is a connect object
        maxturn=300
        count=0
        while(count<maxturn):
            selectresult=root.select(player)
            if selectresult['action']=='draw':
                selectresult['node'].backpropagation('draw')
                count+=1
                continue
            elif selectresult['action']=='o':
                selectresult['node'].backpropagation('o')
                count+=1
                continue
            elif selectresult['action']=='x':
                selectresult['node'].backpropagation('x')
                count+=1
                continue
            nodetoexpan=selectresult['node']
            nodetosimulate=nodetoexpan.expansion(selectresult['action'])
            simulateresult=nodetosimulate.simulation()
            nodetosimulate.backpropagation(simulateresult)
            count+=1
        return {'action':root.getmaxaction(),'statevalue':root.getstatevalue()}
        
        
        

    def getChoiceAction(self):
        return self.MCTS(self.environment.game,self.environment.game.player_at_turn)['action']

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
            newMCTSAgent=MCTSAgent()
            for i in range(m):
                summary=summary+newMCTSAgent.play_a_game()
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
    plt.plot(x,resultlist,'r', label='MCTS')
    plt.plot(x,randlist,'b',label='Random Agent')
    plt.xlabel("k")  
    plt.ylabel("value")  
    plt.savefig("returnMCTS.jpg")  
'''

a=MCTSAgent()
a.environment.game=env
res=a.MCTS(a.environment.game,a.environment.game.player_at_turn)
print(res['action'])
print(res['statevalue'])
a.trainAndShow()



'''          
agentnum=1

agentlsit=[]
randomagentlist=[]

for i in range(agentnum):
    agent=MCTSAgent()#####
    agentlsit.append(agent)
for agent in agentlsit:
    agent.trainAndShow()

for i in range(agentnum):
    agent=ra.randomAgent()#####
    randomagentlist.append(agent)
for agent in randomagentlist:
    agent.trainAndShow()

def sumMCTSagentlistresult():
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

retlist=sumMCTSagentlistresult()
randomlist=sumrandomagentlistresult()
draw(retlist,randomlist)


