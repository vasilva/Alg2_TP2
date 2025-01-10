import numpy as np
import networkx as nx
from memory_profiler import profile

fp = open(f"mem/mem_profiler.log", "w+")


class TSP:
    """
    TSP class for solving the Travelling Salesman Problem.
    """

    @profile(stream=fp, precision=4)
    def __init__(self, G: nx.Graph):
        """
        Initialize the TSP class.

        Args:
            G (nx.Graph): The graph to be solved.
        """
        self.Graph = G
        self.final_res = np.inf
        self.final_path = [None] * (len(G) + 1)
        self.visited = [False] * (len(G))
        self.curr_bound = 0
        self.curr_path = [-1] * (len(G) + 1)
        self.N = len(G)
        self.adj = nx.to_numpy_array(G)

    def __len__(self):
        """
        Return the number of nodes in the graph.

        Returns:
            int: The number of nodes in the graph.
        """
        return self.N

    def __call__(self, algorithm="bb"):
        """
        Find the shortest path between all nodes.

        Args:
            algorithm (str): The algorithm to use. Valid choices are: Branch and Bound: `bb`, Twice Around the Tree: `tat` or Christofides: `ch`. Default is `bb`.

        Returns:
            final_res (int): The cost of the shortest path.
            final_path (list): The shortest path between all nodes.
        """
        match algorithm:
            case "bb":
                return self.BB_TSP()
            case "tat":
                return self.TAT_TSP()
            case "ch":
                return self.christofides()
            case _:
                raise ValueError("Invalid algorithm. Choose 'bb', 'tat' or 'ch'.")

    def first_min(self, i):
        """
        Find the minimum distance between the node and the other nodes.

        Args:
            i (int): The index of the node.

        Returns:
            min (int): The minimum distance between the node and the other nodes.
        """
        min = self.final_res
        for k in range(self.N):
            if self.adj[i][k] < min and i != k:
                min = self.adj[i][k]
        return min

    def second_min(self, i):
        """
        Find the second minimum distance between the node and the other nodes.

        Args:
            i (int): The index of the node.

        Returns:
            second (int): The second minimum distance between the node and the other nodes.
        """
        first, second = self.final_res, self.final_res
        for j in range(self.N):
            if i == j:
                continue
            if self.adj[i][j] <= first:
                second = first
                first = self.adj[i][j]

            elif self.adj[i][j] <= second and self.adj[i][j] != first:
                second = self.adj[i][j]
        return second

    def copy_final_path(self):
        """
        Function to copy temporary solution to the final solution.
        """
        self.final_path[: self.N + 1] = self.curr_path[:]
        self.final_path[self.N] = self.curr_path[0]

    @profile(stream=fp, precision=4)
    def BB_TSP(self):
        """
        Find the shortest path between all nodes using Branch and Bound.

        Returns:
            final_res (int): The cost of the shortest path.
            final_path (list): The shortest path between all nodes.
        """
        # Compute initial bound
        for i in range(self.N):
            self.curr_bound += self.first_min(i) + self.second_min(i)

        # Rounding off the lower bound to an integer
        self.curr_bound = int(self.curr_bound / 2)

        # We start at vertex 1 so the first vertex
        # in curr_path[] is 0
        self.visited[0] = True
        self.curr_path[0] = 0

        self.TSPRec(curr_weight=0, level=1)

        return int(self.final_res), self.final_path

    @profile(stream=fp, precision=4)
    def TSPRec(self, curr_weight, level):
        """
        The recursive function to find the shortest path between all nodes.

        Args:
            curr_weight (int): The current weight of the graph.
            level (int): The current level of the graph.
        """
        # base case is when we have reached level N
        # which means we have covered all the nodes once
        if level == self.N:

            # check if there is an edge from
            # last vertex in path back to the first vertex
            if self.adj[self.curr_path[level - 1]][self.curr_path[0]] != 0:

                # curr_res has the total weight
                # of the solution we got
                curr_res = (
                    curr_weight + self.adj[self.curr_path[level - 1]][self.curr_path[0]]
                )
            if curr_res < self.final_res:
                self.copy_final_path()
                self.final_res = curr_res

            return

        # for any other level iterate for all vertices
        # to build the search space tree recursively
        for i in range(self.N):

            # Consider next vertex if it is not same
            # (diagonal entry in adjacency matrix and
            #  not visited already)
            if self.adj[self.curr_path[level - 1]][i] != 0 and self.visited[i] == False:
                temp = self.curr_bound
                curr_weight += self.adj[self.curr_path[level - 1]][i]

                # different computation of curr_bound
                # for level 2 from the other levels
                if level == 1:
                    self.curr_bound -= (
                        self.first_min(self.curr_path[level - 1]) + self.first_min(i)
                    ) / 2

                else:
                    self.curr_bound -= (
                        self.second_min(self.curr_path[level - 1]) + self.first_min(i)
                    ) / 2

                # curr_bound + curr_weight is the actual lower bound
                # for the node that we have arrived on.
                # If current lower bound < final_res,
                # we need to explore the node further
                if self.curr_bound + curr_weight < self.final_res:
                    self.curr_path[level] = i
                    self.visited[i] = True

                    # call TSPRec for the next level
                    self.TSPRec(curr_weight, level + 1)

                # Else we have to prune the node by resetting
                # all changes to curr_weight and curr_bound
                curr_weight -= self.adj[self.curr_path[level - 1]][i]
                self.curr_bound = temp

                # Also reset the visited array
                self.visited = [False] * len(self.visited)
                for j in range(level):
                    if self.curr_path[j] != -1:
                        self.visited[self.curr_path[j]] = True

    @profile(stream=fp, precision=4)
    def TAT_TSP(self):
        """
        Find the shortest path between all nodes using Twice Around the Tree

        Returns:
            final_res (int): The cost of the shortest path.
            final_path (list): The shortest path between all nodes.
        """
        # Create the Minimum Spanning Tree using Prim algorithm.
        mst = nx.minimum_spanning_tree(self.Graph, algorithm="prim")

        # Do the preorder DFS transversal of the MST.
        dfs = list(nx.dfs_preorder_nodes(mst, source=0))

        self.full_res = 0
        for i in dfs:
            self.full_res += self.adj[dfs[i - 1]][dfs[i]]

        self.full_walk = dfs + [dfs[0]]
        return int(self.full_res), self.full_walk

    @profile(stream=fp, precision=4)
    def christofides(self):
        """
        Find the shortest path between all nodes using Christofides

        Returns:
            final_res (int): The cost of the shortest path.
            final_path (list): The shortest path between all nodes.
        """
        self.final_path = nx.algorithms.approximation.christofides(self.Graph)
        self.final_res = 0
        for i in self.final_path:
            self.final_res += self.adj[i - 1][i]
        return int(self.final_res), self.final_path
