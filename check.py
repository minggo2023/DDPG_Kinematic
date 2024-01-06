import gymnasium as gym
from gym_kinematic import SailEnv
from stable_baselines3.common.env_checker import check_env

env = SailEnv()

check_env(env)