import oscilloscope_graphs
from oscilloscope_graphs import get_trace_max
from oscilloscope_graphs import get_trace_min

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