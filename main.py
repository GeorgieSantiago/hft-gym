import gymnasium as gym
import numpy as np
from utils import plotLearning
import logging

logging.basicConfig(filename='debug.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.info("Logging online")
gym.envs.register(
     id='engine-v0',
     entry_point='gym.envs.engine:Engine',
     max_episode_steps=250,
)

def main():
    env = gym.make('engine-v0')
    net = None
    score_history = []
    eps_history = []
    n_epochs = 500
    logging.debug("Training start!")
    print('Training started!')
    for i in range(n_epochs):
        score = 0
        done = False
        obs = env.reset()
        logging.debug(f"Starting Epoch {i}")
        while not done:
            #TODO action = net.choose_action(obs)
            action = env.action_space.sample()
            logging.debug(action)
            _obs, reward, terminated, truncated, _ = env.step(action)
            print(_obs)
            score += reward
            done = terminated or truncated
            #TODO agent store transition
            #TODO net.store_transition(obs, action, reward, _obs, terminated, truncated)
            #TODO net.learn()
            obs = _obs
        score_history.append(score + i)
        eps_history.append(n_epochs - i)
        avg_score = np.mean(score_history[-100:])
        logging.debug(f'Episode {i} score {score}, avg_score: {avg_score}, epsilon: net.epsilon')
    x = [i + 1 for i in range(n_epochs)]
    filename = 'temp_output.png' #TODO switch this to console param
    plotLearning(x, score_history, eps_history, filename)


if __name__ == '__main__':
    main()
