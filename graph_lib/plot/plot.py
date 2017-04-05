import matplotlib.pyplot as plt


def xy_plot(x, y, style='normal', title='', xlabel='', ylabel='', save_path=None, **kwargs):
    """
    package the plot steps
    :param x: sequence
    :param y: sequence
    :param style: string
        specify the plot style ('normal', 'loglog')
    :param title: string
    :param xlabel: string
    :param ylabel: string
    :param save_path: string
        the path used to save figure
    :param kwargs:
    :return:
    """
    plt.figure()
    if style == 'normal':
        plt.plot(x, y, **kwargs)
    elif style == 'loglog':
        plt.loglog(x, y, **kwargs)
    else:
        print 'The style {} is not supported at present!'.format(style)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    if save_path is not None:
        plt.savefig(save_path)
