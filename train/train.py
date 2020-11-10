#!/usr/bin/env python3

import sys
sys.path.append("..")

import numpy as np
import gym
import gym_DQN_GR

from model import params

import argparse

from PIL import Image

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Convolution2D, Permute, Conv3D, MaxPooling3D
from keras.optimizers import Adam
import keras.backend as K

from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, BoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor
from rl.callbacks import FileLogger, ModelIntervalCheckpoint

from training_data.gates import *
from training_data.rca2 import *
from training_data.rca4 import *
from training_data.rca8 import *
from training_data.csa8 import *
from training_data.cskipa8 import *
from training_data.cla8 import *

THO = 10**3

ENV_NAME = 'DQN_GR-v0'
INPUT_SHAPE = (params.GX+1,params.GY+1,(params.MM+1)+1,1)
WINDOW_LENGTH = 1
MEM_BATCH = 128
LEARNING_RATE = 0.005

MAX_EPISODE_STEPS = 25*THO
TARGET_MODEL_UPDATE = 50*THO
TOTAL_TRAINING_STEPS = 100*THO*THO  
EPSILON_STEPS = 2*THO*THO
MEMORY_SIZE = 1*THO*THO

MAX_EPISODE_STEPS = 0.5*THO
TARGET_MODEL_UPDATE = 1*THO
TOTAL_TRAINING_STEPS = 100*THO*THO 
EPSILON_STEPS = 0.05*THO*THO
MEMORY_SIZE = 1*THO*THO

parser = argparse.ArgumentParser()
parser.add_argument('--mode', choices=['train', 'test'], default='train')
parser.add_argument('--env-name', type=str, default=ENV_NAME)
parser.add_argument('--weights', type=str, default=None)
args = parser.parse_args()


DEF=[];stdcells=[];nets=[];netlist=[];

ref_design = make_rca2(4);

[DEF, stdcells, nets, netlist] = compile_design(ref_design);


# Get the environment and extract the number of actions.
env = gym.make(args.env_name,init_data=[DEF,stdcells,nets,netlist])
np.random.seed(420)
env.seed(420)
nb_actions = env.action_space.n

# Next, we build our model. We use the same model that was described by Mnih et al. (2015).
input_shape = (WINDOW_LENGTH,) + INPUT_SHAPE
input_shape = INPUT_SHAPE
model = Sequential()
model.add(Permute((1, 2, 3, 4), input_shape=input_shape))
model.add(Conv3D(8, (4, 4, 1), strides=(2, 2, 1)))
model.add(Activation('relu'))
model.add(Conv3D(16, (2, 2, 1), strides=(1, 1, 1)))
model.add(Activation('relu'))
#model.add(Conv3D(16, (2, 2, 1), strides=(1, 1, 1)))
#model.add(Activation('relu'))
#model.add(MaxPooling3D(pool_size=(2, 2, 2)))

#model.add(Convolution2D(8, (4, 4), strides=(2, 2)))
#model.add(Activation('relu'))
#model.add(Convolution2D(16, (2, 2), strides=(1, 1)))
#model.add(Activation('relu'))
#model.add(Convolution2D(16, (2, 2), strides=(1, 1)))
#model.add(Activation('relu'))
model.add(Flatten())
model.add(Dense(32))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())

memory = SequentialMemory(limit=MEMORY_SIZE, window_length=WINDOW_LENGTH)
class Processor3D(Processor):
    def process_state_batch(self,batch):
        return np.expand_dims(batch,4)

processor = Processor3D()
# Select a policy. We use eps-greedy action selection, which means that a random action is selected
# with probability eps. We anneal eps from 1.0 to 0.1 over the course of 1M steps. This is done so that
# the agent initially explores the environment (high eps) and then gradually sticks to what it knows
# (low eps). We also set a dedicated eps value that is used during testing. Note that we set it to 0.05
# so that the agent still performs some random actions. This ensures that the agent cannot get stuck.
policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.05,
                              nb_steps=EPSILON_STEPS)

# The trade-off between exploration and exploitation is difficult and an on-going research topic.
# If you want, you can experiment with the parameters or use a different policy. Another popular one
# is Boltzmann-style exploration:
# policy = BoltzmannQPolicy(tau=1.)
# Feel free to give it a try!

dqn = DQNAgent(model=model, nb_actions=nb_actions, policy=policy, memory=memory,
               processor=processor, nb_steps_warmup=MAX_EPISODE_STEPS, gamma=.99,
               target_model_update=TARGET_MODEL_UPDATE,train_interval=1,
               batch_size=MEM_BATCH,delta_clip=1.)
dqn.compile(Adam(lr=LEARNING_RATE), metrics=['mae'])

if args.mode == 'train':
    # Okay, now it's time to learn something! We capture the interrupt exception so that training
    # can be prematurely aborted. Notice that now you can use the built-in Keras callbacks!
    weights_filename = 'dqn_{}_weights.h5f'.format(args.env_name)
    checkpoint_weights_filename = 'dqn_' + args.env_name + '_weights_{step}.h5f'
    log_filename = 'dqn_{}_log.json'.format(args.env_name)
    callbacks = [ModelIntervalCheckpoint(checkpoint_weights_filename, interval=250000)]
    callbacks += [FileLogger(log_filename, interval=100)]
    dqn.fit(env, callbacks=callbacks, nb_steps=TOTAL_TRAINING_STEPS, log_interval=MAX_EPISODE_STEPS, nb_max_episode_steps=MAX_EPISODE_STEPS, visualize=False)

    # After training is done, we save the final weights one more time.
    dqn.save_weights(weights_filename, overwrite=True)

    # Finally, evaluate our algorithm for 10 episodes.
#    dqn.test(env, nb_episodes=10, visualize=True)
elif args.mode == 'test':
    weights_filename = 'dqn_{}_weights.h5f'.format(args.env_name)
    if args.weights:
        weights_filename = args.weights
    dqn.load_weights(weights_filename)
    dqn.test(env, nb_episodes=10, nb_max_episode_steps=MAX_EPISODE_STEPS*10, visualize=False)
