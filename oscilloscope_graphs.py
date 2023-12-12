from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter

def draw_trace(parsed_data: tuple, title_text: str = None, is_digital: bool = False, save_path: str = None,
               max_y: float = None, min_y: float = 0, min_x: float = None, max_x: float = None, force_unit: str = None,
               comparator_line: float = None, t0=None) -> None:
    """
    Plots the full trace of a single channel
    :param parsed_data: the data to plot
    :param title_text: the title of the graph
    :param is_digital: if the data is digital (5V or 0V)
    :param save_path: the path to save the graph
    :param max_y: the maximum value of the y axis
    :param min_y: the minimum value of the y axis
    :param min_x: the minimum value of the x axis
    :param max_x: the maximum value of the x axis
    :param force_unit: the unit the data should be displayed in
    :param comparator_line: pourcentage of max the comparator line (if any)
    """
    # change units if needed TODO : does not work right now
    if force_unit is not None:
        if force_unit == "V":
            if parsed_data[0][1] == "mV":
                parsed_data[1][1] = list(map(lambda x: x / 1000, parsed_data[1][1]))
                try:
                    parsed_data[1][2] = list(map(lambda x: x / 1000, parsed_data[1][2]))
                except IndexError:
                    pass
                parsed_data[0][1] = "V"
        elif force_unit == "mV":
            if parsed_data[0][1] == "V":
                parsed_data[1][1] = list(map(lambda x: x * 1000, parsed_data[1][1]))
                try:
                    parsed_data[1][2] = list(map(lambda x: x * 1000, parsed_data[1][2]))
                except IndexError:
                    pass
                parsed_data[0][1] = "mV"
        else:
            raise ValueError(f"Unknown unit : {force_unit}")

    # scale back time if needed
    if t0 is not None:
        if min_x is not None:
            min_x = min_x - t0
        if max_x is not None:
            max_x = max_x - t0
        parsed_data[1][0] = list(map(lambda x: x - t0, parsed_data[1][0]))


    # change the tick style and text size
    plt.tick_params(axis='both', which='major', labelsize=14, direction="in")
    # draw the grid
    plt.grid(True, which='major', axis='both', linestyle='--')

    # plot the data
    plt.plot(parsed_data[1][0], parsed_data[1][1], linewidth=1)
    if parsed_data[1][2] == []:
        pass
    else:
        plt.plot(parsed_data[1][0], parsed_data[1][2], linewidth=1)

    # draw the comparator line
    if comparator_line is not None:
        comparator_y = max(parsed_data[1][1]) * comparator_line
        plt.axhline(y=comparator_y, color='r', linestyle='--')
        # hard coded for convenience for now TODO : parametrize this
        ax = plt.gca()
        ax.set_yticks(list(ax.get_xticks()) + [2.5, 4.73])
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.1f'))

    # add axis labels
    plt.xlabel(f"temps ({parsed_data[0][0]})", fontsize=14)
    plt.ylabel(f"tension ({parsed_data[0][1]})", fontsize=14)

    # add a title
    if title_text is not None:
        plt.title(title_text)

    # setting the y-axis limits
    if is_digital:
        if comparator_line is None:
            ax = plt.gca()
            ax.set_yticks(list(ax.get_xticks()) + [0, 2.5, 5])
        plt.ylim(0, 5.15)
    else:
        if min_y is None:
            min_y = 0
        if max_y is not None:
            plt.ylim(min_y, max_y)
        else:
            max_y = max(parsed_data[1][1]) + 0.05 * max(parsed_data[1][1])
            if (max_y <= 1 and parsed_data[0][1] == "V") or (max_y <= 1000 and parsed_data[0][1] == "mV"):
                plt.ylim(min_y, max_y)
            else:
                plt.ylim(0, 5.05)

    # setting the x-axis limits
    if min_x is None:
        min_x = min(parsed_data[1][0])
    if max_x is None:
        max_x = max(parsed_data[1][0])
    plt.xlim(min_x, max_x)

    # saving of displaying the graph
    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight')
    else:
        plt.show(bbox_inches='tight')

    plt.close()
