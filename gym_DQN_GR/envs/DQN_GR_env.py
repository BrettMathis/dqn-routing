#!/usr/bin/env python3

from model import params,design

import gym
from gym import error, spaces, utils
from gym.utils import seeding

import numpy as np

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

        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self,action):
        assert self.action_space.contains(action), "Invalid action"

        self.design.do_action(action)

        self.state = np.array(self.design.get_state())
        old_score = self.score
        self.score = self.design.global_loss(self.state)


        return self.state, self.score-old_score, self.design.done(), {}

    def reset(self):
        self.design = design.design(*self.init_data)
        self.state = np.array(self.design.get_state())
        self.score = self.design.global_loss(self.state)
        return self.state

    def render(self,mode='human',close=False):
        print(self.state)
        print(self.score)
        print(self.design.done())
        print(self.design.switching_factor())
        print(self.design.no_switch)
        for n in self.design.nets.values():
            print(n.all_done)
