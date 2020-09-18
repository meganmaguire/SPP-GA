import numpy as np
import AGnr
import AGr
import main
import Plotter
import time


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
        print("Running instances...")

        for instance in self.instances_files:
            # Get parameters for algorithms
            max_width, widths, heights, individuo_size = main.load_data_from_file(instance)

            # Auxiliary lists to gather data of each instance executions
            data_fitness_rotation = []
            data_fitness_no_rotation = []
            data_individual_rotation = []
            data_individual_no_rotation = []

            # Seed Value
            seed = 0
            for execution in range(number_of_executions):
                best_individual, best_individual_fitness = AGr.StripPackagingRotations(n=individuo_size, anchos=widths,
                                                                                       alturas=heights, gens=1000,
                                                                                       max_width=max_width,
                                                                                       seed=seed,
                                                                                       show_figure=False).run()
                # Gather data from algorithm with rotations
                data_fitness_rotation.append(best_individual_fitness)
                data_individual_rotation.append(best_individual.copy())

                best_individual, best_individual_fitness = AGnr.StripPackagingNotRotations(n=individuo_size,
                                                                                           anchos=widths,
                                                                                           alturas=heights,
                                                                                           gens=1000,
                                                                                           max_width=max_width,
                                                                                           seed=seed,
                                                                                           show_figure=False).run()
                # Gather data from algorithm with rotations
                data_fitness_no_rotation.append(best_individual_fitness)
                data_individual_no_rotation.append(best_individual.copy())

                # Change seed
                seed += 1

            # Collect all data

            # No Rotations
            self.best_values_fitness_no_rotations.append(data_fitness_no_rotation.copy())
            self.best_values_individuos_no_rotations.append(data_individual_no_rotation.copy())

            # With Rotation
            self.best_values_fitness_with_rotations.append(data_fitness_rotation.copy())
            self.best_values_individuos_with_rotations.append(data_individual_rotation.copy())

            print(f" ************* Instance - {instance} ************* \n")
            print("     *** Algorithm Results - No Rotations *** \n")
            best_fitness = np.min(data_fitness_no_rotation)
            best_individual = data_individual_no_rotation[
                data_fitness_no_rotation.index(np.min(data_fitness_no_rotation))
            ]
            print(f"        - Best Fitness : {best_fitness}")
            print(f"        - Best Individual: {best_individual}")
            print(f"        - Median: {np.median(data_fitness_no_rotation)}")
            print(f"        - Deviation: {np.std(data_fitness_no_rotation)}\n\n")
            Plotter.PlotterStrip().plot_individual_with_no_rotation(individual=best_individual, max_width=max_width,
                                                                    heights=heights, widths=widths,
                                                                    title=f"{instance} - No Rotations Algorithm - Best")

            print("     *** Algorithm Results - With Rotations *** \n")
            best_fitness = np.min(data_fitness_rotation)
            best_individual = data_individual_rotation[
                data_fitness_rotation.index(np.min(data_fitness_rotation))
            ]
            print(f"        - Best Fitness : {best_fitness}")
            print(f"        - Best Individual: {best_individual}")
            print(f"        - Median: {np.median(data_fitness_rotation)}")
            print(f"        - Deviation: {np.std(data_fitness_rotation)}\n\n")
            Plotter.PlotterStrip().plot_individual_with_rotation(individual=best_individual, max_width=max_width,
                                                                 heights=heights, widths=widths,
                                                                 title=f"{instance} - Rotations Algorithm - Best")
            print("---------------------------------------------------------")
            print("---------------------------------------------------------")
        return


# Time it
start_time = time.time()
Statistics().calculate_statistics(20)
print("--- %s seconds ---" % (time.time() - start_time))
