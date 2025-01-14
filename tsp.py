import numpy as np
import networkx as nx


class TSP:
    """
    Classe TSP para resolver o Problema do Caixeiro Viajante.
    """

    def __init__(self, G: nx.Graph):
        """
        Inicializa a classe TSP.

        Args:
            G (nx.Graph): O grafo a ser resolvido.
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
        Retorna o número de nós no grafo.

        Retorna:
            int: O número de nós no grafo.
        """
        return self.N

    def __call__(self, algorithm="bb"):
        """
        Encontra o caminho mais curto entre todos os nós.

        Args:
            algorithm (str): O algoritmo a ser usado. As escolhas válidas são: Branch and Bound: `bb`, Twice Around the Tree: `tat` ou Christofides: `ch`. O padrão é `bb`.

        Returns:
            final_res (int): O custo do caminho mais curto.
            final_path (list): O caminho mais curto entre todos os nós.
        """
        match algorithm:
            case "bb":
                return self.branch_bound()
            case "tat":
                return self.twice_around_tree()
            case "ch":
                return self.christofides()
            case _:
                raise ValueError("Algoritmo inválido. Escolha 'bb', 'tat' ou 'ch'.")

    def pri_seg_min(self, i):
        """
        Encontra a menor e segunda menor distâncias entre um nó e os outros nós.

        Args:
            i (int): O índice do nó.

        Returns:
            primeiro (int): A distância mínima entre um nó e os outros nós.
            segundo (int): A segunda menor distância entre um nó e os outros nós.
        """
        primeiro, segundo = np.inf, np.inf
        for j in range(self.N):
            if i == j:
                continue
            if self.adj[i][j] <= primeiro:
                segundo = primeiro
                primeiro = self.adj[i][j]
            elif self.adj[i][j] <= segundo and self.adj[i][j] != primeiro:
                segundo = self.adj[i][j]
        return primeiro, segundo

    def branch_bound(self):
        """
        Encontra o caminho mais curto entre todos os nós usando Branch and Bound.

        Returns:
            final_res (int): O custo do caminho mais curto.
            final_path (list): O caminho mais curto entre todos os nós.
        """
        # Calcula o limite inicial
        for i in range(self.N):
            primeiro, segundo = self.pri_seg_min(i)
            self.curr_bound += primeiro + segundo

        # Arredondando o limite inferior para um inteiro
        self.curr_bound = int(np.rint(self.curr_bound / 2))

        # Começa no vértice 1, então o primeiro vértice
        # em curr_path[] é 0
        self.visited[0] = True
        self.curr_path[0] = 0

        # Faz a chamada da função recursiva
        self.branch_bound_Rec(curr_weight=0, level=1)

        return int(self.final_res), self.final_path

    def branch_bound_Rec(self, curr_weight, level):
        """
        A função recursiva do Branch and Bound para encontrar o caminho mais curto entre todos os nós.

        Args:
            curr_weight (int): O peso atual do grafo.
            level (int): O nível atual do grafo.
        """
        # Caso base é quando atingimos o nível N
        # o que significa que cobrimos todos os nós uma vez
        if level == self.N:
            # Verifica se há uma aresta do
            # último vértice no caminho de volta ao primeiro vértice
            if self.adj[self.curr_path[level - 1]][self.curr_path[0]] != 0:
                # curr_res tem o peso total
                # da solução obtida
                curr_res = (
                    curr_weight + self.adj[self.curr_path[level - 1]][self.curr_path[0]]
                )
            # Resposta final
            if curr_res < self.final_res:
                self.final_path[: self.N + 1] = self.curr_path[:]
                self.final_path[self.N] = self.curr_path[0]
                self.final_res = curr_res
            return

        # Para qualquer outro nível, iterar por todos os vértices
        # para construir a árvore de espaço de busca recursivamente
        for i in range(self.N):
            # Considerar o próximo vértice se não for o mesmo
            # (entrada diagonal na matriz de adjacência e ainda não foi visitado)
            if self.adj[self.curr_path[level - 1]][i] != 0 and self.visited[i] == False:
                temp = self.curr_bound
                curr_weight += self.adj[self.curr_path[level - 1]][i]
                primeiro, segundo = self.pri_seg_min(self.curr_path[level - 1])

                # Cálculo diferente de curr_bound
                # para o nível 2 em relação aos outros níveis
                if level == 1:
                    self.curr_bound -= (primeiro + self.pri_seg_min(i)[0]) / 2
                else:
                    self.curr_bound -= (segundo + self.pri_seg_min(i)[0]) / 2
                # curr_bound + curr_weight é o limite inferior real para o nó visitado.
                # Se o limite inferior atual < final_res,
                # precisa-se explorar o nó mais a fundo
                if self.curr_bound + curr_weight < self.final_res:
                    self.curr_path[level] = i
                    self.visited[i] = True

                    # Chamada recursiva para o próximo nível
                    self.branch_bound_Rec(curr_weight, level + 1)

                # Caso contrário, tem que podar o nó, resetando
                # todas as mudanças em curr_weight e curr_bound
                curr_weight -= self.adj[self.curr_path[level - 1]][i]
                self.curr_bound = temp

                # Também resetar o array de visitados
                self.visited = [False] * len(self.visited)
                for j in range(level):
                    if self.curr_path[j] != -1:
                        self.visited[self.curr_path[j]] = True

    def twice_around_tree(self):
        """
        Encontra o caminho mais curto entre todos os nós usando Twice Around the Tree

        Returns:
            final_res (int): O custo do caminho mais curto.
            final_path (list): O caminho mais curto entre todos os nós.
        """
        # Cria a Árvore Geradora Mínima usando o algoritmo de Prim.
        mst = nx.minimum_spanning_tree(self.Graph, algorithm="prim")

        # Faz a travessia em pré-ordem do DFS da Árvore Geradora Mínima.
        dfs_preorder = list(nx.dfs_preorder_nodes(mst, source=0))

        # Acumula as distâncias entre os vértices da lista do dfs
        self.final_res = 0
        for i in dfs_preorder:
            self.final_res += self.adj[dfs_preorder[i - 1]][dfs_preorder[i]]

        self.final_path = dfs_preorder + [dfs_preorder[0]]
        return int(self.final_res), self.final_path

    def christofides(self):
        """
        Encontra o caminho mais curto entre todos os nós usando Christofides

        Returns:
            final_res (int): O custo do caminho mais curto.
            final_path (list): O caminho mais curto entre todos os nós.
        """
        # Usa-se a função Christofides da biblioteca NetworkX
        self.final_path = nx.algorithms.approximation.christofides(self.Graph)
        n = len(self.final_path)

        # Acumula as distâncias entre os vértices da lista criada pelo Christofides
        self.final_res = 0
        for i in range(1, n):
            self.final_res += self.adj[self.final_path[i - 1]][self.final_path[i]]
        return int(self.final_res), self.final_path
