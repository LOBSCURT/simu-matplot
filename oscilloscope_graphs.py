from matplotlib import pyplot as plt


def draw_trace(parsed_data, title_text: str = None, is_digital=False, save_path=None, max_y=None,
               min_y=0, min_x=None, max_x=None, force_unit=None) -> None:
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


    plt.tick_params(axis='both', which='major', labelsize=14, direction="in")
    plt.grid(True, which='major', axis='both', linestyle='--')

    plt.plot(parsed_data[1][0], parsed_data[1][1], linewidth=1)
    if parsed_data[1][2] == []:
        pass
    else:
        plt.plot(parsed_data[1][0], parsed_data[1][2], linewidth=1)

    plt.xlabel(f"temps ({parsed_data[0][0]})", fontsize=14)
    plt.ylabel(f"tension ({parsed_data[0][1]})", fontsize=14)

    if title_text is not None:
        plt.title(title_text)

    # setting the y-axis limits
    if is_digital:
        plt.ylim(0, 5.05)
    else:
        if min_y is None:
            min_y = 0
        if max_y is not None:
            plt.ylim(min_y, max_y)
        else:
            max_y = max(parsed_data[1][1]) + 0.05 * max(parsed_data[1][1])
            if (max_y <= 1 and parsed_data[0][1]=="V") or (max_y <= 1000 and parsed_data[0][1]=="mV"):
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
        plt.savefig(save_path, bbox_inches = 'tight' )
    else:
        plt.show(bbox_inches = 'tight' )

    plt.close()
