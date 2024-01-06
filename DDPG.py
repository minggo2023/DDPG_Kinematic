import gymnasium as gym
from stable_baselines3 import DDPG
from stable_baselines3.common.noise import OrnsteinUhlenbeckActionNoise, NormalActionNoise
from gym_kinematic import SailEnv
import os
import numpy as np

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

env = SailEnv()
n_actions = env.action_space.shape[-1]
action_noise = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions), sigma=0.1, theta=0.15)
model = DDPG("MlpPolicy", env, tensorboard_log=log_dir)
model.learn(total_timesteps=1_000_000, progress_bar=True)
model.save("ddpg_r3")