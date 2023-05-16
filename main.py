import pandas as pd
from random import randint
import networkx as nx
import numpy as np
import scipy.interpolate as inter


def create_graph(edges, vertices):
    G = nx.Graph()
    G.add_nodes_from(vertices['id'].tolist())
    G.add_edges_from([(edges['id1'][i], edges['id2'][i]) for i in range(len(edges))])
    return G


def density_g(structure, G):
    '''
    :param structure: list of vendices' ids representing initial structure
    :param G: networkx graph inside which structure is created
    :return structures: list of changes possible for initial structure
    '''

    # todo: zrobić w drugą stronę rozrastanie się i malenie też

    structures = []
    if structure is None:
        a = randint(0, len(G.edges) - 1)
        structure = [list(G.edges)[a][0], list(G.edges)[a][1]]

    connected_edges = G.edges(structure[len(structure) - 1])
    if len(structure) > 2:
        structures.append(structure[:len(structure) - 1])

    for edge in connected_edges:
        if edge[1] not in structure:
            structures.append(structure + [edge[1]])

    return structures


def similarity_f(structure, vertices, hic_map):
    '''
    wziąć strukturę i zrobić macierz dystansów długość struktury x długość struktury
    potem interpolacja by się wymiary zgadzały z mapą hic
    potem odwrócić macierz
    i potem pearson?

    :param structure:
    :param hic_map:
    :return:
    '''
    # todo: interpolacja kodem poniżej, odwrócić macierz, pearson z mapą hic
    distance_matrix = np.zeros((len(structure), len(structure)))

    for i in range(len(structure)):
        for j in range(len(structure)):
            # a i b to są współrzędne tych punkcików
            a = np.array([vertices[vertices['id'] == structure[i]]['x'],
                         vertices[vertices['id'] == structure[i]]['y'],
                         vertices[vertices['id'] == structure[i]]['z']])
            b = np.array([vertices[vertices['id'] == structure[j]]['x'],
                         vertices[vertices['id'] == structure[j]]['y'],
                         vertices[vertices['id'] == structure[j]]['z']])
            distance_matrix[i, j] = np.sqrt(np.sum((a-b)**2))

    vals = np.reshape(distance_matrix, distance_matrix.size)
    pts = np.array([[i, j] for i in [0.0, 0.5, 1.0] for j in [0.0, 0.5, 1.0]])
    grid_x, grid_y = np.mgrid[0:1:50j, 0:1:50j] # 50x50
    grid_z = inter.griddata(pts, vals, (grid_x, grid_y), method='linear')

    distance_matrix = np.linalg.inv(grid_z)

    corr = np.corrcoef(distance_matrix, hic_map)

    # Zwracamy macierz czy jakąś wartość?
    # print(corr[1,0])

    return corr

def main():
    edges = pd.read_csv('data/WB_mesh/d8_E.csv')
    vertices = pd.read_csv('data/WB_mesh/d8_V.csv')
    G = create_graph(edges, vertices)
    structures = density_g(None, G)
    print(structures)
    hic = np.load('data/hic_050.npy')
    print(hic)
    print(similarity_f(structures[1], vertices, hic))
    
    # A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # vals = np.reshape(A, (9))
    # pts = np.array([[i, j] for i in [0.0, 0.5, 1.0] for j in [0.0, 0.5, 1.0]])
    # grid_x, grid_y = np.mgrid[0:1:7j, 0:1:5j]
    # grid_z = inter.griddata(pts, vals, (grid_x, grid_y), method='linear')


if __name__ == '__main__':
    main()
