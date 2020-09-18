# Strip Packing Problem - Genetic Algorithm

Solving the [Strip Packing Problem](https://en.wikipedia.org/wiki/Strip_packing_problem) with a genetic algorithm.

To be able to run this project, make sure to have installed [Anaconda 3] (https://www.anaconda.com/) or have installed numpy~=1.18.5 and matplotlib~=3.2.2 
in Python 3 enviroment.

## Instructions

- main.py - Runs any instance that are stored in data/ folder, with or without rotations. User can choose which algorithm will run the instance selected.
- Statistics.py - Runs 20 executions for each instance in data/ folder with both algorithms, and finally will give the figures with the best solution for each instance. 

### Project Structure
  - AGnr.py - Solution with no rotations
  - AGr.py - Solution with rotations
  - Plotter.py - Wrapper to use some of the matplotlib functions to draw the individuals.
  - Statistics.py - Code to gather results and give a report of them.
  
