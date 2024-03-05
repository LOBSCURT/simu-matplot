from LTspice_txt_parser import LTspice_read_txt
from pico_csv_parser import pico_read_csv
from oscilloscope_graphs import draw_trace
import os
import shutil

INPUT_DIRECTORY = "input/"
OUTPUT_DIRECTORY = "output/"


def process_data_file(file_path: str) -> list[list]:
    if file_path[-3:] == "csv":
        with open(file_path, "r") as f:
            parsed_data = pico_read_csv(f.readlines())
    elif file_path[-3:] == "txt":
        with open(file_path, "r") as f:
            parsed_data = LTspice_read_txt(f.readlines())

    # TODO : handle somewhere the unifications of units

    return parsed_data


def change_filename_extension(filename: str) -> str:
    """
    Change the extension of a file from csv or txt to png
    :param filename: the filename to change
    :return: the filename with the new extension
    """
    return filename.replace(".csv", ".png").replace(".txt", ".png")


def process_all_csv():
    # check if the output directory exists if so clear it if not create it
    if os.path.isdir(OUTPUT_DIRECTORY):
        shutil.rmtree(OUTPUT_DIRECTORY)
        os.mkdir(OUTPUT_DIRECTORY)
    else:
        os.mkdir(OUTPUT_DIRECTORY)

    # fetch all the files in the input directory
    input_section = os.listdir(INPUT_DIRECTORY)
    for directory in input_section:
        directory = directory + "/"
        if not os.path.isdir(OUTPUT_DIRECTORY + directory):
            os.mkdir(OUTPUT_DIRECTORY + directory)

        input_setting_directory = os.listdir(INPUT_DIRECTORY + directory)
        for setting_folder in input_setting_directory:
            setting_path = setting_folder + "/"
            if not os.path.isdir(OUTPUT_DIRECTORY + directory + setting_path):
                os.mkdir(OUTPUT_DIRECTORY + directory + setting_path)

            input_files = os.listdir(INPUT_DIRECTORY + directory + setting_path)

            if setting_folder == "NOT_DEFINED":

                for file in input_files:
                    current_locale = directory + setting_path
                    # read the file
                    parsed_data = process_data_file(INPUT_DIRECTORY + current_locale + file)
                    # plot the data
                    draw_trace(parsed_data,
                               save_path=OUTPUT_DIRECTORY + current_locale + change_filename_extension(file))
            else:
                # format: title_title-text;x_min_x_max_x;y_min_y_max_y;unit_V;digital;comparator_pourcent
                # format continued: t0_start-time;selectTrace_1_2;show0_False;centered25V_True;ground_2,5
                settings = setting_folder.split(";")
                y_lim = [None, None]
                x_lim = [None, None]
                title = ""
                force_unit = None
                digital = False
                comparator_pourcent = None
                t0 = None
                selected_traces = None
                show_0 = True
                centered_2_5_V = False
                ground = 0 # to indicate when the mesure was taken with a ground at something else than 0V (in V)

                for setting in settings:
                    setting_data = setting.split("_")
                    if setting_data[0] == "title":
                        title = setting_data[1]
                    elif setting_data[0] == "x":
                        x_lim = setting_data[1:]
                        x_lim = list(map(lambda x: float(x.replace(",", ".")), x_lim))
                    elif setting_data[0] == "y":
                        y_lim = setting_data[1:]
                        y_lim = list(map(lambda x: float(x.replace(",", ".")), y_lim))
                    elif setting_data[0] == "unit":
                        force_unit = setting_data[1]
                    elif setting_data[0] == "digital":
                        digital = True
                    elif setting_data[0] == "comparator":
                        comparator_pourcent = float(setting_data[1].replace(",", "."))
                    elif setting_data[0] == "t0":
                        t0 = float(setting_data[1].replace(",", "."))
                    elif setting_data[0] == "selectTrace":
                        selected_traces = set()
                        selected_traces.add(int(setting_data[1]))
                        if len(setting_data) == 3:
                            selected_traces.add(int(setting_data[2]))
                    elif setting_data[0] == "show0":
                        show_0 = setting_data[1] == "True"
                    elif setting_data[0] == "centered25V":
                        centered_2_5_V = setting_data[1] == "True"
                    elif setting_data[0] == "ground":
                        ground = float(setting_data[1].replace(",", "."))
                    else:
                        raise ValueError(
                            f"Unknown setting : {setting_data[0]}  in folder {setting_folder} from {directory}")

                for file in input_files:
                    current_locale = directory + setting_path
                    # read the file
                    parsed_data = process_data_file(INPUT_DIRECTORY + current_locale + file)
                    # plot the data
                    draw_trace(parsed_data, title_text=title, is_digital=digital,
                               save_path=OUTPUT_DIRECTORY + current_locale + change_filename_extension(file),
                               max_y=y_lim[1], min_y=y_lim[0], min_x=x_lim[0], max_x=x_lim[1],
                               voltage_unit_to_force=force_unit, comparator_line=comparator_pourcent, t0=t0,
                               selected_traces=selected_traces, show_0=show_0, centered_2_5_V=centered_2_5_V,
                               ground=ground)


if __name__ == "__main__":
    process_all_csv()
