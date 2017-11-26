import numpy as np
from numpy import polyfit
import matplotlib.pyplot as plt


def plot2d(x, y, style='normal',
           title='', xlabel='', ylabel='', save_path=None, grid=False, **kwargs):
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
    :param grid: bool
        If true, it displays grid line.
        If false, it doesn't display grid line.
    :param kwargs: keyword arguments for plt.plot
    """
    if style == 'normal':
        plt.plot(x, y, **kwargs)
    elif style == 'loglog':
        # loglog() supports all the keyword arguments of plot() and
        # matplotlib.axes.Axes.set_xscale() / matplotlib.axes.Axes.set_yscale().
        plt.loglog(x, y, **kwargs)
    else:
        print('The style {} is not supported at present!'.format(style))

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    if grid:
        plt.grid()
    if save_path is not None:
        plt.savefig(save_path)


def scatter2d(x, y, radius_min=3, radius_max=10, marker='o', color='b', alpha=0.5,
              title='', xlabel='', ylabel='', save_path=None, grid=False):
    """
    Plot a scatter diagram, and points's size in the diagram are weighted by their counts.
    Bigger the count is, bigger the point will be.
    :param x: sequence
    :param y: sequence
    :param radius_min: number
        the smallest point's radius
    :param radius_max: number
        the largest point's radius
    :param marker: string
        The shape that the points will be displayed as.
    :param color: color, sequence, or sequence of color, optional, default: ‘b’
        c can be a single color format string, or a sequence of color specifications of length N,
        or a sequence of N numbers to be mapped to colors using the cmap and norm specified via kwargs (see below).
        Note that c should not be a single numeric RGB or RGBA sequence because that is indistinguishable
        from an array of values to be colormapped. c can be a 2-D array in which the rows are RGB or RGBA,
        however, including the case of a single row to specify the same color for all points.
        quote from:
        https://matplotlib.org/devdocs/api/_as_gen/matplotlib.pyplot.scatter.html#matplotlib.pyplot.scatter
    :param alpha: float
    :param title: string
    :param xlabel: string
    :param ylabel: string
    :param save_path: string
        the path used to save figure
    :param grid: bool
        If true, it displays grid line.
        If false, it doesn't display grid line.
    :return:
    """
    if radius_max < radius_min:
        raise ValueError('Radius_max should be larger than radius_min!')

    points = list(zip(x, y))
    points_uniq = set(zip(x, y))
    x_uniq, y_uniq, points_count = [], [], []
    for point in points_uniq:
        x_uniq.append(point[0])
        y_uniq.append(point[1])
        points_count.append(points.count(point))
    max_count = max(points_count)
    radius_increment = radius_max - radius_min
    points_area = [np.pi*(count/max_count*radius_increment+radius_min)**2 for count in points_count]
    plt.scatter(x_uniq, y_uniq, s=points_area, marker=marker, alpha=alpha, c=color)

    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if grid:
        plt.grid()
    if save_path is not None:
        plt.savefig(save_path)


def polyfit2d(x, y, deg,
              title='', xlabel='', ylabel='', save_path=None, grid=False, **kwargs):
    """
    do polyfit for two sequence and plot the fit curve
    :param x: array_like, shape (M,)
        x-coordinates of the M sample points
    :param y: array_like, shape (M,)
        y-coordinates of the sample points.
    :param deg: int
        Degree of the fitting polynomial
    :param title: string
    :param xlabel: string
    :param ylabel: string
    :param save_path: string
        the path used to save figure
    :param grid: bool
        If true, it displays grid line.
        If false, it doesn't display grid line.
    :param kwargs: key words for plot2d
    """
    p = polyfit(x, y, deg)
    x_fit = np.unique(sorted(x))
    y_fit = p[deg]
    for idx in range(deg):
        y_fit += p[idx] * x_fit ** (deg - idx)
    plot2d(x_fit, y_fit, **kwargs,
           xlabel=xlabel, ylabel=ylabel, title=title, save_path=save_path, grid=grid)
