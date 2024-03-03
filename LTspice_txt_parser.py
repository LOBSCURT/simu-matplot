def LTspice_read_txt(raw_data: list[str]) -> list[list]:
    """
    Reads a txt LTspice raw file content and returns the units as a list [time, voltage]
    and the data as a list of lists [time, voltage1, [voltage2]]
    """
    units = ["s", "V", None]
    if len(raw_data[0].split("\t")) == 3:
        units[2] = "V"

    time = []
    voltage1 = []
    voltage2 = []
    for row in raw_data[1:]:
        row = row.strip("\n").split("\t")
        row = tuple(map(lambda x: float(x), row))
        time.append(row[0])
        voltage1.append(row[1])
        if len(row) >= 3:
            voltage2.append(row[2])

    return [units, [time, voltage1, voltage2]]
