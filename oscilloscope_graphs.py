from matplotlib import pyplot as plt


def full_trace_1_channel(parsed_data, title_text: str = None, is_digital=False, save_path=None, max_y=None,
                         min_y=0, min_x=None, max_x=None) -> None:
    """
    Plots the full trace of a single channel
    :param parsed_data:
    :param title_text:
    :param is_digital:
    :param save_path:
    :param max_y:
    :param min_y:
    :return:
    """
    plt.plot(parsed_data[1][0], parsed_data[1][1])

    plt.xlabel(f"temps ({parsed_data[0][0]})")
    plt.ylabel(f"tension ({parsed_data[0][1]})")

    if title_text is not None:
        plt.title(title_text)

    # setting the y axis limits
    if is_digital:
        plt.ylim(0, 5)
    else:
        if max_y is not None:
            plt.ylim(min_y, max_y)
        else:
            max_y = max(parsed_data[1][1])
            if (max_y <= 1 and parsed_data[0][1]=="V") or (max_y <= 1000 and parsed_data[0][1]=="mV"):
                plt.ylim(min_y, max_y)
            else:
                plt.ylim(0, 5)

    # setting the x-axis limits
    if min_x is None:
        min_x = min(parsed_data[1][0])
    if max_x is None:
        max_x = max(parsed_data[1][0])
    plt.xlim(min_x, max_x)

    # saving of displaying the graph
    if save_path is not None:
        plt.savefig(save_path)
    else:
        plt.show()
