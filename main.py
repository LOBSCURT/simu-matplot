from pico_csv_parser import pico_read_csv
from oscilloscope_graphs import draw_trace
import os

INPUT_DIRECTORY = "input/"
OUTPUT_DIRECTORY = "output/"

if __name__ == "__main__":



    # fetch all the files in the input directory
    input_section = os.listdir(INPUT_DIRECTORY)
    for directory in input_section:
        directory = directory + "/"
        if not os.path.isdir(OUTPUT_DIRECTORY + directory):
            os.mkdir(OUTPUT_DIRECTORY + directory)

        input_setting_directory = os.listdir(INPUT_DIRECTORY + directory)
        for setting in input_setting_directory:
            setting_path = setting + "/"
            if not os.path.isdir(OUTPUT_DIRECTORY + directory + setting_path):
                os.mkdir(OUTPUT_DIRECTORY + directory + setting_path)

            input_files = os.listdir(INPUT_DIRECTORY + directory + setting_path)

            if setting == "NOT_DEFINED":

                for file in input_files:
                    current_locale = directory + setting_path
                    # read the file
                    parsed_data = pico_read_csv(INPUT_DIRECTORY + current_locale + file)
                    # plot the data
                    draw_trace(parsed_data, save_path=OUTPUT_DIRECTORY + current_locale + file.replace(".csv", ".png"))

            else:
                settings = setting.split("-")