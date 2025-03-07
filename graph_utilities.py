import numpy as np
from matplotlib import pyplot as plt, cm as cm


def plot_bar_graph(data, x_axis, y_axis, x_label, y_label, title, visible_x=True, ymin=None, ymax=None):
    """Function to plot a bar graph

    :param data: Data to plot (DataFrame)
    :param x_axis: Column name for the x_axis (str)
    :param y_axis: Column name for the y_axis (str)
    :param x_label: Label for the x_axis (str)
    :param y_label: Label for the y_axis (str)
    :param title: Title of the plot (str)
    :param visible_x: Whether to display the x_axis label (bool, default True)
    :param ymin: If included, the minimum value for the y-axis (float, default None)
    :param ymax: If included, the maximum value for the y-axis (float, default None)
    :return: None, directly displays with matplotlib
    """
    plt.figure(figsize=(10, 6))

    # Generate colors based on the number of bars
    colors = cm.viridis(np.linspace(0, 1, len(data[x_axis])))

    plt.bar(data[x_axis], data[y_axis], color = colors)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.xticks(rotation=90)
    # Set font size to 10
    plt.xticks(fontsize=10)

    # Set y-axis limits if necessary
    if ymin is not None and ymax is not None:
        plt.ylim(ymin, ymax)


    # Hide x-axis labels if necessary
    if not visible_x:
        plt.xticks(ticks=range(len(data[x_axis])), labels=['']*len(data[x_axis]))

    plt.tight_layout()
    plt.show()


def plot_box_graph(data, x_axis, y_axis, x_label, y_label, title, visible_x=True):
    """Function to plot a box plot

    :param data: Data to plot (DataFrame)
    :param x_axis: Column name for the x_axis (str)
    :param y_axis: Column name for the y_axis (str)
    :param x_label: Label for the x_axis (str)
    :param y_label: Label for the y_axis (str)
    :param title: Title of the plot (str)
    :return: None, directly displays with matplotlib
    """
    plt.figure(figsize=(10, 6))

    plt.boxplot(data[y_axis])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # Hide x-axis labels if necessary
    if not visible_x:
        plt.xticks(ticks=range(len(data[x_axis])), labels=['']*len(data[x_axis]))
    plt.tight_layout()
    plt.show()


def plot_line_graph(data, x_axis, y_axis, x_label, y_label, title, ymin=None, ymax=None):
    """Function to plot a line graph

    :param data: Data to plot (DataFrame)
    :param x_axis: Column name for the x_axis (str)
    :param y_axis: Column name for the y_axis (str)
    :param x_label: Label for the x_axis (str)
    :param y_label: Label for the y_axis (str)
    :param title: Title of the plot (str)
    :param ymin: If included, the minimum value for the y-axis (float, default None)
    :param ymax: If included, the maximum value for the y-axis (float, default None)
    :return: None, directly displays with matplotlib
    """
    plt.figure(figsize=(10, 6))

    plt.plot(data[x_axis], data[y_axis])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # Set y-axis limits if necessary
    if ymin is not None and ymax is not None:
        plt.ylim(ymin, ymax)

    plt.tight_layout()
    plt.show()
