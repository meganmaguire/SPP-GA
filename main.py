import os
import AGr
import AGnr


def get_int_input(text, min_value, max_value):
    value = 0
    while True:
        try:
            value = int(input(text))
        except ValueError:
            print("Invalid Value")
            continue

        if value < min_value or value > max_value:
            print(f"Value must be between{min_value} and {max_value}")
            continue
        else:
            break
    return value


def get_files_in_data():
    files_in_data = os.popen('ls data').read().split("\n")
    # Clean empty lines
    files_in_data.remove("")

    return files_in_data


def menu_select_files():
    prefix_dir = "data/"
    files_in_data = get_files_in_data()
    built_options = ""
    # Build options with files_in_data
    for index in range(len(files_in_data)):
        built_options = built_options + f"{index + 1}){files_in_data[index]}\n"

    while (True):
        print("Elegir instancia del problema:\n")
        print(built_options)
        return prefix_dir + files_in_data[
            get_int_input("Ingrese instancia de problema: ", 1, len(files_in_data)) - 1
            ]


def main_menu():
    print("--------------------------------------------------")
    print("--- Strip Packaging Problem - Genetic Algorithm---")
    print("--------------------------------------------------\n")
    while True:
        print("""Select Solution
        1) Solution using rectangles with rotations
        2) Solution without rotations
        """)
        return get_int_input("Option Selected: ", 1, 2)


def load_data_from_file(filename):
    file_opened = open(filename, "r")
    data = file_opened.read().split("\n")
    max_width = int(data.pop(0))
    widths = []
    heights = []
    for index in range(len(data)):
        current_rectangle = data[index].split(" ")
        widths.append(int(current_rectangle[0]))
        heights.append(int(current_rectangle[1]))

    # Control for data
    if len(widths) != len(heights):
        print("WIDTHS AND HEIGHTS != SIZES")
        return 0, [], [], 0

    n = len(widths)
    return max_width, widths, heights, n


# Driver Function
def main():
    algorithm_selected = main_menu()
    instance_selected = menu_select_files()
    max_width, widths, heights, individuo_size = load_data_from_file(instance_selected)
    # 1 - With Rotations -- 2 - No Rotations
    if algorithm_selected == 1:
        print("Running with rotations...")
        AGr.StripPackagingRotations(n=individuo_size, anchos=widths, alturas=heights, gens=5000, max_width=max_width)
    else:
        print("Running with no rotations...")
        AGnr.StripPackagingNotRotations(n=individuo_size, anchos=widths, alturas=heights, gens=5000,
                                        max_width=max_width)
    return


# Setting Driver Function
if __name__ == '__main__':
    main()
