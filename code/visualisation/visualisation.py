from itertools import cycle
import csv, ast
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D

class output:
    '''
    Deze class bevat de functies voor het printen van de grid, 
    het berekenen van de kosten en het maken van de visualisatie.
    '''
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj


    def print_grid (self) -> None:
        """
        Print de huidig grid status met gates en verschillende lagen.
        """
        # Print de grid in de terminal
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
        """
        Berekent de score van de geplaatste draden
        """
        self.grid_edit.score = wirecount + (300 * self.grid_edit.wirecrosscount)

    def animation(self, frame, ax, grid_edit_obj):
        """
        Functie die wordt aangeroepen voor elke frame van de 3D animatie.
        """
        # Check of er gates zijn
        if not grid_edit_obj.gate_dict:
            print("   geen gates in de dict")
            return

        # Zet gates in de visualisatie
        if frame == 0:
            for _, (y, x, z) in grid_edit_obj.gate_dict.items():
                ax.scatter(x, y, z, color='blue', s=100, marker='o')  

        # Maak een kleurenpalet voor de draden
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


        # print kruisingen in visual
        if frame == total_frames - 1: 
            wirecross = grid_edit_obj.wirecross_list 
            if wirecross:
                for y, x, z in wirecross:
                    ax.scatter(x, y, z, color='red', s=125, marker='x')
            else:
                print("   geen kruisingen gevonden.")

            # print overlappingen in visual
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


        # set assen
        ax.set_xticks(range(0, self.grid_edit.maximum_x + 3, 1))
        ax.set_yticks(range(0, self.grid_edit.maximum_y + 3, 1))
        ax.set_zlim(bottom=0)
        ax.set_zticks(range(1, 10, 1))


        # labels and titels
        ax.set_xlabel("X-as")
        ax.set_ylabel("Y-as")
        ax.set_zlabel("Z-as")
        ax.set_title(f"3D Visualisatie van nummer {self.grid_edit.nummer} \n Score:{self.grid_edit.score}")
        legend_elements = [
        Line2D([0], [0], color='red', marker='x', linestyle='None', markersize=10, label='Kruising'),
        Line2D([0], [0], color='red', linewidth=3, label='Overlapping'),
        Line2D([0], [0], color='blue', marker='o', linestyle='None', markersize=8, label='Gate')
        ]

        # Voeg de aangepaste legenda toe
        ax.legend(handles=legend_elements, loc="upper right")

        # Set de kijkhoek
        ax.view_init(elev=37, azim=-131, roll=7)
        ax.dist = 2

        if frame == total_frames - 1:
            print("\n3D visualisatie succesvol getoond.\n**Sluit het venster van animatie om programma te stoppen**")

    def generate_3d_visual(self, ax):
        """
        Genereert een 3D-visualisatie en slaat deze op als een afbeelding.
        """
        # Check of er gates zijn
        if not self.grid_edit.gate_dict:
            print("   geen gates in de dict")
            return

        # Zet gates in de visualisatie
        for _, (y, x, z) in self.grid_edit.gate_dict.items():
            ax.scatter(x, y, z, color='blue', s=100, marker='o')

        kleuren_palet = cycle([
            'black', 'blue', 'green', 'orange', 'purple', 'teal', 'gold',
            'pink', 'coral', 'olive', 'indigo', 'yellow'
        ])

        # Teken de draden
        wires = self.grid_edit.wirepaths_list
        if wires:
            for wire in wires:
                kleur = next(kleuren_palet)
                wire_y, wire_x, wire_z = zip(*wire)
                ax.plot(wire_x, wire_y, wire_z, color=kleur, linewidth=2)
        else:
            print("   geen wires gevonden")

        # Print kruisingen in visual
        wirecross = self.grid_edit.wirecross_list
        if wirecross:
            for y, x, z in wirecross:
                ax.scatter(x, y, z, color='red', s=125, marker='x')
        else:
            print("   geen kruisingen gevonden.")

        # Print overlaps in visual
        overlap = self.grid_edit.overlapping_lijst
        if overlap:
            for segment in overlap:
                if len(segment) == 2:
                    overlap_y, overlap_x, overlap_z = zip(*segment)
                    ax.plot(overlap_x, overlap_y, overlap_z, color='red', linewidth=3)
        else:
            print("   geen overlappingen gevonden.")

        # Stel assen in
        ax.set_xticks(range(0, self.grid_edit.maximum_x + 1, 1))
        ax.set_yticks(range(0, self.grid_edit.maximum_y + 1, 1))
        ax.set_zlim(bottom=0)
        ax.set_zticks(range(1, 10, 1))

        # Labels en titel
        ax.set_xlabel("X-as")
        ax.set_ylabel("Y-as")
        ax.set_zlabel("Z-as")
        ax.set_title(f"3D Visualisatie van nummer {self.grid_edit.nummer} \n Score:{self.grid_edit.score}")

        # Voeg legenda toe
        legend_elements = [
            Line2D([0], [0], color='red', marker='x', linestyle='None', markersize=10, label='Kruising'),
            Line2D([0], [0], color='red', linewidth=3, label='Overlapping'),
            Line2D([0], [0], color='blue', marker='o', linestyle='None', markersize=8, label='Gate')
        ]
        ax.legend(handles=legend_elements, loc="upper right")

        # Set de kijkhoek
        ax.view_init(elev=37, azim=-131, roll=7)
        ax.dist = 2

        # Sla afbeelding op
        filename = f"3D_visualisatie_{self.grid_edit.nummer}.png"
        plt.savefig(filename, dpi=300)
        print(f"Afbeelding opgeslagen: {filename}")
        print("**Sluit het venster van 3D visualisatie om programma te stoppen**")
        plt.show()


    def visualisatie(self):
        """
        Visualiseert de gates en wires in een 3D-omgeving.
        Gates worden weergegeven als blauwe punten en wires als rode lijnen
        Je kan kiezen tussen animatie of afbeelding.
        """
        print("-----visualisatie-----")
        print("Start met maken van de animatie")

        # Vraag de gebruiker of ze een animatie of afbeelding willen
        order = input("Wil je animatie of afbeelding? Typ ani of afb: ")
        while order != "ani" and order != "afb":
            order = input("Wil je animatie of afbeelding? Typ ani of afb: ")
        
        # Setup - Gebruik het grid_edit object dat is doorgegeven aan de class
        fig = plt.figure(figsize=(11, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Maak de animatie
        if order == 'ani':
            wires = self.grid_edit.wirepaths_list
            total_frames = sum(len(wire) for wire in wires)
            animation = FuncAnimation(fig, self.animation, frames = total_frames, fargs=(ax, self.grid_edit), interval=1, repeat=False)
            plt.show()
            
                  
        # Maak de afbeelding
        if order == 'afb':
            self.generate_3d_visual(ax)
        
    
    def write_to_csv(self, wirecount, name_file): # DEZE TOEVOEGEN
        """
        Schrijft de huidige wirepaths, overlappingen, kruisingen en score naar een CSV-bestand genaamd data.
        Deze functie wordt voornamelijk gebruikt voor data-analyse en het bijhouden van de voortgang
        het bestand staat in de map 'data'.
        """
        # Open het CSV-bestand in 'append' mode
        with open(name_file, 'a', newline='') as csvfile:
            kolom = ['nummer', 'pad', 'overlappingen', 'kruisingen', 'succes', 'score', 'aantal_wires', 'aantal_kruisingen']
            writer = csv.DictWriter(csvfile, fieldnames=kolom)

            # Als het bestand leeg is, schrijf dan eerst de header (kolomnamen)
            csvfile.seek(0, 2)  # Ga naar het einde van het bestand
            if csvfile.tell() == 0:  # Als het bestand leeg is, schrijf header
                writer.writeheader()

            # Genereer nummer voor de nieuwe rij
            with open(name_file, 'r', newline='') as check_csvfile:
                reader = csv.reader(check_csvfile)
                rows = list(reader)
                nummer = 1 if len(rows) == 0 else len(rows)  # Nummer is gelijk aan het aantal rijen, begint bij 1

                # gegevens voor elke rij
                data = {
                    'nummer': nummer,
                    'pad': str(self.grid_edit.wirepaths_list),
                    'overlappingen': str(self.grid_edit.overlapping_lijst),
                    'kruisingen': str(self.grid_edit.wirecross_list),
                    'succes': "Ja" if (len(self.grid_edit.overlapping_lijst) == 0 and self.grid_edit.valide_counter == self.grid_edit.netlist_counter) else "Nee",  # checkt naar valide oplossing
                    'score': self.grid_edit.score,  # score van hele netwerk
                    'aantal_wires': wirecount,  # Aantal draden in netwerk
                    'aantal_kruisingen': self.grid_edit.wirecrosscount  # aantal kruisingen 
                }
                
                # Schrijf gegevens in csv bestand
                writer.writerow(data)
                self.grid_edit.nummer = nummer
        
        print("-----output-----")
        print("CSV-bestand succesvol geschreven.")
        print("\n")
        print(self.grid_edit.valide_counter, self.grid_edit.netlist_counter)

    def output_to_csv(self, matched_wires, netlist_path):
        """
        Deze functie slaat beste resultaat op in output.csv volgens richtlijn van de opdracht
        Overschrijft het bestand bij elke run. De output staat in de map data.
        """
        output_file = "data/output.csv"
        split_parts = netlist_path.split("/")
        chip_id = split_parts[1]  
        net_id = split_parts[-1].replace("netlist_", "").replace(".csv", "") 

        # maak bestand leeg en schrijf de headers
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["net", "wires"])

            for chip_a, chip_b, path in matched_wires:
                writer.writerow([f"({chip_a},{chip_b})", f"{path}"])

            # Voeg de chip en net toe aan de output
            writer.writerow([f"{chip_id}_net_{net_id}", self.grid_edit.score])
    
    def search_row(self, name_file):
        """
        Zoekt de rij met de beste score in het data CSV-bestand.
        Geeft de rij van de beste terug als string 
        """
        best_score = None
        best_row = None

        # Open CSV-bestand om de beste rij te zoeken
        with open(name_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['succes'] == "Ja":
                    score = int(row['score'])  # Zet score om naar een integer

                    # Eerste keer instellen of als een betere score wordt gevonden
                    if best_score is None or score < best_score:
                        best_score = score
                        best_row = row 

        # Return de beste rij als deze is gevonden als 
        if best_row:
            return best_row
        
    def load_best_result(self, name_file, best_row):
        """
        Neemt best row van search_row functie en
        laadt de beste resultaten van het data CSV-bestand in de grid_edit object.
        Hierdoor kunnen de gegevvens door output_to_csv en visualitatie worden gebruikt.
        """

        # Open CSV-bestand om de beste rij te zoeken
        with open(name_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['nummer'] == best_row['nummer']:  # Vergelijk met het juiste nummer
                    self.grid_edit.wirepaths_list = ast.literal_eval(best_row['pad'])  # zet string om naar lijst
                    self.grid_edit.overlapping_lijst = ast.literal_eval(best_row['overlappingen'])  # zet string om naar lijst
                    self.grid_edit.wirecross_list = ast.literal_eval(best_row['kruisingen'])  # zet string om naar lijst
                    self.grid_edit.score = int(best_row['score'])  # Update de beste score
                    print(f"Beste score geladen: {self.grid_edit.score}, nummer {best_row['nummer']}")
