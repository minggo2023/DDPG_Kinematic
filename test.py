import numpy as np
import gymnasium as gym
from gym_kinematic import SailEnv
import matplotlib.pyplot as plt 

env = SailEnv()

env.reset()

x = []
y = []


for i in range(3000):
    x_r, y_r = env.step()

    x.append(x_r)
    y.append(y_r)

plt.plot(x, y)
plt.show()

