import gymnasium as gym

gym.envs.register(
     id='engine-v0',
     entry_point='gym.envs.engine:Engine',
     max_episode_steps=250,
)