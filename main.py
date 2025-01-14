import numpy as np
import networkx as nx
import os
from tsp import TSP
import sys


def open_tsp_files(path):
    """
    Retorna a lista de arquivos .tsp no diretório especificado.

    Args:
        path (str): O caminho para o diretório que contém os arquivos .tsp.

    Returns:
        list: Uma lista com os nomes dos arquivos .tsp no diretório.
    """
    files = os.listdir(path)
    files = [file for file in files if file.endswith(".tsp")]
    return files


def get_bounds():
    """
    Abre o arquivo bounds.txt e retorna os resultados ótimos.

    Returns:
        bounds (dict): Os resultados ótimos de cada arquivo.
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

    Returns:
        points (list[(int, int)]): Uma lista de pontos.
        name (str): O nome do problema TSP.
        comment (str): O comentário do problema TSP.
        dimension (int): Tamanho do problema TSP.
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

    Returns:
        int: A distância euclidiana entre os dois pontos.
    """
    return int(np.rint(np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)))


def complete_graph(points) -> nx.Graph:
    """
    Cria um grafo completo com n nós.
    Args:
        points (list[(int, int)]): Uma lista com coordenadas (x,y) dos pontos.

    Returns:
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

    match len(sys.argv):
        # Roda todos os arquivos tsp com algoritmo Twice Around the Tree
        case 1:
            path = "data/"
            files = open_tsp_files(path)
            G_dict = {}
            bounds = get_bounds()
            for f in files:
                points, name, comment, dim = read_tsp(f)
                G = complete_graph(points)
                bound = bounds[f]
                G_dict[f"{name}"] = (G, comment, bound)

            for name, (G, _, bound) in G_dict.items():
                with open(f"logs/tat/profile_{name}_tat.log", "w+") as sys.stdout:
                    t = TSP(G)
                    final_res, final_path = t("tat")
                    print(f"{name = }")
                    print(f"{bound = }")
                    print(f"{final_res = }")

        case 2:
            # Roda o arquivo passado como argumento com o
            # algoritmo Twice Around the Tree
            filename = sys.argv[1]
            points, name, comment, dim = read_tsp(filename)
            G = complete_graph(points)
            filename = filename.replace("data/", "")
            bound = get_bounds()[filename]
            with open(f"logs/tat/profile_{name}_tat.log", "w+") as sys.stdout:
                t = TSP(G)
                final_res, final_path = t("tat")
                print(f"{name = }")
                print(f"{bound = }")
                print(f"{final_res = }")

        case 3:
            # Roda o arquivo passado como argumento com o
            # algoritmo passado como argumento
            filename = sys.argv[1]
            alg = sys.argv[2]
            points, name, comment, dim = read_tsp(filename)
            G = complete_graph(points)
            filename = filename.replace("data/", "")
            bound = get_bounds()[filename]
            with open(f"logs/{alg}/profile_{name}_{alg}.log", "w+") as sys.stdout:
                t = TSP(G)
                final_res, final_path = t(alg)
                print(f"{name = }")
                print(f"{bound = }")
                print(f"{final_res = }")

        case _:
            usage = (
                "Usage: python3 main.py (optional)[filename.tsp] (optional)[bb|tat|ch]"
            )
            raise ValueError(usage)
