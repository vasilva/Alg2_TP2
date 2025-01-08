import numpy as np
import networkx as nx
import pandas as pd
import scipy as sp


def read_tsp(filename: str):
    """
    Ler um arquivo TSP.
    Args:
        filename (str): O nome do arquivo TSP.

    Retorna:
        points (list[(int, int)]): Uma lista de pontos.
        name (str): O nome do problema TSP.
        comment (str): O comentário do problema TSP.
        dimension (int): A dimensão do problema TSP.
    """
    with open(filename, "r") as f:
        for i in range(6):
            line = f.readline().split(":")
            keyword = line[0].strip()
            match keyword:
                case "NAME":
                    name = line[-1].strip()
                case "COMMENT":
                    comment = line[-1].strip()
                case "DIMENSION":
                    dimension = int(line[-1].strip())
                case _:
                    _ = line[-1].strip()
        points = []
        for i in range(dimension):
            _, x, y = f.readline().split()
            points.append((int(x), int(y)))

    return points, name, comment, dimension


def euclidean_distance(x1, y1, x2, y2) -> int:
    """
    Distância euclidiana entre dois pontos.
    Args:
        x1 (int): A coordenada x do primeiro ponto.
        y1 (int): A coordenada y do primeiro ponto.
        x2 (int): A coordenada x do segundo ponto.
        y2 (int): A coordenada y do segundo ponto.

    Retorna:
        int: A distância euclidiana entre os dois pontos.
    """
    return int(np.round(np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)))


def complete_graph(points, dimension) -> nx.Graph:
    """
    Cria um grafo completo com n nós.
    Args:
        points (list[(int, int)]): Uma lista de pontos.
        dimension (int): A dimensão do problema TSP.

    Retorna:
        nx.Graph: O grafo completo.
    """
    G = nx.Graph()
    G.add_nodes_from(range(1, dimension + 1))
    for i in range(1, dimension + 1):
        for j in range(i + 1, dimension + 1):
            w = euclidean_distance(*points[i - 1], *points[j - 1])
            G.add_edge(i, j, weight=w)
    return G


if __name__ == "__main__":
    points, name, comment, dim = read_tsp("data/a280.tsp")
    G = complete_graph(points, dim)
    print(str(G))
