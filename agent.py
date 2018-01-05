import numpy as np
import random


class Agent(object):
    # all agents have the same R G alpha
    reward, alpha = None, None

    @staticmethod
    def set_reward(r):
        Agent.reward = r

    @staticmethod
    def set_alpha(a):
        Agent.alpha = a

    def __init__(self):
        self.Q = np.zeros((1, 2), np.float32)       # 2 actions each agent

    def choose_action(self, seed=None):
        if seed is not None:
            random.seed(seed)

        if self.Q[1] == self.Q[0]:
            return random.choice(range(2))

        if self.Q[1] > self.Q[0]:
            return 1

        if self.Q[1] < self.Q[0]:
            return 0

    def update(self, your_action, joint_action):
        self.Q[your_action] = (1 - self.alpha) * self.Q[your_action] + self.alpha * (
            self.reward[joint_action[0]][joint_action[1]])


if __name__ == '__main__':
    player = Agent()
    pass
