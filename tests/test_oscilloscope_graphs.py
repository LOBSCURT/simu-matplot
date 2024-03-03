import oscilloscope_graphs

def test_change_unit():
    data_V = [1, 2000, 3000]
    data_mV = [1000, 2000000, 3000000]

    assert oscilloscope_graphs.change_unit(data_V, "V", "mV") == data_mV

    assert oscilloscope_graphs.change_unit(data_mV, "mV", "V") == data_V