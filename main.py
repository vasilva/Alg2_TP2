import numpy as np
import networkx as nx
import pandas as pd
import os
import cProfile
from tsp import TSP


def open_tsp_files():
    path = "data/"
    files = os.listdir(path)
    files = [file for file in files if file.endswith(".tsp")]
    return path, files


def get_bounds():
    """
    Open the bounds.txt file and return the bounds.

    Returns:
        bounds (dict): The bounds.
    """
    with open("data/bounds.txt", "r") as f:
        bounds = f.readlines()

    bounds = [bound.strip().split() for bound in bounds]
    bounds = {bound[0]: int(bound[1]) for bound in bounds}
    return bounds


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
                    dim = int(line[-1].strip())
                case _:
                    _ = line[-1].strip()
        points = []
        for i in range(dim):
            _, x, y = f.readline().split()
            points.append((float(x), float(y)))

    return points, name, comment, dim


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
    return int(np.rint(np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)))


def complete_graph(points) -> nx.Graph:
    """
    Cria um grafo completo com n nós.
    Args:
        points (list[(int, int)]): Uma lista com coordenadas (x,y) dos pontos.

    Retorna:
        nx.Graph: O grafo completo.
    """
    G = nx.Graph()
    dim = len(points)
    G.add_nodes_from(range(dim))
    for i in range(dim):
        for j in range(i + 1, dim):
            w = euclidean_distance(*points[i], *points[j])
            G.add_edge(i, j, weight=w)
    return G


if __name__ == "__main__":

    path, files = open_tsp_files()
    G_dict = {}
    bounds = get_bounds()
    for f in files:
        points, name, comment, dim = read_tsp(path + f)
        G = complete_graph(points)
        bound = bounds[f]
        G_dict[f"{name}"] = (G, comment, bound)

    for name, (G, _, bound) in G_dict.items():
        t = TSP(G)
        cProfile.run(f"t('tat')")
        print(f"{name = }")
        print("-" * 50)
