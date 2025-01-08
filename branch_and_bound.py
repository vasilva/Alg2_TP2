import numpy as np
import networkx as nx


maxsize = np.inf
final_res = maxsize


def first_min(adj, i, N):
    """
    Find the minimum distance between the node and the other nodes.

    Args:
        adj (np.ndarray): The adjacency matrix of the graph.
        i (int): The index of the node.
        N (int): The number of nodes in the graph.

    Returns:
        min (int): The minimum distance between the node and
    """
    min = maxsize
    for k in range(N):
        if adj[i][k] < min and i != k:
            min = adj[i][k]
    return min


def second_min(adj, i, N):
    """
    Find the second minimum distance between the node and the other nodes.

    Args:
        adj (np.ndarray): The adjacency matrix of the graph.
        i (int): The index of the node.
        N (int): The number of nodes in the graph.

    Returns:
        second (int): The second minimum distance between the node and the other nodes.
    """
    first, second = maxsize, maxsize
    for j in range(N):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]
        elif adj[i][j] <= second and adj[i][j] != first:
            second = adj[i][j]
    return second


def TSPRec(adj, N, curr_bound, curr_weight, level, curr_path, final_path, visited):
    """
    The recursive function to find the shortest path between all nodes.

    Args:
        adj (np.ndarray): The adjacency matrix of the graph.
        N (int): The number of nodes in the graph.
        curr_bound (int): The current bound of the graph.
        curr_weight (int): The current weight of the graph.
        level (int): The current level of the graph.
        curr_path (list): The current path of the graph.
        final_path (list): The final path
        visited (list): The visited nodes of the graph.
    """
    global final_res
    if level == N:
        if adj[curr_path[level - 1]][curr_path[0]] != 0:

            curr_res = curr_weight + adj[curr_path[level - 1]][curr_path[0]]
            if curr_res < final_res:
                final_path[: N + 1] = curr_path[:]
                final_path[N] = curr_path[0]
                final_res = curr_res
        return

    for i in range(N):
        if adj[curr_path[level - 1]][i] != 0 and visited[i] == False:
            temp = curr_bound
            curr_weight += adj[curr_path[level - 1]][i]

            if level == 1:
                curr_bound -= (
                    first_min(adj, curr_path[level - 1], N) + first_min(adj, i, N)
                ) / 2
            else:
                curr_bound -= (
                    second_min(adj, curr_path[level - 1], N) + first_min(adj, i, N)
                ) / 2

            if curr_bound + curr_weight < final_res:
                curr_path[level] = i
                visited[i] = True

                TSPRec(
                    adj,
                    N,
                    curr_bound,
                    curr_weight,
                    level + 1,
                    curr_path,
                    final_path,
                    visited,
                )

            curr_weight -= adj[curr_path[level - 1]][i]
            curr_bound = temp

            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True


def TSP(G):
    """
    Find the shortest path between all nodes.
    Args:


        Returns:
        final_path (list): The shortest path between all nodes.
        final_res (float):
    """

    N = len(G)
    adj = nx.to_numpy_array(G)
    curr_bound = 0
    curr_path = [-1] * (N + 1)
    final_path = [None] * (N + 1)
    visited = [False] * N

    for i in range(N):
        curr_bound += first_min(adj, i, N) + second_min(adj, i, N)

    curr_bound = int(curr_bound / 2)
    visited[0] = True
    curr_path[0] = 0

    TSPRec(adj, N, curr_bound, 0, 1, curr_path, final_path, visited)

    return final_res, final_path


if __name__ == "__main__":
    adj = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]

    adj = np.array(adj)

    G = nx.from_numpy_array(adj)
    N = len(G)

    final_res, final_path = TSP(G)

    print("Minimum cost :", final_res)
    print("Path Taken : ", end=" ")
    for i in range(N + 1):
        print(final_path[i], end=" ")
    print()
