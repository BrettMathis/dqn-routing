#!/usr/bin/env python3

from model import params,design

import gym
from gym import error, spaces, utils
from gym.utils import seeding

import numpy as np

from timeit import default_timer as timer

class DQN_GR_env(gym.Env):
    metadata = {'render.modes': ['human']}

    # params=(DEF,stdcells,nets,netlist)

    def __init__(self,init_data):

        super(DQN_GR_env, self).__init__()

        self.init_data=init_data

        self.design = design.design(*self.init_data)

        self.action_space = spaces.Discrete(6+params.SN)
        self.observation_space = spaces.Box(0,max(params.MT)*5,
                                 [params.GX+1,params.GY+1,2*(params.MM+1)],
                                 np.intc)

        self.state = np.array(self.design.get_state())
        self.score = self.design.global_loss(self.state)
        self.num_solved = sum([x.all_done for x in self.design.nets.values()])

        self.blank=None

        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self,action):
#        start = timer()
        assert self.action_space.contains(action), "Invalid action"
#        end1 = timer()

        self.design.do_action(action)
#        end2 = timer()

        self.state = np.array(self.design.get_state())
#        end3 = timer()

        old_score = self.score
        self.score = self.design.global_loss(self.state)
#        end4 = timer()

        num_solved=sum([x.all_done for x in self.design.nets.values()])

        q_score = self.score - old_score
        q_score += params.RW*(num_solved-self.num_solved)

        self.num_solved=num_solved
#        end5 = timer()

#        print("Assertion took "+str((end1-start)*10**3))
#        print("Do-action took "+str((end2-end1)*10**3))
#        print("Get-state took "+str((end3-end2)*10**3))
#        print("Get-loss took "+str((end4-end3)*10**3))
#        print("Simple addition took "+str((end5-end4)*10**3))
#        print(end5-start)

        return self.state, q_score, self.design.done(), {}

    def reset(self):
        if self.blank is None:
            self.blank=np.array(self.design.visualize())
            self.blank[0]=np.zeros_like(self.blank[0])
            self.blank[-1]=np.zeros_like(self.blank[-1])

        self.render()

        self.design = design.design(*self.init_data)
        self.state = np.array(self.design.get_state())
        self.score = self.design.global_loss(self.state)
        return self.state

    def render(self,mode='human',close=False):
        #state = self.state[:]
        #state = np.array([[y[:params.MM+1] for y in x] for x in state])
        #state.transpose(2,0,1)
        #print(state)
        np.set_printoptions(linewidth=np.inf)
        np.set_printoptions(edgeitems=np.inf)
        print(np.array(self.design.visualize())-self.blank)
        print(self.score+params.RW*self.num_solved)
        print(self.design.done())
        print(self.num_solved)
        print(self.design.switching_factor())
        print(self.design.active)
        print(self.design.nets[self.design.active[0]].close)
#        for n in self.design.nets.values():
#            print(n.all_done)
