from itertools import cycle
import csv, os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation
import heapq

class output:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

    def print_grid (self) -> None:
        """
        print de huidig grid status met gates en verschillende lagen.
        """
        try:
            for z, layer in enumerate(self.grid_edit.grid):
                print(f"Laag {z}")
                for row in layer:
                    print(row)
        except IndexError:
            print("Fout bij het itereren door de grid. Controleer of de dimensies correct zijn.")
        except Exception as e:
            print(f"Onverwachte fout bij het printen van de grid: {e}")
        finally:
            print("Klaar met printen.")        

    def costen_berekening(self)->int:
        """berekent de score van de geplaatste draden"""
        score = self.grid_edit.wirecount + 300 * self.grid_edit.wirecrosscount
        return score
    
    def animation(self, frame, ax, grid_edit_obj):
        
        print(grid_edit_obj.gate_dict[2])
        print(grid_edit_obj.gate_nr)
        if not grid_edit_obj.gate_dict:
            print("geen gates in de dict")
            return
        

        # Zet gates opnieuw in de visualisatie
        if frame == 0:
            for gate_nr, (y, x, z) in grid_edit_obj.gate_dict.items():
                ax.scatter(x, y, z, color='blue', label=f'Gate' if gate_nr == 1 else "", s=100, marker = 'o')

        kleuren_palet = cycle([ 
            'red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black',
            'gray', 'orange', 'brown', 'pink', 'purple', 'teal', 'gold', 'lime',
            'indigo', 'maroon', 'navy', 'olive', 'coral', 'aqua', 'fuchsia',
            'salmon', 'tan', 'lavender', 'beige', 'khaki', 'ivory', 'azure',
            'turquoise', 'plum', 'orchid', 'violet'])

        # Teken de lijnen stap voor stap
        wires = grid_edit_obj.wirepaths_list
        if wires:
            total_frames = sum(len(wire) for wire in wires)
            current_frame = 0
            for wire in wires:
                wire_length = len(wire)
                kleur = next(kleuren_palet) 
                if frame < current_frame + wire_length:
                    wire_y, wire_x, wire_z = zip(*wire[:frame - current_frame + 1])
                    ax.plot(wire_x, wire_y, wire_z, color=kleur, linewidth=2, label='Wire Path' if frame == 0 else "")
                    break
                current_frame += wire_length
        else:
            print("Geen wires gevonden")

        # Instellen van ticks met stappen van 1
        maximum = max(grid_edit_obj.maximum_y, grid_edit_obj.maximum_x)
        ax.set_xticks(range(0, maximum + 4, 1))
        ax.set_yticks(range(0, maximum + 4, 1))
        ax.set_zlim(bottom=0)
        ax.set_zticks(range(1, 10, 1))


        # Labels and legend
        ax.set_xlabel("X-as")
        ax.set_ylabel("Y-as")
        ax.set_zlabel("Z-as")
        ax.set_title("3D Visualisatie van Gates en Wires")
        
    
        ax.legend()

        # Set the view
        ax.view_init(elev=37, azim=-138, roll=-11)

    def visualisatie(self):
        """
        Visualiseert de gates en wires in een 3D-omgeving.
        Gates worden weergegeven als blauwe punten en wires als rode lijnen.
        z = 0 is de bodem
        """
        # Setup - Gebruik het grid_edit object dat is doorgegeven aan de class
        grid_edit_obj = self.grid_edit
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        wires = grid_edit_obj.wirepaths_list
        animatie = self.animation

        
        total_frames = sum(len(wire) for wire in wires)
        # Maak de animatie
        _ = FuncAnimation(fig, animatie, frames = total_frames, fargs=(ax, grid_edit_obj), interval=500, repeat=False)

        # Toon de animatie
        plt.show()   