# coding in python3.6.0

import networkx as nx
import random


def newman_girvan_benchmark(n_vtx, n_community, z_in, z_out):
    """
    generate newman-girvan benchmark network

    Parameters
    ----------
    n_vtx : integer
        the number of vertices of the graph
    n_community : integer
        the number of communities
    z_in : integer
        the average degree of a vertex within its community
    z_out : integer
        the average degree of a vertex between its community and another community

    Return
    ------
    graph : nx.Graph
        newman-girvan benchmark network
    """
    if z_in < 2:
        raise ValueError("z_in mustn't less than 2 in order to guarantee communities are connected!")
    # create communities
    community_size = int(n_vtx/n_community)
    communities = [range(i*community_size, (i+1)*community_size) for i in range(n_community-1)]
    communities.append(range((n_community-1)*community_size, n_vtx))

    # -----------create graph-----------
    graph = nx.Graph()
    # add edges within communities
    for c in communities:
        # initialize community
        # guarantee the community is connected
        c_1 = list(c)  # c_1 is a copy of c
        c_1.append(c_1.pop(0))
        circle_edges = [edge for edge in zip(c, c_1)]
        graph.add_edges_from(circle_edges)

        # start adding inner edges randomly
        c_current_degree = len(c) * 2
        c_total_degree = len(c) * z_in
        while c_current_degree < c_total_degree:
            edge = tuple(random.sample(c, 2))
            edge_reverse = (edge[1], edge[0])
            if edge not in graph.edges() and edge_reverse not in graph.edges():
                graph.add_edge(*edge)
                c_current_degree += 2
        # assign nodes' attributes
        for v in c:
            graph.node[v]['community'] = c

    # add edges between communities
    out_current_degree = 0
    out_total_degree = n_vtx * z_out
    while out_current_degree < out_total_degree:
        community_linked = random.sample(communities, 2)
        vtx0 = random.choice(community_linked[0])
        vtx1 = random.choice(community_linked[1])
        edge = (vtx0, vtx1)
        edge_reverse = (vtx1, vtx0)
        if edge not in graph.edges() and edge_reverse not in graph.edges():
            graph.add_edge(vtx0, vtx1)
            out_current_degree += 2

    return graph
