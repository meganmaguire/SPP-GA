import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


class PlotterStrip:
    _color_list = list(mcolors.CSS4_COLORS.values())

    def __init__(self):
        np.random.seed(0)

    def plot_individual_with_rotation(self, individual):
        return

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
