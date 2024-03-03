from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def change_unit(data: list[float], source_unit: str, target_unit: str) -> list[float]:
    scale_factors = {"V": 1, "mV": 1000}

    if source_unit == target_unit:
        return data
    else:
        source_scale = scale_factors[source_unit]
        target_scale = scale_factors[target_unit]
        return list(map(lambda x: x * target_scale / source_scale, data))


def force_unit(parsed_data: list[list], expected_unit: str) -> list[list]:
    """
    Forces the data to be in a specific unit
    :param parsed_data: the data to force
    :param expected_unit: the unit to force the data to
    :return: the data in the expected unit
    """
    for i, (source_unit, data) in enumerate(zip(parsed_data[0][1:], parsed_data[1][1:])):
        if source_unit == expected_unit or source_unit is None:
            pass
        else:
            scaled_data = change_unit(data, source_unit, expected_unit)
            parsed_data[1][i + 1] = scaled_data
            parsed_data[0][i + 1] = expected_unit

    return parsed_data


def draw_trace(parsed_data: list[list], title_text: str = None, is_digital: bool = False, save_path: str = None,
               max_y: float = None, min_y: float = 0, min_x: float = None, max_x: float = None,
               unit_to_force: str = None, comparator_line: float = None, t0=None,
               selected_traces=None) -> None:
    """
    Plots the full trace of 1 or 2 channels
    :param parsed_data: the data to plot (contains the units and one or two traces)
    :param title_text: the title of the graph
    :param is_digital: if the data is digital (5V or 0V)
    :param save_path: the path to save the graph
    :param max_y: the maximum value of the y-axis
    :param min_y: the minimum value of the y-axis
    :param min_x: the minimum value of the x-axis
    :param max_x: the maximum value of the x-axis
    :param unit_to_force: the unit the data should be displayed in
    :param comparator_line: pourcentage of max the comparator line (if any)
    :param t0: the time to start the graph from
    :param selected_traces: the traces to plot
    """

    if selected_traces is None:
        if parsed_data[0][2] is None:
            selected_traces = {1}
        else:
            selected_traces = {1, 2}

    if unit_to_force is not None:
        working_voltage_unit = unit_to_force
    elif (parsed_data[0][2] is None) or (parsed_data[0][1] == parsed_data[0][2]):
        working_voltage_unit = parsed_data[0][1]
    elif (parsed_data[0][1] == "V" and 1 in selected_traces) or (parsed_data[0][2] == "V" and 1 in selected_traces):
        working_voltage_unit = "V"
    else:
        working_voltage_unit = "mV"

    # change units if needed
    parsed_data = force_unit(parsed_data, working_voltage_unit)

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
    if 1 in selected_traces:
        plt.plot(parsed_data[1][0], parsed_data[1][1], linewidth=1)
    if parsed_data[1][2] == []:
        pass
    elif 2 in selected_traces:
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
        plt.title(title_text, fontsize=16)

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
            if 1 in selected_traces and 2 not in selected_traces:
                max_y = (1 + 0.05) * max(parsed_data[1][1])
                if (max_y <= 1 and working_voltage_unit == "V") or (max_y <= 1000 and working_voltage_unit == "mV"):
                    plt.ylim(min_y, max_y)
                else:
                    plt.ylim(0, 5.05)
            elif 2 in selected_traces and 1 not in selected_traces:
                max_y = (1 + 0.05) * max(parsed_data[1][2])
                if (max_y <= 1 and working_voltage_unit == "V") or (max_y <= 1000 and working_voltage_unit == "mV"):
                    plt.ylim(min_y, max_y)
                else:
                    plt.ylim(0, 5.05)
            else:
                max_y = (1 + 0.05) * max(max(parsed_data[1][1]), max(parsed_data[1][2]))
                if (max_y <= 1 and working_voltage_unit == "V") or (max_y <= 1000 and working_voltage_unit == "mV"):
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
