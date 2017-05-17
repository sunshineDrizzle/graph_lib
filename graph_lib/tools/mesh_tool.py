# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

import numpy as np
from scipy import sparse
from scipy.spatial.distance import pdist
from scipy.stats import pearsonr
from networkx import Graph


# --------------------------------get information from mesh--------------------------
def mesh_edges(faces):
    """
	Copy from FreeROI! Not writed by myself!
    Returns sparse matrix with edges as an adjacency matrix

    Parameters
    ----------
    faces : array of shape [n_triangles x 3]
        The mesh faces

    Returns
    -------
    edges : sparse matrix
        The adjacency matrix
    """
    npoints = np.max(faces) + 1
    nfaces = len(faces)
    a, b, c = faces.T
    edges = sparse.coo_matrix((np.ones(nfaces), (a, b)),
                              shape=(npoints, npoints))
    edges = edges + sparse.coo_matrix((np.ones(nfaces), (b, c)),
                                      shape=(npoints, npoints))
    edges = edges + sparse.coo_matrix((np.ones(nfaces), (c, a)),
                                      shape=(npoints, npoints))
    edges = edges + edges.T
    edges = edges.tocoo()
    return edges


def get_n_ring_neighbor(faces, n=1, ordinal=False):
    """
    get n ring nerghbor from faces array
    :param faces: the array of shape [n_triangles, 3]
    :param n: integer
        specify which ring should be got
    :param ordinal: bool
        True: get the n_th ring neighbor
        False: get the n ring neighbor
    :return: list
        each index of the list represents a vertex number
        each element is a set which includes neighbors of corresponding vertex
    """
    n_vtx = np.max(faces) + 1  # get the number of vertices

    # find 1_ring neighbors' id for each vertex
    coo_w = mesh_edges(faces)
    csr_w = coo_w.tocsr()
    n_ring_neighbors = [csr_w.indices[csr_w.indptr[i]:csr_w.indptr[i+1]] for i in range(n_vtx)]
    n_ring_neighbors = [set(i) for i in n_ring_neighbors]

    if n > 1:
        # find n_ring neighbors
        one_ring_neighbors = [i.copy() for i in n_ring_neighbors]
        n_th_ring_neighbors = [i.copy() for i in n_ring_neighbors]
        # if n>1, go to get more neighbors
        for i in range(n-1):
            for neighbor_set in n_th_ring_neighbors:
                neighbor_set_tmp = neighbor_set.copy()
                for v_id in neighbor_set_tmp:
                    neighbor_set.update(one_ring_neighbors[v_id])

            if i == 0:
                for v_id in range(n_vtx):
                    n_th_ring_neighbors[v_id].remove(v_id)

            for v_id in range(n_vtx):
                n_th_ring_neighbors[v_id] -= n_ring_neighbors[v_id]  # get the (i+2)_th ring neighbors
                n_ring_neighbors[v_id] |= n_th_ring_neighbors[v_id]  # get the (i+2) ring neighbors
    elif n == 1:
        n_th_ring_neighbors = n_ring_neighbors
    else:
        raise RuntimeError("The number of rings should be equal or greater than 1!")

    if ordinal:
        return n_th_ring_neighbors
    else:
        return n_ring_neighbors


