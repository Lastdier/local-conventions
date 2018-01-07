import random


class Agent(object):
    # all agents have the same R G alpha
    reward, alpha, epsilon = None, None, None

    @staticmethod
    def set_reward(r):
        Agent.reward = r

    @staticmethod
    def set_alpha(a):
        Agent.alpha = a

    @staticmethod
    def set_epsilon(e):
        Agent.epsilon = e

    @staticmethod
    def number_of_action():
        return len(Agent.reward[0])

    def __init__(self):
        self.Q = [0. for _ in range(len(Agent.reward[0]))]       # 2 actions each agent

    def choose_max_action(self, seed=None):
        if seed is not None:
            random.seed(seed)

        max_q = -99999.
        m = []
        for i in range(len(self.Q)):
            if self.Q[i] > max_q:
                max_q = self.Q[i]
                m = [i]
            elif self.Q[i] == max_q:
                m.append(i)

        return random.choice(m)

    def epsilon_greedy(self, seed=None):
        if seed is not None:
            random.seed(seed)

        if random.random() <= Agent.epsilon:
            return random.choice(range(Agent.number_of_action()))
        else:
            return self.choose_max_action(seed=seed)

    def update(self, player, joint_action):
        self.Q[joint_action[player]] = (1 - self.alpha) * self.Q[joint_action[player]] + self.alpha * (
            self.reward[joint_action[0]][joint_action[1]][player])


if __name__ == '__main__':
    p = Agent()
    pass
