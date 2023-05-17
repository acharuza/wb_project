from random import randint


def density_g(structure, graph):
    '''
    :param structure: list of vertices' ids representing initial structure
    :param graph: networkx graph inside which structure is created
    :return structures: list of changes possible for initial structure
    '''
    structures = []
    if structure is None:
        a = randint(0, len(graph.edges) - 1)
        structure = [list(graph.edges)[a][0], list(graph.edges)[a][1]]

    if len(structure) > 2:
        structures.append(structure[:len(structure) - 1])
        structures.append(structure[1:])

    connected_edges = graph.edges(structure[len(structure) - 1])
    for edge in connected_edges:
        if edge[1] not in structure:
            structures.append(structure + [edge[1]])

    connected_edges = graph.edges(structure[0])
    for edge in connected_edges:
        if edge[1] not in structure:
            structures.append([edge[1]] + structure)

    return structures
