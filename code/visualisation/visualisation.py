import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from code.classes.grid import grid_edit  # Zorg dat de juiste klasse wordt geïmporteerd

def visualisatie(grid_edit_instance):
    """
    Visualiseert het grid en de gates in een 3D-plot.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Visualiseer de gates
    for gate_nr, (y, x, z) in grid_edit_instance.gate_dict.items():
        ax.scatter(y, x, z, color='blue', label=f'Gate {gate_nr}')

    # Visualiseer de wires
    for z in range(len(grid_edit_instance.grid)):
        for y in range(len(grid_edit_instance.grid[z])):
            for x in range(len(grid_edit_instance.grid[z][y])):
                if grid_edit_instance.grid[z][y][x] == "+":
                    ax.scatter(x, y, z, color='red', label='Wire')

    # Stel assenlabels in
    ax.set_xlabel('X-as')
    ax.set_ylabel('Y-as')
    ax.set_zlabel('Z-as')

    plt.show()
