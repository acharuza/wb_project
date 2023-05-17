import numpy as np
import scipy.interpolate as inter
from skimage.transform import resize


def similarity_f(structure, vertices, hic_map):
    '''
    :param structure: list of vertices' ids representing generated structure
    :param vertices: df with info about vertices
    :param hic_map: numpy array
    :return: pearson correlation between inversed distance matrix of the structure and hic_map
    '''
    n = len(structure)
    distance_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            a = np.array([vertices[vertices['id'] == structure[i]]['x'],
                         vertices[vertices['id'] == structure[i]]['y'],
                         vertices[vertices['id'] == structure[i]]['z']])
            b = np.array([vertices[vertices['id'] == structure[j]]['x'],
                         vertices[vertices['id'] == structure[j]]['y'],
                         vertices[vertices['id'] == structure[j]]['z']])
            distance_matrix[i, j] = np.sqrt(np.sum((a-b)**2))

    if distance_matrix.shape[0] < hic_map.shape[0]:
        vals = np.reshape(distance_matrix, distance_matrix.size)
        pts = np.array([[i, j] for i in range(n) for j in range(n)])
        grid_x, grid_y = np.mgrid[0:1:hic_map.shape[0] * 1j, 0:1:hic_map.shape[0] * 1j]
        distance_matrix = inter.griddata(pts, vals, (grid_x, grid_y), method='linear')

    elif distance_matrix.shape[0] > hic_map.shape[0]:
        distance_matrix = resize(distance_matrix, (50, 50), mode='constant')

    distance_matrix = np.linalg.inv(distance_matrix)
    pearson = np.corrcoef(distance_matrix, hic_map)[0, 1]
    return pearson
