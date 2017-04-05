# io functions for text files
import networkx as nx

def xy2text(fpath, x, y, xy_label=None):
    """
    save pairs from two sequences into text file
    :param fpath: string
        the path of the text file
    :param x: sequence
    :param y: sequence
    :param xy_label: objects able to be unpacked such as tuple and list
        title about the x, y sequences
    :return:
    """
    with open(fpath, 'wb') as f:
        if xy_label is not None:
            f.writelines('{}\t\t\t\t{}\n'.format(xy_label[0], xy_label[1]))
        all_text = ''
        for xy in zip(x, y):
            all_text += '{}\t\t\t\t{}\n'.format(xy[0], xy[1])
        f.write(all_text)


def read_edgelist(fpath):
    """
    create a graph object using edge list file
    :param fpath: string
        the path of the text file
    :return: networkx.Graph
    """
    # read the data
    with open(fpath) as f:
        data = f.readlines()
    # create the graph
    graph = nx.Graph()
    for raw_edge in data:
        edge = raw_edge.split()
        graph.add_edge(*edge)
    return graph
