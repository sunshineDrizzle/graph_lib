import numpy as np
from networkx import to_scipy_sparse_matrix
from scipy.sparse import dia_matrix


# ---------------------------get information from graph-----------------------------------
def DW_matrices(graph):
    """
    NOTE: copy from skimage.future.graph._ncut.DW_matrices--version: 0.12.3
    Returns the diagonal and weight matrices of a graph.

    Parameters
    ----------
    graph : nx.Graph

    Returns
    -------
    D : csc_matrix
        The diagonal matrix of the graph. ``D[i, i]`` is the sum of weights of
        all edges incident on `i`. All other entries are `0`.
    W : csc_matrix
        The weight matrix of the graph. ``W[i, j]`` is the weight of the edge
        joining `i` to `j`.
    """
    # sparse.eighsh is most efficient with CSC-formatted input
    W = to_scipy_sparse_matrix(graph, format='csc')
    entries = W.sum(axis=0)
    D = dia_matrix((entries, 0), shape=W.shape).tocsc()

    return D, W


def node_attr2array(graph, attrs):
    """
    extract nodes' attributes into a array
    :param graph: nx.Graph
    :param attrs: tuple (e.g. ('ncut label', 'color'))
        nodes' attributes which are going to be saved
    :return: numpy array
        each row_index represents a node; each column represent a nodes' attribute.
    """
    n_vtx = graph.number_of_nodes()
    arr_shape = (n_vtx, len(attrs))
    arr = np.zeros(arr_shape)
    for node, data in graph.nodes_iter(data=True):
        for idx, attr in enumerate(attrs):
            arr[node, idx] = data[attr]
    return arr
