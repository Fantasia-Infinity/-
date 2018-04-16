import connect
import random
import copy
import numpy as np
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
    

