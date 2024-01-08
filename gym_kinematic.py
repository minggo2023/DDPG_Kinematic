import numpy as np
import gymnasium as gym
from gymnasium import spaces

# 帆船相关参数
class SailEnv(gym.Env):
    def __init__(self):
        self.ts = 0.1
        # 初始状态
        self.psi = np.pi / 3
        self.x = 25
        self.y = 25
        
        self.u = 1
        self.ak = np.pi / 4

        # 帆船的固定参数

        self.L=12
        self.Delta=2*self.L
        # 控制器相关参数
        self.kpsi = 0.1
        self.i =  0 

        #　标志位
        self.psi_d = []
        self.t = 0

        # 状态空间的参数        
        self.max_action = np.pi / 2
        self.min_action = - np.pi / 2
        self.action_space = spaces.Box(low=self.min_action, high=self.max_action, shape=(1,), dtype=np.float32)
        
        self.min_x = -2
        self.max_ye = 40.
        self.min_ye = -40.
        self.min_psi_ak = -np.pi
        self.max_psi_ak = np.pi
        self.low_state = np.array( \
            [self.min_ye, self.min_psi_ak], dtype=np.float32)
        self.high_state = np.array( \
            [self.max_ye, self.max_psi_ak], dtype=np.float32)
        self.observation_space = spaces.Box( \
            low=self.low_state, high=self.high_state, dtype=np.float32)


    def step(self,action):
        ye = self.state[0]
        action = action[0]

        # action = -np.arctan(ye / self.Delta)

        psid = self.ak  + action   # Los控制器  调整 路径的角度来实现斜线的跟踪

        if psid > np.pi:                            
            psid = psid - 2 * np.pi  
        elif psid < -np.pi:
            psid = psid + 2 * np.pi
        self.psi_d.append(psid)
    
        if self.i == 0:
            self.dpsid = 0
        elif abs(self.psi_d[-1] - self.psi_d[-2]) >= np.pi:
            self.dpsid = self.dpsid 
        else:
            self.dpsid = (self.psi_d[-1] - self.psi_d[-2]) / self.ts
    
        psic = psid - self.psi

        if psic > np.pi:
            psic = psic - 2 * np.pi
        elif psic < - np.pi:
            psic = psic + 2 * np.pi
    
        alphar  = self.dpsid + self.kpsi * psic

        self.x = self.x + self.u  * self.ts * np.cos(self.psi)
        self.y = self.y + self.u  * self.ts * np.sin(self.psi)
        self.psi = self.psi + alphar * self.ts

        if self.psi > np.pi:
            self.psi = self.psi - 2 * np.pi
        elif self.psi < - np.pi:
            self.psi = self.psi + 2 * np.pi

        reward = self.cal_reward3(ye, self.psi, self.x)

        done = False
        if abs(ye) > self.max_ye or self.x < self.min_x or self.x > 100  :
            done = True
        else:
            done = False
        
        ye = -(self.x - 2.5)*np.sin(self.ak) + (self.y - 2.5)*np.cos(self.ak)

        self.state = np.array(  \
            [ ye, self.psi], dtype=np.float32) 
        
        info = {'x': self.x, 'y':self.y, 'ye':ye}
        print(info)
        
        return self.state, reward, done, False, info
        # return self.x, self.y
    
    def reset(self, seed=None, options=None):
        self.u = 1

        self.i = 0
        self.t = 0

        self.psi_d = []

        """
        系统初始化代码（状态）

        """
        action = 0
        x = 0  # 初始x值的位置
        y = 25  # 初始y值的位置
        psi = np.pi / 3  # 初始psi值

        self.x = x
        self.y = y
        self.psi = psi

        x_0 = 2.5
        y_0 = 2.5
        x_d = 30
        y_d = y_0

        self.x_0 = x_0
        self.y_0 = y_0

        self.ak = np.pi / 4

        psi_ak = self.psi - self.ak
        if psi_ak > np.pi:
            psi_ak = psi_ak - 2 * np.pi
        elif psi_ak < - np.pi:
            psi_ak = psi_ak + 2 * np.pi
        
        ye = -(self.x - 2.5)*np.sin(self.ak) + (self.y - 2.5)*np.cos(self.ak)

        self.state = np.array(  \
            [ye, psi_ak], dtype=np.float32)  #更改型号

        info = {'x': self.x, 'y':self.y, 'ye':ye}

        return self.state, info
    
    def cal_reward3(self, ye, psi, x):
        
        reward_y = 2 * np.exp(-0.7 * ye**2) - 1

        reward_psi = 1.3 * np.exp(-10 * abs(psi)) - 0.3

        # reward_d= - np.sqrt((x - 100)**2 + (y - 2.5)**2) / 4

        reward = reward_y + reward_psi 

        if x > 100:
            reward = reward_y + reward_psi + 100

        return reward

        

        