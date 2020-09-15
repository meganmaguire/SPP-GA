import os
import AGnr
import AGr

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
    files_in_data = get_files_in_data()
    built_options = ""
    # Build options with files_in_data
    for index in range(len(files_in_data)):
        built_options = built_options + f"{index + 1}){files_in_data[index]}\n"

    while (True):
        print("Elegir instancia del problema:\n")
        print(built_options)
        return files_in_data[
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


# Driver Function
def main():
    main_menu()
    menu_select_files()
    return


# Setting Driver Function
if __name__ == '__main__':
    main()
