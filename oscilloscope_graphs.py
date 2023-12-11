from matplotlib import pyplot as plt

def full_trace_1_channel(parsed_data, title_text:str = "", is_digital=False, max_y=None, min_y=0) -> None:
    plt.plot(parsed_data[1][0], parsed_data[1][1])

    plt.xlabel(f"temps ({parsed_data[0][0]})")
    plt.ylabel(f"tension ({parsed_data[0][1]})")

    plt.title(title_text)

    if is_digital:
        plt.ylim(0, 5)
    else:
        if max_y is not None:
            plt.ylim(min_y, max_y)
        else:
            plt.ylim(min_y, max(parsed_data[1][1]))

    plt.show()
