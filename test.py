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

    if x_r >=100:
        break

f = open("j.txt","w")
f.writelines(str(x))
f.writelines(str(y))
f.close()

plt.plot(x, y)
plt.show()

