from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def change_voltage_unit(data: list[float], source_unit: str, target_unit: str) -> list[float]:
    scale_factors = {"V": 1, "mV": 1000}

    if source_unit == target_unit:
        return data
    else:
        source_scale = scale_factors[source_unit]
        target_scale = scale_factors[target_unit]
        return list(map(lambda x: x * target_scale / source_scale, data))


def change_time_unit(data: list[float], source_unit: str, target_unit: str) -> list[float]:
    scale_factors = {"s": 1, "ms": 1000}

    if source_unit == target_unit:
        return data
    else:
        source_scale = scale_factors[source_unit]
        target_scale = scale_factors[target_unit]
        return list(map(lambda x: x * target_scale / source_scale, data))


def force_units(parsed_data: list[list], expected_voltage_unit: str, expected_time_unit: str) -> list[list]:
    """
    Forces the data to be in a specific unit
    :param parsed_data: the data to force
    :param expected_voltage_unit: the unit to force the data to
    :return: the data in the expected unit
    """
    # voltage
    for i, (source_unit, data) in enumerate(zip(parsed_data[0][1:], parsed_data[1][1:])):
        if source_unit == expected_voltage_unit or source_unit is None:
            pass
        else:
            scaled_data = change_voltage_unit(data, source_unit, expected_voltage_unit)
            parsed_data[1][i + 1] = scaled_data
            parsed_data[0][i + 1] = expected_voltage_unit

    # time
    if parsed_data[0][0] == expected_voltage_unit:
        pass
    else:
        scaled_data = change_time_unit(parsed_data[1][0], parsed_data[0][0], expected_time_unit)
        parsed_data[1][0] = scaled_data
        parsed_data[0][0] = expected_time_unit

    return parsed_data


def get_trace_max(parsed_data: list[list], selected_traces: set[int]) -> float:
    """
    Returns the maximum value of the selected traces
    :param parsed_data: the data to get the maximum value from
    :param selected_traces: the traces to get the maximum value from
    :return: the maximum value of the selected traces
    """
    max_y = 0
    for i in selected_traces:
        max_y = max(max(parsed_data[1][i]), max_y)
    return max_y


def get_trace_min(parsed_data: list[list], selected_traces: set[int]) -> float:
    """
    Returns the minimum value of the selected traces
    :param parsed_data: the data to get the minimum value from
    :param selected_traces: the traces to get the minimum value from
    :return: the minimum value of the selected traces
    """
    min_y = 1e300
    for i in selected_traces:
        min_y = min(min(parsed_data[1][i]), min_y)
    return min_y


def change_ground(parsed_data: list[list], ground: float) -> list[list]:
    """
    Changes the ground of the data
    :param parsed_data: the data to change the ground of
    :param ground: the ground to change to (in V)
    :return: the data with the new ground
    """
    if parsed_data[0][1] == "V":
        parsed_data[1][1] = list(map(lambda x: float(round(x + ground, 5)), parsed_data[1][1]))
        if parsed_data[0][2] == "V":
            parsed_data[1][2] = list(map(lambda x: float(round(x + ground, 5)), parsed_data[1][2]))
    elif parsed_data[0][1] == "mV":
        parsed_data[1][1] = list(map(lambda x: float(round(x + ground * 1000, 5)), parsed_data[1][1]))
        if parsed_data[0][2] == "mV":
            parsed_data[1][2] = list(map(lambda x: float(round(x + ground * 1000, 5)), parsed_data[1][2]))
    return parsed_data


def draw_trace(parsed_data: list[list], title_text: str = None, is_digital: bool = False, save_path: str = None,
               max_y: float = None, min_y: float = 0, min_x: float = None, max_x: float = None,
               voltage_unit_to_force: str = None, comparator_line: float = None, t0=None, selected_traces=None,
               show_0=True, centered_2_5_V=False, time_unit_to_force="ms", ground=0, invert_colors=False,
               doted: dict = None, legende: list = None) -> None:
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
    :param voltage_unit_to_force: the unit the data should be displayed in
    :param time_unit_to_force: the unit the time should be displayed in
    :param comparator_line: pourcentage of max the comparator line (if any)
    :param t0: the time to start the graph from
    :param selected_traces: the traces to plot
    :param show_0: if the plot should show 0
    :param centered_2_5_V: if the plot should be centered around 2.5V
    :param ground: ground at something else than 0V (in V)
    """

    if selected_traces is None:
        if parsed_data[0][2] is None:
            selected_traces = {1}
        else:
            selected_traces = {1, 2}

    if voltage_unit_to_force is not None:
        working_voltage_unit = voltage_unit_to_force
    elif (parsed_data[0][2] is None) or (parsed_data[0][1] == parsed_data[0][2]):
        working_voltage_unit = parsed_data[0][1]
    elif (parsed_data[0][1] == "V" and 1 in selected_traces) or (parsed_data[0][2] == "V" and 1 in selected_traces):
        working_voltage_unit = "V"
    else:
        working_voltage_unit = "mV"

    # change units if needed
    parsed_data = force_units(parsed_data, working_voltage_unit, time_unit_to_force)

    # change the ground if needed
    if ground != 0:
        parsed_data = change_ground(parsed_data, ground)

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

    if invert_colors:
        color2 = "C0"
        color1 = "C1"
    else:
        color1 = "C0"
        color2 = "C1"

    line_style1 = line_style2 = "-"
    linewidth1 = linewidth2 = 1
    if doted is not None:
        if 1 in doted:
            line_style1 = "--"
            linewidth1 = 1.5
        if 2 in doted:
            line_style2 = "--"
            linewidth2 = 1.5

    # plot the data
    if 1 in selected_traces:
        if legende is None:
            plt.plot(parsed_data[1][0], parsed_data[1][1], linewidth=linewidth1, color=color1, linestyle=line_style1)
        else:
            plt.plot(parsed_data[1][0], parsed_data[1][1], linewidth=linewidth1, color=color1, linestyle=line_style1, label=legende[0])
    if parsed_data[1][2] == []:
        pass
    elif 2 in selected_traces:
        if legende is None:
            plt.plot(parsed_data[1][0], parsed_data[1][2], linewidth=linewidth2, color=color2, linestyle=line_style2)
        else:
            plt.plot(parsed_data[1][0], parsed_data[1][2], linewidth=linewidth2, color=color2, linestyle=line_style2, label=legende[1])
    if legende is not None:
        plt.legend(loc='upper right')

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
        min_y = 0
        max_y = 5.15
    else:
        if min_y is None:
            if show_0:
                min_y = 0
            else:
                min_y = (1 - 0.05) * get_trace_min(parsed_data, selected_traces)

        if max_y is None:
            max_y = (1 + 0.05) * get_trace_max(parsed_data, selected_traces)
    # change the tiks if the data is centered around 2.5 V
    if centered_2_5_V:
        ax = plt.gca()
        ax.set_yticks(list(ax.get_xticks()) + [get_trace_min(parsed_data, selected_traces), 2.5,
                                               get_trace_max(parsed_data, selected_traces)])
    plt.ylim(min_y, max_y)

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
