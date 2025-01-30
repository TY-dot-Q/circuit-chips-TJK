from itertools import cycle
import csv, os, ast
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
    
    def animation(self, frame, ax):
        """
        Functie die wordt aangeroepen voor elke frame van de animatie.
        """
        # Check of er gates zijn
        if not self.grid_edit.gate_dict:
            print("   geen gates in de dict")
            return
        
        if frame == 0:
            for _, (y, x, z) in self.grid_edit.gate_dict.items():
                ax.scatter(x, y, z, color='blue', s=100, marker='o')  # Teken de bolletjes
        
        kleuren_palet = cycle([ 
        'black', 'blue', 'green', 'orange', 'purple', 'teal', 'gold',
        'pink', 'coral', 'olive', 'indigo', 'yellow'])

        # Teken de lijnen stap voor stap
        wires = self.grid_edit.wirepaths_list
        if wires:
            total_frames = sum(len(wire) for wire in wires)
            current_frame = 0
            for wire in wires:
                wire_length = len(wire)
                kleur = next(kleuren_palet) 
                if frame < current_frame + wire_length:
                    wire_y, wire_x, wire_z = zip(*wire[:frame - current_frame + 1])
                    ax.plot(wire_x, wire_y, wire_z, color=kleur, linewidth = 2)
                    return
                current_frame += wire_length
        else:
            print("   geen wires gevonden")

        
        # print wirecrosses in visual
        if frame == total_frames - 1: 
            wirecross = self.grid_edit.wirecross_list 
            if wirecross:
                for y, x, z in wirecross:
                    ax.scatter(x, y, z, color='red', s=125, marker='x')
            else:
                print("   geen kruisingen gevonden.")


        # Laatste Frame weergegeven
        if frame == total_frames - 1: 

            # print wirecrosses in visual
            wirecross = self.grid_edit.wirecross_list 
            if wirecross:
                for y, x, z in wirecross:
                    ax.scatter(x, y, z, color='red', s=125, marker='x')
            else:
                print("   geen kruisingen gevonden.")

            # print overlaps in visual
            overlap = self.grid_edit.overlapping_lijst
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
        Line2D([0], [0], color='red', marker='x', linestyle='None', markersize=10, label='Kruising'),
        Line2D([0], [0], color='red', linewidth=3, label='Overlapping'),
        Line2D([0], [0], color='blue', marker='o', linestyle='None', markersize=8, label='Gate')
        ]

        # Voeg de aangepaste legenda toe
        ax.legend(handles=legend_elements, loc="upper right")

        # Set the view
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

        # Print wirecrosses in visual
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
        Gates worden weergegeven als blauwe punten en wires als rode lijnen.
        z = 0 is de bodem
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
            animation = FuncAnimation(fig, self.animation, frames = total_frames, fargs=(ax), interval=1, repeat=False)
            plt.show()
            
                  
        # Maak de afbeelding
        if order == 'afb':
            self.generate_3d_visual(ax)
    
        
    
    def write_to_csv(self, wirecount, name_file): # DEZE TOEVOEGEN
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
                nummer = 1 if len(rows) == 0 else len(rows)  # Nummer is gelijk aan het aantal rijen, zodat het begint bij 1

                # Dit zijn de andere gegevens die je wilt toevoegen. Pas deze aan op basis van je eigen logica.
                data = {
                    'nummer': nummer,
                    'pad': str(self.grid_edit.wirepaths_list),
                    'overlappingen': str(self.grid_edit.overlapping_lijst),
                    'kruisingen': str(self.grid_edit.wirecross_list),
                    'succes': "Ja" if (len(self.grid_edit.overlapping_lijst) == 0 and self.grid_edit.valide_counter == self.grid_edit.netlist_counter) else "Nee",  # klopt niet - als er geen overlapping is dus twee twee 
                    'score': self.grid_edit.score,  # klopt niet
                    'aantal_wires': wirecount,  # Aantal draden in netwerk
                    'aantal_kruisingen': self.grid_edit.wirecrosscount  # aantal kruisingen 
                }
                
                # Schrijf in csv bestand
                writer.writerow(data)
                self.grid_edit.nummer = nummer
        
        print("-----output-----")
        print("CSV-bestand succesvol geschreven.")
        print("\n")
        print(self.grid_edit.valide_counter, self.grid_edit.netlist_counter)

    def output_to_csv(self, matched_wires, netlist_path):
        """Slaat de matched wirepaths op in output.csv en overschrijft het bestand bij elke run."""
        output_file = "data/output.csv"
        split_parts = netlist_path.split("/")
        chip_id = split_parts[1]  
        net_id = split_parts[-1].replace("netlist_", "").replace(".csv", "") 

        # Leeg het bestand en schrijf de headers
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["net", "wires"])

            for chip_a, chip_b, path in matched_wires:
                writer.writerow([f"({chip_a},{chip_b})", f"{path}"])

            # Voeg de chip-net info toe
            writer.writerow([f"{chip_id}_net_{net_id}", self.grid_edit.score])
    
    def search_row(self, name_file):
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

        # Return de beste rij als deze is gevonden
        if best_row:
            return best_row
        
    def load_best_result(self, name_file, best_row):

        # Als een geldige rij is gevonden, importeer de waarden
        # Open CSV-bestand om de beste rij te zoeken
        with open(name_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['nummer'] == best_row['nummer']:  # Vergelijk met het juiste nummer
                    self.grid_edit.wirepaths_list = ast.literal_eval(best_row['pad'])  # Converteer string naar lijst
                    self.grid_edit.overlapping_lijst = ast.literal_eval(best_row['overlappingen'])  # Converteer string naar lijst
                    self.grid_edit.wirecross_list = ast.literal_eval(best_row['kruisingen'])  # Converteer string naar lijst
                    self.grid_edit.score = int(best_row['score'])  # Update de beste score
                    print(f"Beste score geladen: {self.grid_edit.score}, nummer {best_row['nummer']}")
                else:
                    print("Geen succesvolle resultaten gevonden.")


    def load_specific_result(self, name_file, nummer):
        # Open het CSV-bestand en zoek naar de rij met het opgegeven nummer
        with open(name_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['nummer'] == str(nummer):  # Vergelijk met het juiste nummer
                    # Gevonden rij, zet de waarden in de visualisatie objecten
                    self.grid_edit.wirepaths_list = ast.literal_eval(row['pad'])  # Converteer string naar lijst
                    self.grid_edit.overlapping_lijst = ast.literal_eval(row['overlappingen'])  # Converteer string naar lijst
                    self.grid_edit.wirecross_list = ast.literal_eval(row['kruisingen'])  # Converteer string naar lijst
                    self.grid_edit.score = int(row['score'])  # Update de score
                    print(f"Visualisatie geladen voor nummer {row['nummer']} met score {row['score']}")
    

    def visual(self):
        name_csv_file = "data/test.csv"
        max_num = 100000
        choice = input(f"\nWil je de visualisatie van een andere iteratie zien? \nTyp het nummer van de iteratie zoals staat in {name_csv_file} of \"stop\" om te stoppen: ")

        while not choice.isdigit() and int(choice) > max_num and choice != "stop":
            print(f"Ongeldige invoer :(, kies nummer tussen 1 en {max_num}.")
            continue

        if choice == "stop":
            print("Het programma wordt afgesloten :).")
            return

        choice = int(choice)
        self.load_specific_result(name_csv_file, choice)
        self.visualisatie()
