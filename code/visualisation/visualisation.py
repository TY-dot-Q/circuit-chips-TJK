from itertools import cycle
import csv, os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D

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
            print("Klaar met printen.\n\n")        

    def costen_berekening(self, wirecount)->int: 
        """berekent de score van de geplaatste draden"""
        self.grid_edit.score = wirecount + (300 * self.grid_edit.wirecrosscount)
    
    def animation(self, frame, ax, grid_edit_obj):
        """
        Functie die wordt aangeroepen voor elke frame van de animatie.
        """
        # Check of er gates zijn
        if not grid_edit_obj.gate_dict:
            print(" - geen gates in de dict")
            return
        

        # Zet gates opnieuw in de visualisatie
        if frame == 0:
            for _, (y, x, z) in grid_edit_obj.gate_dict.items():
                ax.scatter(x, y, z, color='blue', s=100, marker = 'o')

        kleuren_palet = cycle([ 
        'black', 'blue', 'green', 'orange', 'purple', 'teal', 'gold',
        'pink', 'coral', 'olive', 'indigo', 'yellow'])

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
                    ax.plot(wire_x, wire_y, wire_z, color=kleur, linewidth = 2)
                    break
                current_frame += wire_length
        else:
            print("   geen wires gevonden")

        
        # print wirecrosses in visual
        if frame == total_frames - 1: 
            wirecross = grid_edit_obj.wirecross_list 
            if wirecross:
                for y, x, z in wirecross:
                    ax.scatter(x, y, z, color='black', s=250, marker='x')
            else:
                print("   geen kruisingen gevonden.")


        # print overlaps in visual
        if frame == total_frames - 1: 
            overlap = grid_edit_obj.overlapping_lijst
            if isinstance(overlap, list):
                if all(isinstance(sublist, list) and all(isinstance(coord, tuple) and len(coord) == 3 for coord in sublist) for sublist in overlap):
                    if overlap:
                        for segment in overlap:
                            if len(segment) == 2: 
                                overlap_y, overlap_x, overlap_z = zip(*segment)
                                ax.plot(overlap_x, overlap_y, overlap_z, color='red', linewidth=3)
                    else:
                        print("   geen overlappingen gevonden.")
            
        # set axes for grid
        maximum = max(grid_edit_obj.maximum_y, grid_edit_obj.maximum_x)
        ax.set_xticks(range(0, self.grid_edit.maximum_x + 1, 1))
        ax.set_yticks(range(0, self.grid_edit.maximum_y + 1, 1))
        ax.set_zlim(bottom=0)
        ax.set_zticks(range(1, 10, 1))


        # title axes and legend
        ax.set_xlabel("X-as")
        ax.set_ylabel("Y-as")
        ax.set_zlabel("Z-as")
        ax.set_title(f"3D Visualisatie van nummer {self.grid_edit.nummer} \n Score:{self.grid_edit.score}")
        legend_elements = [
        Line2D([0], [0], color='black', marker='x', linestyle='None', markersize=10, label='Kruising'),
        Line2D([0], [0], color='red', linewidth=3, label='Overlapping'),
        Line2D([0], [0], color='blue', marker='o', linestyle='None', markersize=8, label='Gate')
        ]

        # Voeg de aangepaste legenda toe
        ax.legend(handles=legend_elements, loc="upper right")
        ax.legend()

        # Set the view
        ax.view_init(elev=37, azim=-131, roll=7)
        ax.dist = 2

        if frame == total_frames - 1:
            print("\n3D visualisatie succesvol getoond.\n**Sluit het venster van animatie om programma te stoppen**")
            plt.savefig(f"eindstand_animatie_{self.grid_edit.nummer}.png", dpi=300)
            print(f"Afbeelding opgeslagen: eindstand_animatie_{self.grid_edit.nummer}.png")

    def visualisatie(self):
        """
        Visualiseert de gates en wires in een 3D-omgeving.
        Gates worden weergegeven als blauwe punten en wires als rode lijnen.
        z = 0 is de bodem
        """
        print("-----animatie-----")
        print("Start met maken van de animatie")

        # Setup - Gebruik het grid_edit object dat is doorgegeven aan de class
        grid_edit_obj = self.grid_edit
        fig = plt.figure(figsize=(11, 8))
        ax = fig.add_subplot(111, projection='3d')
        wires = grid_edit_obj.wirepaths_list
        animatie = self.animation

        
        total_frames = sum(len(wire) for wire in wires)
        # Maak de animatie
        animatie = FuncAnimation(fig, animatie, frames = total_frames, fargs=(ax, grid_edit_obj), interval=1, repeat=False)

        # Toon de animatie
        plt.show()
        
    
    def write_to_csv(self, wirepaths_list, overlapping_lijst, wirecount): # DEZE TOEVOEGEN
        # Open het CSV-bestand in 'append' mode
        grid_edit_obj = self.grid_edit
        with open('wirepaths.csv', 'a', newline='') as csvfile:
            kolom = ['nummer', 'pad', 'overlappingen', 'kruisingen', 'succes', 'score', 'aantal_wires', 'aantal_kruisingen']
            writer = csv.DictWriter(csvfile, fieldnames=kolom)

            # Als het bestand leeg is, schrijf dan eerst de header (kolomnamen)
            csvfile.seek(0, 2)  # Ga naar het einde van het bestand
            if csvfile.tell() == 0:  # Als het bestand leeg is, schrijf header
                writer.writeheader()

            # Genereer nummer voor de nieuwe rij
            with open('wirepaths.csv', 'r', newline='') as check_csvfile:
                reader = csv.reader(check_csvfile)
                rows = list(reader)
                nummer = len(rows)  # Nummer is gelijk aan het aantal rijen, zodat het begint bij 1

                # Dit zijn de andere gegevens die je wilt toevoegen. Pas deze aan op basis van je eigen logica.
                data = {
                    'nummer': nummer,
                    'pad': str(wirepaths_list),
                    'overlappingen': str(overlapping_lijst),
                    'kruisingen': str(grid_edit_obj.wirecross_list),
                    'succes': "Nee" if len(overlapping_lijst) > 0 else "Ja",  # klopt niet - als er geen overlapping is dus twee twee 
                    'score': grid_edit_obj.score,  # klopt niet
                    'aantal_wires': wirecount,  # Aantal draden in netwerk
                    'aantal_kruisingen': grid_edit_obj.wirecrosscount  # aantal kruisingen 
                }
                
                # Schrijf in csv bestand
                writer.writerow(data)
                nummer += 1  # Verhoog het nummer voor de volgende rij
        self.grid_edit.nummer = nummer - 1
        print("-----output-----")
        print("CSV-bestand succesvol geschreven.")
        print("\n")