# ---------------------transform mesh to graph-related data structure----------------
def mesh2edge_list(faces, n=1, ordinal=False, vtx_signal=None,
                   weight_type=('dissimilar', 'euclidean'), weight_normalization=False):
    """
    get edge_list according to mesh's geometry and vtx_signal
    The edge_list can be used to create graph or adjacent matrix

    Parameters
    ----------
    faces : a array with shape (n_triangles, 3)
    n : integer
        specify which ring should be got
    ordinal : bool
        True: get the n_th ring neighbor
        False: get the n ring neighbor
    vtx_signal : numpy array
        NxM array, N is the number of vertices,
        M is the number of measurements and time points.
    weight_type : (str1, str2)
        The rule used for calculating weights
        such as ('dissimilar', 'euclidean') and ('similar', 'pearson correlation')
    weight_normalization : bool
        If it is False, do nothing.
        If it is True, normalize weights to [0, 1].
            After doing this, greater the weight is, two vertices of the edge are more related.

    Returns
    -------
    row_ind : list
        row indices of edges
    col_ind : list
        column indices of edges
    edge_data : list
        edge data of the edges-zip(row_ind, col_ind)
    """

    n_ring_neighbors = get_n_ring_neighbor(faces, n, ordinal)

    row_ind = [i for i, neighbors in enumerate(n_ring_neighbors) for v_id in neighbors]
    col_ind = [v_id for neighbors in n_ring_neighbors for v_id in neighbors]
    if vtx_signal is None:
        # create unweighted edges
        n_edge = len(row_ind)  # the number of edges
        edge_data = np.ones(n_edge)
    else:
        # calculate weights according to mesh's geometry and vertices' signal
        if weight_type[0] == 'dissimilar':
            edge_data = [pdist(np.c_[vtx_signal[i], vtx_signal[j]].T,
                               metric=weight_type[1])[0] for i, j in zip(row_ind, col_ind)]

            if weight_normalization:
                max_dissimilar = np.max(edge_data)
                min_dissimilar = np.min(edge_data)
                edge_data = [(max_dissimilar-dist)/(max_dissimilar-min_dissimilar) for dist in edge_data]
        elif weight_type[0] == 'similar':
            if weight_type[1] == 'pearson correlation':
                edge_data = [pearsonr(vtx_signal[i], vtx_signal[j])[0] for i, j in zip(row_ind, col_ind)]
            else:
                raise TypeError("The weight_type-{} is not supported now!".format(weight_type))

            if weight_normalization:
                max_similar = np.max(edge_data)
                min_similar = np.min(edge_data)
                edge_data = [(simi-min_similar)/(max_similar-min_similar) for simi in edge_data]
        else:
            raise TypeError("The weight_type-{} is not supported now!".format(weight_type))

    return row_ind, col_ind, edge_data


def mesh2adjacent_matrix(faces, n=1, ordinal=False, vtx_signal=None,
                         weight_type=('dissimilar', 'euclidean'), weight_normalization=False):
    """
    get adjacent matrix according to mesh's geometry and vtx_signal

    Parameters
    ----------
    faces : a array with shape (n_triangles, 3)
    n : integer
        specify which ring should be got
    ordinal : bool
        True: get the n_th ring neighbor
        False: get the n ring neighbor
    vtx_signal : numpy array
        NxM array, N is the number of vertices,
        M is the number of measurements and time points.
    weight_type : (str1, str2)
        The rule used for calculating weights
        such as ('dissimilar', 'euclidean') and ('similar', 'pearson correlation')
    weight_normalization : bool
        If it is False, do nothing.
        If it is True, normalize weights to [0, 1].
            After doing this, greater the weight is, two vertices of the edge are more related.

    Returns
    -------
    adjacent_matrix : coo matrix
    """

    n_vtx = np.max(faces) + 1
    row_ind, col_ind, edge_data = mesh2edge_list(faces, n, ordinal, vtx_signal,
                                                 weight_type, weight_normalization)
    adjacent_matrix = sparse.coo_matrix((edge_data, (row_ind, col_ind)), (n_vtx, n_vtx))

    return adjacent_matrix


def mesh2graph(faces, n=1, ordinal=False, vtx_signal=None,
               weight_type=('dissimilar', 'euclidean'), weight_normalization=False):
    """
    create graph according to mesh's geometry and vtx_signal

    Parameters
    ----------
    faces : a array with shape (n_triangles, 3)
    n : integer
        specify which ring should be got
    ordinal : bool
        True: get the n_th ring neighbor
        False: get the n ring neighbor
    vtx_signal : numpy array
        NxM array, N is the number of vertices,
        M is the number of measurements and time points.
    weight_type : (str1, str2)
        The rule used for calculating weights
        such as ('dissimilar', 'euclidean') and ('similar', 'pearson correlation')
    weight_normalization : bool
        If it is False, do nothing.
        If it is True, normalize weights to [0, 1].
            After doing this, greater the weight is, two vertices of the edge are more related.

    Returns
    -------
    graph : nx.Graph
    """

    row_ind, col_ind, edge_data = mesh2edge_list(faces, n, ordinal, vtx_signal,
                                                 weight_type, weight_normalization)
    graph = Graph()
    # add_weighted_edges_from is faster than from_scipy_sparse_matrix and from_numpy_matrix
    # add_weighted_edges_from is also faster than default constructor
    # To get more related information, please refer to
    # http://stackoverflow.com/questions/24681677/transform-csr-matrix-into-networkx-graph
    graph.add_weighted_edges_from(zip(row_ind, col_ind, edge_data))

    return graph
