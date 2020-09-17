import numpy as np
import AGnr
import AGr
import main


class Statistics:
    instances_files = []
    best_values_fitness_with_rotations = []
    best_values_individuos_with_rotations = []
    best_values_fitness_no_rotations = []
    best_values_individuos_no_rotations = []

    def _get_instances(self):
        self.instances_files.clear()
        # Append Data
        prefix_dir = "data/"
        for file in main.get_files_in_data():
            self.instances_files.append(prefix_dir + file)
        return

    def __init__(self):
        self._get_instances()
        return

    def _median(self):
        return

    def _deviation(self):
        return

    def calculate_statistics(self, number_of_executions):

        for instance in self.instances_files:
            # Get parameters for algorithms
            max_width, widths, heights, individuo_size = main.load_data_from_file(instance)

            # Auxiliary lists to gather data of each instance executions
            data_fitness_rotation = []
            data_fitness_no_rotation = []
            data_individual_rotation = []
            data_individual_no_rotation = []

            for execution in range(number_of_executions):
                best_individual, best_individual_fitness = AGr.StripPackagingRotations(n=individuo_size, anchos=widths,
                                                                                       alturas=heights, gens=1000,
                                                                                       max_width=max_width,
                                                                                       seed=execution,
                                                                                       show_figure=False).run()
                # Gather data from algorithm with rotations
                data_fitness_rotation.append(best_individual_fitness)
                data_individual_rotation.append(best_individual)

                best_individual, best_individual_fitness = AGnr.StripPackagingNotRotations(n=individuo_size,
                                                                                           anchos=widths,
                                                                                           alturas=heights,
                                                                                           gens=1000,
                                                                                           max_width=max_width,
                                                                                           seed=execution,
                                                                                           show_figure=False).run()
                # Gather data from algorithm with rotations
                data_fitness_no_rotation.append(best_individual_fitness)
                data_individual_no_rotation.append(best_individual)

            # Collect all data

            # No Rotations
            self.best_values_fitness_no_rotations.append(data_fitness_no_rotation)
            self.best_values_individuos_no_rotations.append(data_individual_no_rotation)
            # With Rotation
            self.best_values_fitness_with_rotations.append(data_fitness_rotation)
            self.best_values_individuos_with_rotations.append(data_individual_rotation)

        return


Statistics().calculate_statistics(20)
