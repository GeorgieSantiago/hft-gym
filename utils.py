import matplotlib.pyplot as plt
import numpy as np
import gymnasium as gym
from datetime import datetime, timedelta
import mplfinance as mpf
import pandas as pd
from PIL import Image
import os
import io

from gym.envs.client import Symbol


def plot_learning_curve(scores, x, figure_file):
    running_avg = np.zeros(len(scores))
    for i in range(len(running_avg)):
        running_avg[i] = np.mean(scores[max(0, i - 100):(i + 1)])
    plt.plot(x, running_avg)
    plt.title('Running average of previous 100 scores')
    plt.savefig(figure_file)


class SkipEnv(gym.Wrapper):
    def __init__(self, env=None, skip=4):
        super(SkipEnv, self).__init__(env)
        self._skip = skip

    def step(self, action):
        t_reward = 0.0
        done = False
        for _ in range(self._skip):
            obs, reward, done, info = self.env.step(action)
            t_reward += reward
            if done:
                break
        return obs, t_reward, done, info

    def reset(self):
        self._obs_buffer = []
        obs = self.env.reset()
        self._obs_buffer.append(obs)
        return obs


class PreProcessFrame(gym.ObservationWrapper):
    def __init__(self, env=None):
        super(PreProcessFrame, self).__init__(env)
        self.observation_space = gym.spaces.Box(low=0, high=255,
                                                shape=(80, 80, 1), dtype=np.uint8)

    def observation(self, obs):
        return PreProcessFrame.process(obs)

    @staticmethod
    def process(frame):
        new_frame = np.reshape(frame, frame.shape).astype(np.float32)

        new_frame = 0.299 * new_frame[:, :, 0] + 0.587 * new_frame[:, :, 1] + \
                    0.114 * new_frame[:, :, 2]

        new_frame = new_frame[35:195:2, ::2].reshape(80, 80, 1)

        return new_frame.astype(np.uint8)


class MoveImgChannel(gym.ObservationWrapper):
    def __init__(self, env):
        super(MoveImgChannel, self).__init__(env)
        self.observation_space = gym.spaces.Box(low=0.0, high=1.0,
                                                shape=(self.observation_space.shape[-1],
                                                       self.observation_space.shape[0],
                                                       self.observation_space.shape[1]),
                                                dtype=np.float32)

    def observation(self, observation):
        return np.moveaxis(observation, 2, 0)


class ScaleFrame(gym.ObservationWrapper):
    def observation(self, obs):
        return np.array(obs).astype(np.float32) / 255.0


class BufferWrapper(gym.ObservationWrapper):
    def __init__(self, env, n_steps):
        super(BufferWrapper, self).__init__(env)
        self.observation_space = gym.spaces.Box(
            env.observation_space.low.repeat(n_steps, axis=0),
            env.observation_space.high.repeat(n_steps, axis=0),
            dtype=np.float32)

    def reset(self):
        self.buffer = np.zeros_like(self.observation_space.low, dtype=np.float32)
        return self.observation(self.env.reset())

    def observation(self, observation):
        self.buffer[:-1] = self.buffer[1:]
        self.buffer[-1] = observation
        return self.buffer


class HOLC(object):
    def __init__(self, _high: float, _open: float, _low: float, _close: float, _volume: float, _period: datetime):
        self.high = _high
        self.open = _open
        self.low = _low
        self.close = _close
        self.period = _period
        self.volume = _volume


def make_env(env_name):
    env = gym.make(env_name)
    env = SkipEnv(env)
    env = PreProcessFrame(env)
    env = MoveImgChannel(env)
    env = BufferWrapper(env, 4)
    return ScaleFrame(env)


def plot_bars(data, start_dt: datetime, end_dt: datetime, as_np_array=False, save=False, show=False) -> Image:
    objs = [{
        'high': d['h'],
        'open': d['o'],
        'low': d['l'],
        'close': d['c'],
        'volume': d['v'],
    } for d in data if d != None]
    df = pd.DataFrame(objs, [pd.to_datetime(d['t']) for d in data if d != None])
    fig, _ = mpf.plot(df, type='candle', volume=True, returnfig=True)
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')
    im = Image.open(img_buf)
    if show:
        im.show()
    if save:
        if "plots" not in os.listdir():
            os.mkdir("plots")
        filename = f"plots/{start_dt.timestamp()}-{end_dt.timestamp()}-figures.png"
        fig.savefig(filename, format="png")
    if as_np_array:
        return np.array(im, dtype=np.float32)
    img_buf.close()

    return im


# Usage
# instrument = Symbol('TSLA')
# start_dt = datetime(2023, 5, 22)
# end_dt = datetime(2023, 5, 23)
# im = plot_bars(instrument.collection(start_dt, end_dt), start_dt, end_dt, as_np_array=True, save=True, show=True)


def get_obs_shape():
    today = datetime.today()
    monday = today - timedelta(days=today.weekday())
    wednesday = monday + timedelta(days=2)
    symbol = Symbol('TSLA')
    data = plot_bars(symbol.collection(monday, wednesday)['TSLA'], monday, wednesday, as_np_array=True)
    print(data.shape)
