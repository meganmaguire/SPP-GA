import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


class PlotterStrip:
    # _color_list = list(mcolors.CSS4_COLORS.values())
    _color_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    def __init__(self):
        np.random.seed(0)

    def plot_individual_with_rotation(self, individual, heights, widths, max_width):
        # Plot Variables
        plt.axes()
        ancho_anterior = 0
        # Index rectangle variables
        i = 0
        ancho_acum = 0
        altura_max = 0
        altura_total = 0
        ancho_actual = 0

        for rectangulo in individual[0]:
            rectangulo = int(rectangulo)

            # Update Plot position
            ancho_anterior += ancho_actual

            # Chequeo la orientación del rectángulo
            if individual[1][i] == 0:
                ancho_actual = widths[rectangulo]
                altura_actual = heights[rectangulo]
            else:
                ancho_actual = heights[rectangulo]
                altura_actual = widths[rectangulo]

            if ancho_actual + ancho_acum <= max_width:
                ancho_acum += ancho_actual
                if altura_actual > altura_max:
                    altura_max = altura_actual
            else:
                altura_total += altura_max
                ancho_acum = ancho_actual
                altura_max = altura_actual

                # Update Plot position
                ancho_anterior = 0
            i += 1

            # Draw rectangle
            plt.axis('scaled')
            rectangle_to_draw = plt.Rectangle((ancho_anterior, altura_total), ancho_actual, altura_actual,
                                              fc=self._random_color(), ec='k')
            plt.gca().add_patch(rectangle_to_draw)

        plt.show()

        altura_total += altura_max
        return altura_total

    def plot_individual_with_no_rotation(self, individual, heights, widths, max_width):
        # Plot variables
        plt.axes()

        ancho_anterior = 0
        ancho_actual = 0
        altura_actual = 0

        # Variables to index rectangles
        ancho_acum = 0
        altura_max = 0
        altura_total = 0

        for rectangle in individual:
            rectangle = int(rectangle)

            # Update Plot position
            ancho_anterior += ancho_actual
            ancho_actual = widths[rectangle]

            # Update heights and widths
            if widths[rectangle] + ancho_acum <= max_width:
                ancho_acum += widths[rectangle]
                if heights[rectangle] > altura_max:
                    altura_max = heights[rectangle]
            else:
                altura_total += altura_max
                ancho_acum = widths[rectangle]
                altura_max = heights[rectangle]

                # Update Plot position
                altura_actual = altura_total
                ancho_anterior = 0

            # Draw rectangle
            plt.axis('scaled')
            rectangle = plt.Rectangle((ancho_anterior, altura_actual), widths[rectangle], heights[rectangle],
                                      fc=self._random_color(), ec='k')
            plt.gca().add_patch(rectangle)

        plt.show()

        return

    # Returns a random color from _color_list
    def _random_color(self):
        fill_color_index = np.random.randint(0, len(self._color_list))
        return self._color_list[fill_color_index]
