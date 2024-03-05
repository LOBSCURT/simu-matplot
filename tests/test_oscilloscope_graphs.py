import oscilloscope_graphs
from oscilloscope_graphs import get_trace_max
from oscilloscope_graphs import get_trace_min
from oscilloscope_graphs import change_ground


def test_change_unit():
    data_V = [1, 2000, 3000]
    data_mV = [1000, 2000000, 3000000]

    assert oscilloscope_graphs.change_voltage_unit(data_V, "V", "mV") == data_mV

    assert oscilloscope_graphs.change_voltage_unit(data_mV, "mV", "V") == data_V


def test_get_trace_max_2_channel():
    parsed_data = [
        ["s", "V", "V"],
        [
            [3333, 3334, 3335],
            [0.0, 2.072000000511463e-09, 6.316353223183249e-08],
            [2.5, 2.5, 2.499983]
        ]
    ]
    selected_traces = {1, 2}
    assert get_trace_max(parsed_data, selected_traces) == 2.5
    assert get_trace_max(parsed_data, {1}) == 6.316353223183249e-08


def test_get_trace_max_1_channel():
    parsed_data = [
        ["s", "V", None],
        [
            [3333, 3334, 3335],
            [0.0, 2.072000000511463e-09, 6.316353223183249e-08],
            []
        ]
    ]
    selected_traces = {1}
    assert get_trace_max(parsed_data, selected_traces) == 6.316353223183249e-08


def test_get_trace_min_2_channel():
    parsed_data = [
        ["s", "V", "V"],
        [
            [3333, 3334, 3335],
            [0.0, 2.072000000511463e-09, 6.316353223183249e-08],
            [2.5, 2.5, 2.499983]
        ]
    ]
    selected_traces = {1, 2}
    assert get_trace_min(parsed_data, selected_traces) == 0.0
    assert get_trace_min(parsed_data, {2}) == 2.499983


def test_get_trace_min_1_channel():
    parsed_data = [
        ["s", "V", None],
        [
            [3333, 3334, 3335],
            [2, 2.072000000511463e-09, 6.316353223183249e-08],
            []
        ]
    ]
    selected_traces = {1}
    assert get_trace_min(parsed_data, selected_traces) == 2.072000000511463e-09


def test_change_ground_2_channel_V():
    parsed_data = [
        ["s", "V", "V"],
        [
            [3333, 3334, 3335],
            [0.0, 1, 3],
            [2.5, 2.5, 2.4]
        ]
    ]
    expected_output = [
        ["s", "V", "V"],
        [
            [3333, 3334, 3335],
            [-2.5, -1.5, 0.5],
            [0.0, 0.0, -0.1]
        ]
    ]
    assert change_ground(parsed_data, 2.5) == expected_output


def test_change_ground_2_channel_mV():
    parsed_data = [
        ["s", "mV", "mV"],
        [
            [3333, 3334, 3335],
            [0.0, 1000, 3000],
            [2500, 2500, 2400]
        ]
    ]
    expected_output = [
        ["s", "mV", "mV"],
        [
            [3333, 3334, 3335],
            [-2500.0, -1500.0, 500.0],
            [0.0, 0.0, -100.0]

        ]
    ]
    assert change_ground(parsed_data, 2.5) == expected_output


def test_change_ground_1_channel_V():
    parsed_data = [
        ["s", "V", None],
        [
            [3333, 3334, 3335],
            [0.0, 1, 3],
            []
        ]
    ]
    expected_output = [
        ["s", "V", None],
        [
            [3333, 3334, 3335],
            [-2.5, -1.5, 0.5],
            []
        ]
    ]
    assert change_ground(parsed_data, 2.5) == expected_output


def test_change_ground_1_channel_mV():
    parsed_data = [
        ["s", "mV", None],
        [
            [3333, 3334, 3335],
            [0.0, 1000, 3000],
            []
        ]
    ]
    expected_output = [
        ["s", "mV", None],
        [
            [3333, 3334, 3335],
            [-2500.0, -1500.0, 500.0],
            []
        ]
    ]
    assert change_ground(parsed_data, 2.5) == expected_output
