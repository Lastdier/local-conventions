import agent
import random
import random_graph
import math


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

    def __init__(self, alpha, epsilon, graph):
        agent.Agent.set_reward(five_COORDINATION_GAME)
        agent.Agent.set_epsilon(epsilon)
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
                a1 = self.agent_pool[p1].epsilon_greedy(seed=seed)
                a2 = self.agent_pool[p2].epsilon_greedy(seed=seed)

                # players update their Q table
                self.agent_pool[p1].update(0, (a1, a2))
                self.agent_pool[p2].update(1, (a1, a2))

                checked.add(p1)
                checked.add(p2)

            # print self.local_convention_conformity_of_communities

            # print self.global_convention_conformity

            print self.local_convention_conformity_of_system

    @property
    def local_convention_conformity_of_communities(self):
        lcc = [0. for _ in range(len(self.graph.partition))]  # local_convention_conformity list
        agents_action_list = []
        for a in self.agent_pool:
            agents_action_list.append(a.choose_max_action())

        start = 0
        for p in range(len(self.graph.partition)):
            h = 0.
            end = start + len(self.graph.partition[p])
            for action in range(agent.Agent.number_of_action()):
                count = agents_action_list[start:end].count(action)
                count += 0.
                if count == 0:
                    continue
                count /= len(self.graph.partition[p])
                h -= count * math.log(count, 2)
            lcc[p] = 1 - h / math.log(agent.Agent.number_of_action(), 2)
            start = end + 1
        return lcc

    @property
    def local_convention_conformity_of_system(self):
        lcc = self.local_convention_conformity_of_communities
        lcc_of_system = 0.
        for p in range(len(self.graph.partition)):
            lcc_of_system += lcc[p] * len(self.graph.partition[p]) / len(self.graph)

        return lcc_of_system

    @property
    def global_convention_conformity(self):
        agents_action_list = []
        for a in self.agent_pool:
            agents_action_list.append(a.choose_max_action())

        h = 0.
        for action in range(agent.Agent.number_of_action()):
            count = agents_action_list.count(action)
            count += 0.
            if count == 0:
                continue
            count /= len(self.graph)
            h -= count * math.log(count, 2)
        global_convention_conformity = 1 - h / math.log(agent.Agent.number_of_action(), 2)

        return global_convention_conformity


if __name__ == "__main__":
    g = random_graph.gaussian_random_partition_graph(500, 50, 1.1, .5, .1)
    e = QLearning(.5, .1, g)
    e.main_loop(10)
    pass
