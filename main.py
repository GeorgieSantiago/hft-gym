import gymnasium as gym
import numpy as np
from utils import plotLearning, get_obs_shape
import logging
import sys
import argparse
from gym.envs.client import Symbol
from datetime import datetime

logging.basicConfig(filename='debug.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.info("Logging online")

# gym.envs.register(
#      id='engine-v0',
#      entry_point='gym.envs.engine:Engine',
#      max_episode_steps=250,
# )

gym.envs.register(
     id='engine-v1',
     entry_point='gym.envs.alpaca_env:Alpaca',
     max_episode_steps=250,
)

def println(data):
    print(data)
    print("\n")
    sys.stdout.flush()

def run():
    env = gym.make('engine-v1')
    env.setup("TSLA", 12, start_time=datetime(2022, 6, 1), end_time=datetime(2022, 6, 21), debug=True)
    net = None
    score_history = []
    eps_history = []
    n_epochs = 500
    logging.debug("Training start!")
    println('Training started!')
    for i in range(n_epochs):
        score = 0
        done = False
        obs = env.reset()
        logging.debug(f"Starting Epoch {i}")
        while not done:
            action = env.action_space.sample()
            logging.debug(action)
            _obs, reward, terminated, truncated, _ = env.step(action)
            exit(1)
            score += reward
            done = terminated or truncated
            obs = _obs
        score_history.append(score + i)
        eps_history.append(n_epochs - i)
        avg_score = np.mean(score_history[-100:])
        logging.debug(f'Episode {i} score {score}, avg_score: {avg_score}, epsilon: net.epsilon')
    x = [i + 1 for i in range(n_epochs)]
    filename = 'temp_output.png' #TODO switch this to console param
    plotLearning(x, score_history, eps_history, filename)

def main(options: dict):
    '''
    Utilities
    '''
    if options.obs_shape:
        return get_obs_shape()
    
    '''
    Engine entrypoint
    '''
    run()


if __name__ == '__main__':
    args = argparse.ArgumentParser(
        description='Trade engine AI training'
    )

    args.add_argument('--user', choices=[
        'human',
        'ai',
        'algo'
    ], default='ai')

    args.add_argument('--obs_shape', default=False, type=bool)
    main(args.parse_args())
