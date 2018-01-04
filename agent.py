import numpy as np


class Agent(object):
    game_matrix = [[]]  # contains reward matrix

    def __init__(self, r, gamma, a):
        self.Q = np.zeros((6, 6), np.float32)
        self.R = r
        self.G = gamma
        self.alpha = a

    def main_loop(self, episode):
        for _ in range(episode):
            state = np.random.random_integers(0, 4)
            while state != 5:
                possible_action = []
                for i in range(len(self.R[state])):
                    if self.R[state][i] > -1:
                        possible_action.append(i)
                action = np.random.choice(possible_action)
                self.Q[state, action] = (1 - self.alpha) * self.Q[state, action] + self.alpha * (self.R[state, action] + self.G * (max(self.Q[action])))
                state = action

