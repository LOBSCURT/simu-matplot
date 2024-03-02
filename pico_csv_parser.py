
def pico_read_csv(raw_data: list[str]) -> tuple[tuple, list[list]]:
    """
    Reads a CSV picoscope file and returns the units as a tuple (time, voltage)
    and the data as a list of lists (time, voltage1, [voltage2])
    """
    (time_unit, voltage_unit) = raw_data[1].split(";")[0:2]

    if len(raw_data[1].split(";")) >= 3:
        if raw_data[1].split(";")[1].strip("()\n") != raw_data[1].split(";")[2].strip("()\n"):
            raise ValueError("The two channels do not have the same units")

    time_unit = time_unit.strip("()\n")
    voltage_unit = voltage_unit.strip("()\n")

    time = []
    voltage1 = []
    voltage2 = []
    for row in raw_data[3:-1]:
        row = row.strip("\n").split(";")
        row = tuple(map(lambda x: x.replace(",", "."), row))
        row = tuple(map(lambda x: float(x), row))
        time.append(row[0])
        voltage1.append(row[1])
        if len(row) >= 3:
            voltage2.append(row[2])
    return (time_unit, voltage_unit), [time, voltage1, voltage2]
