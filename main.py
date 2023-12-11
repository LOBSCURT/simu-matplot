from pico_csv_parser import pico_read_csv
from oscilloscope_graphs import full_trace_1_channel
import os

INPUT_DIRECTORY = "input/"
OUTPUT_DIRECTORY = "output/"

if __name__ == "__main__":
    # fetch all the files in the input directory
    input_files = os.listdir(INPUT_DIRECTORY)
    for file in input_files:
        # read the file
        parsed_data = pico_read_csv(INPUT_DIRECTORY + file)
        # plot the data
        full_trace_1_channel(parsed_data, save_path=OUTPUT_DIRECTORY + file.replace(".csv", ".png"))
