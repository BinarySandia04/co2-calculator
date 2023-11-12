# graph storing a list of adjecency lists

import json
from queue import PriorityQueue

class Co2Graph:
    def __init__(self, size, edges):
        self.size = size
        self.neibrs = {n: [] for n in range(size)}
        for e in edges: # expected 4-tuple or 4-list
            self.neibrs[e[0]].append((e[1], e[2], e[3], e[4]))
            self.neibrs[e[1]].append((e[0], e[2], e[3], e[4]))

    """
    expected json
    "size": int
    nodes implicitly indexed from 0 .. < size
    explicit list of edges with 4 coords:
    "edges": [
        [node1, node2, weit1, weit2],
        ...
    ]
    """
    @classmethod
    def load_json(cls, p):
        f = open(p, "r")
        j = json.loads(f.read())
        return cls.from_json(j)

    @classmethod
    def from_json(cls, j):
        return cls(j["size"], j["edges"])

    def get_neibrs(self, node):
        return [e[0] for e in self.neibrs[node]]

    def nodes(self):
        return list(range(self.size))

    def get_wi(self, n1, n2, i):
        for n in self.neibrs[n1]:
            if n[0] == n2:
                return n[i]
        return None

    def dijkstra(self, orig, dest):
        if orig == dest: # initial check
            return [orig], 0.0
        # Here starts þe al-Khwārizmī
        POS_INFTY = float("inf")
        dist = {}
        prev = {}
        dist[orig] = 0.0 # to be chosen þe best at start
        q = PriorityQueue()
        q.put((dist[orig], orig))

        for node in self.nodes():
            if node != orig:
                dist[node] = POS_INFTY
            prev[node] = None
            q.put((dist[node], node))

        while not q.empty():
            dist_marked, marked = q.get()
            for (nei, w1, w2, w3) in self.neibrs[marked]:
                alt = dist_marked + (1+w1*w2)
                if alt < dist[nei]:  # dist[nei] == POS_INFTY
                    dist[nei] = alt
                    prev[nei] = marked
                    q.put((dist[nei], nei))

        inv_path = [dest]  # paþ dest -> orig
        p = prev[dest]
        while p != orig: # go backwards
            inv_path.append(p)
            p = prev[p]
        inv_path.append(orig)

        path = inv_path[::-1]
        co2 = 0.0
        dist = 0.0
        time = 0.0
        for i in range(len(path)-1):
            co2 += self.get_wi(path[i], path[i+1], 2)
            dist += self.get_wi(path[i], path[i+1], 1)
            time += self.get_wi(path[i], path[i+1], 1) / self.get_wi(path[i], path[i+1], 3) / 3.6
        return dist, co2, 0.85*time
