import agent
import random
import random_graph


# reward of this game
COORDINATION_GAME = [
    [(4, 4), (-1, -1)],
    [(-1, -1), (4, 4)]
]

five_COORDINATION_GAME = [
    [(1, 1), (-1, -1), (-1, -1), (-1, -1), (-1, -1)],
    [(-1, -1), (1, 1), (-1, -1), (-1, -1), (-1, -1)],
    [(-1, -1), (-1, -1), (1, 1), (-1, -1), (-1, -1)],
    [(-1, -1), (-1, -1), (-1, -1), (1, 1), (-1, -1)],
    [(-1, -1), (-1, -1), (-1, -1), (-1, -1), (1, 1)]
]

SOCIAL_DILEMMA_GAME = [
    [(-1, -1), (3, 2)],
    [(2, 3), (1, 1)]
]


class QLearning(object):

    def __init__(self, alpha, graph):
        agent.Agent.set_reward(five_COORDINATION_GAME)
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

                if len(self.graph.nodes[p1]) < 1:
                    continue

                potential_p2 = self.graph.nodes[p1] - checked     # nodes in graph[p1] but not in checked
                if len(potential_p2) < 1:       # when every node p1 connect to is checked
                    continue
                p2 = random.choice(range(len(potential_p2)))
                for _ in range(p2):
                    potential_p2.pop()
                p2 = potential_p2.pop()

                # players choose their action
                a1 = self.agent_pool[p1].choose_action(seed=seed)
                a2 = self.agent_pool[p2].choose_action(seed=seed)

                # players update their Q table
                self.agent_pool[p1].update(0, (a1, a2))
                self.agent_pool[p2].update(1, (a1, a2))

                checked.add(p1)
                checked.add(p2)

    @property
    def local_convention_conformity(self):
        for p in g.partition:
            


if __name__ == "__main__":
    g = random_graph.gaussian_random_partition_graph(5000, 100, .7, .5, .1)
    e = QLearning(.5, g)
    e.main_loop(500)
    pass
