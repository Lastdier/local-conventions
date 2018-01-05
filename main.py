import numpy as np
import agent
import random
import random_graph


# reward of this game
COORDINATION_GAME = np.array([
    [(4, 4), (-1, -1)],
    [(-1, -1), (4, 4)]
])

SOCIAL_DILEMMA_GAME = np.array([
    [(-1, -1), (3, 2)],
    [(2, 3), (1, 1)]
])


class QLearning(object):

    def __init__(self, alpha, graph):
        agent.Agent.set_reward(COORDINATION_GAME)
        agent.Agent.set_alpha(alpha)
        self.graph = graph
        self.agent_pool = [agent.Agent() for _ in range(len(self.graph))]

    def main_loop(self, episode, seed=None):
        if seed is not None:
            random.seed(seed)

        for _ in range(episode):
            checked = set()
            for p1 in range(len(self.graph)):
                if p1 in checked:
                    continue

                if len(self.graph[p1]) < 1:
                    continue

                potential_p2 = self.graph[p1] - checked     # nodes in graph[p1] but not in checked
                if len(potential_p2) < 1:       # when every node p1 connect to is checked
                    continue
                p2 = random.choice(potential_p2)

                # players choose their action
                a1 = self.agent_pool[p1].choose_action(seed=seed)
                a2 = self.agent_pool[p2].choose_action(seed=seed)

                # players update their Q table
                self.agent_pool[p1].update(a1, (a1, a2))
                self.agent_pool[p2].update(a2, (a1, a2))

                checked.add(p1)
                checked.add(p2)


if __name__ == "__main__":
    g = random_graph.gaussian_random_partition_graph(100, 10, .7, .5, .1)
    e = QLearning(.5, g)
    e.main_loop(500)
