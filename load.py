from gym_kinematic import SailEnv
from stable_baselines3 import DDPG
import matplotlib.pyplot as plt

env = SailEnv() 

model = DDPG.load('Trained_model/0.25pi', env = env)
obs, _ = env.reset()
done = False

x = []
y = []

while not done:
    action, _ = model.predict(obs)
    obs, _, done, _, info = env.step(action)
    x.append(info['x'])
    y.append(info['y'])

f = open("ddpg_slope.txt","w")
f.writelines(str(x))
f.writelines(str(y))
f.close()

plt.plot([2.5, 100], [2.5, 100])
plt.plot(x, y)
plt.show()