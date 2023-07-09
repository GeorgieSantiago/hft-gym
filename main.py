import gymnasium as gym
import numpy as np
from utils import plot_learning_curve, get_obs_shape
import logging
import sys
import argparse
from datetime import datetime

gym.envs.register(
    id='engine-v1',
    entry_point='gym.envs.alpaca_env:Alpaca',
    max_episode_steps=250,
)


def println(data):
    print(data)
    print("\n")
    sys.stdout.flush()


def run(human_player: bool = False):
    env = gym.make('engine-v1')
    env.setup("TSLA", 60, start_time=datetime(2022, 6, 1), end_time=datetime(2022, 6, 21), debug=True, live=False)
    net = None
    score_history = []
    eps_history = []
    n_epochs = 50000
    println('Training started!')
    for i in range(n_epochs):
        score = 0
        done = False
        obs, _ = env.reset()
        while not done:
            if not human_player:
                action = env.action_space.sample()
                _obs, reward, terminated, truncated, info = env.step(action)
                score += reward
                done = terminated or truncated
                obs = _obs
            else:
                print(obs)
                should_continue = input("Continue? [y/n]")
                open_price = float(input("Open price: "))
                spread_value = float(input("Spread: "))
                loss_value = float(input("Loss: "))
                _obs, reward, terminated, truncated, info = env.step(
                    (open_price, spread_value, loss_value))
                done = terminated or truncated or should_continue is not 'y'
                println(f"reward: {reward}")
                obs = _obs
        score_history.append(score)
        eps_history.append(n_epochs)
        avg_score = np.mean(score_history[-100:])
        println(f'Episode {i} score {score}, avg_score: {avg_score}, epsilon: net.epsilon')
        if human_player:
            break
    x = [i + 1 for i in range(n_epochs)]
    filename = f'temp_output_random_agent_episodes_model_{"human" if human_player else "model"}_{n_epochs}_engine_1.png'  # TODO switch this to console param
    plot_learning_curve(score_history, x if not human_player else [1], filename)


def main(options):
    if options.obs_shape:
        return get_obs_shape()
    run(options.human)


if __name__ == '__main__':
    args = argparse.ArgumentParser(
        description='Trade engine AI training'
    )

    args.add_argument('--human', default=False, type=bool)
    args.add_argument('--obs_shape', default=False, type=bool)
    main(args.parse_args())
