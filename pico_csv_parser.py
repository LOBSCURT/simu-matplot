def pico_read_csv(raw_data: list[str]) -> list[list]:
    """
    Reads a CSV picoscope file and returns the units as a list [time, voltage1, [voltage2]]
    and the data as a list of lists [time, voltage1, [voltage2]]
    """
    (time_unit, voltage_unit1) = raw_data[1].split(";")[0:2]
    time_unit = time_unit.strip("()\n")
    voltage_unit1 = voltage_unit1.strip("()\n")
    voltage_unit2 = None

    if len(raw_data[1].split(";")) >= 3:
        voltage_unit2 = raw_data[1].split(";")[2]
        voltage_unit2 = voltage_unit2.strip("()\n")

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

    return [[time_unit, voltage_unit1, voltage_unit2], [time, voltage1, voltage2]]
