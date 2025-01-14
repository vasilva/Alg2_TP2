# Trabalho Prático 2 – Soluções para problemas difíceis
## Vinícius Alexandre da Silva

Código fonte e Arquivos:

`main.py`: Programa principal do projeto. Faz as leitura dos arquivos .tsp, cria o Grafo e roda o algoritmo correspondente.
Usage: python3 main.py [filename.tsp] [tat|bb|ch]

`tsp.py`: Contém a classe TSP que possui os algoritmos Branch and Bound, Twice Around the Tree e Christofides.

`data/`: Pasta com todos os arquivos .tsp de entrada.

`dados e graficos.ipynb`: Notebook com a tabela de dados gerados e os gráficos produzidos a partir dessa tabela.

`Soluções para problemas difíceis - Problema do Caixeiro Viajante.pdf`: Documentação do trabalho.

`main_bb.sh`, `main_ch.sh`, `main_tat.sh`: Scripts para rodar todas as instâncias de entrada com o respectivo algoritmo com tempo limite de 30 minutos.
