from gym.envs.registration import register

register(
    id='DQN_GR-v0',
    entry_point='gym_DQN_GR.envs:DQN_GR_env'
)
