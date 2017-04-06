import numpy as np
import networkx as nx


def get_distance(graph):
    """
    Get distance between each pair of nodes.
    If there is no path between pair (i, j), regard the distance as np.inf
    :param graph: network.Graph
    :return: dictionary
        distance between each pair of nodes
    """
    distance = dict()
    for idx, i in enumerate(graph.nodes()):
        for j in graph.nodes()[idx+1:]:
            try:
                distance[(i, j)] = nx.shortest_path_length(graph, i, j)
            except nx.NetworkXNoPath:
                distance[(i, j)] = np.inf
    return distance


def get_distribution(graph, target, y_type='frequency'):
    """
    get the distribution of graph's properties.
    :param graph: networkx.Graph
    :param target: string
        specify the target property whose distribution is needed
    :param y_type: string
        specify the y axis from 'proportion' and 'frequency' at present
    :return: (x, y)
        sequence x includes all the target property's value
        sequence y includes y_type corresponding to x's elements
    """
    # get the sequence
    if target == 'degree':
        dictionary = nx.degree(graph)
    elif target == 'cc':
        dictionary = nx.clustering(graph)
    elif target == 'distance':
        dictionary = get_distance(graph)
    else:
        raise ValueError('The {} is not a supported target at present.'.format(target))
    sequence = dictionary.values()
    seq = sorted(np.unique(sequence))

    # calculate the distribution
    x, y = [], []
    for i in seq:
        x.append(i)
        temp_seq = np.equal(sequence, i)
        y.append(sum(temp_seq))
    if y_type == 'proportion':
        y = np.array(y, 'float64') / dictionary.__len__()
    elif y_type == 'frequency':
        pass
    else:
        raise ValueError('The {} is not supported at present'.format(y_type))

    return x, y


def cc_degree_relationship(graph):
    """
    get the relationship between clustering coefficient and degree
    :param graph: networkx.Graph
    :return: (degree, cc)
        degree includes degrees corresponding to graph's nodes
        cc includes clustering coefficient corresponding to graph's nodes
    """
    degree_dict = nx.degree(graph)
    cc_dict = nx.clustering(graph)

    degree, cc = [], []
    for key in graph.nodes():
        degree.append(degree_dict[key])
        cc.append(cc_dict[key])

    return degree, cc
