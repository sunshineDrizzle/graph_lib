import numpy as np
import networkx as nx


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
        dictionary = dict()
        for idx, i in enumerate(graph.nodes()):
            for j in graph.nodes()[idx+1:]:
                dictionary[(i, j)] = nx.shortest_path_length(graph, i, j)
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
