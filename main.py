from pico_csv_parser import pico_read_csv
from oscilloscope_graphs import full_trace_1_channel


if __name__ == "__main__":
    parsed_data = pico_read_csv("exemples/20231211-0001_10.csv")

    full_trace_1_channel(parsed_data, "Exemple de trace complète")