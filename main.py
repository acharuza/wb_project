import pandas as pd
import networkx as nx
import numpy as np
from density import density_g
from similarity import similarity_f


def create_graph(edges, vertices):
    G = nx.Graph()
    G.add_nodes_from(vertices['id'].tolist())
    G.add_edges_from([(edges['id1'][i], edges['id2'][i]) for i in range(len(edges))])
    return G


def read_files(graph_nr, hic_size):
    edges = pd.read_csv(f'data/WB_mesh/d{graph_nr}_E.csv')
    vertices = pd.read_csv(f'data/WB_mesh/d{graph_nr}_V.csv')

    if hic_size not in [20, 30, 50, 100, 150, 207]:
        hic_size = 50
    if hic_size < 100:
        hic_size = f'0{hic_size}'
    hic_map = np.load(f'data/hic/hic_{hic_size}.npy')

    return edges, vertices, hic_map


def main():
    edges, vertices, hic_map = read_files(8, 50)
    G = create_graph(edges, vertices)
    structures = density_g(None, G)
    print(structures)
    print(similarity_f(structures[3], vertices, hic_map))


if __name__ == '__main__':
    main()
