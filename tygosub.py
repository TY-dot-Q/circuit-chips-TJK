import csv, os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class grid_edit:
    grid=[]
    gate_dict={}
    wire_list=[]
    gate_nr =1

    def __init__(self):
        """initaliseer de gridedit class"""
        self.wirecount=0
        self.wirecrosscount=0
        self.score=0

    def grid_create (self, max_y, max_x) -> None:
        """
        creeert een array 3d grid gebaseerde op de globale max_z en opgegeven max_y en x
        let op dit vervangt alle waardes niet runnen nadat gates zijn opgegeven.
        """
        self.grid = [[[0 for _ in range(max_x)] for _ in range(max_y)] for _ in range(7)]
        print("grid succesvol gemaakt")

    def add_gate (self, y, x, z) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een nummer 1,2,3 etc en je kan hiermee dus gates toevoegen.
        gebruik x en y coordinaten
        """
        if not (0 <= z < len(self.grid) and 0 <= y < len(self.grid[0]) and 0 <= x < len(self.grid[0][0])):
            print(f"Error: Coordinates y={y}, x={x}, z={z} are out of bounds.")
            return
    
        if self.grid[z][y][x] ==0:
            self.grid[z][y][x] = self.gate_nr #voeg de gate toe
            self.gate_dict[self.gate_nr] = (y,x,z)
            print(self.gate_dict[self.gate_nr])
            print(f"gate met het nummer {self.gate_nr} toegevoegd op de coordinaten y={y}, x={x}, z={z} ")
            self.gate_nr +=1
            
        else:
            print(f"er staat al iets namelijk \"{self.grid[z][y][x]}\"")
    
    def add_wire (self, y, x, z) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een wire, checkt ook of er niet al een gate is. 
        """
        # early stop bij out of bounds 
        if not (0 <= z < len(self.grid) and 0 <= y < len(self.grid[0]) and 0 <= x < len(self.grid[0][0])):
            print(f"Error: Coordinates y={y}, x={x}, z={z} are out of bounds.")
            return

        if self.grid[z][y][x] ==0 or isinstance(self.grid[z][y][x], int): # als de coordinaten van de grid op een gate staan
            self.grid[z][y][x] = "+" #voeg de wire toe
            self.wirecount+=1
            self.wire_list.append((y,x,z))
            print(f"wire toegevoegd op de coordinaten y={y}, x={x} z={z} ")
            gate_nr = self.grid[z][y][x]
            if gate_nr not in self.gate_dict:
                self.gate_dict[gate_nr] = (y, x, z)  # Voeg toe aan gate dict
                print(f"Gate nummer {gate_nr} toegevoegd aan gate_dict op coördinaten y={y}, x={x}, z={z}")
            else:
                print(f"Gate nummer {gate_nr} staat al in gate_dict.")
        # als er al een draad is 
        elif self.grid[z][y][x]=="+":
            self.wirecrosscount+=1
            print(f"kruisende draad toegevoegd op de coordinaten y={y}, x={x} z={z} ")
        # als het misgaat
        else:
            print(f"er staat al iets namelijk: \"{self.grid[z][y][x]}\"")

    def connect_gates(self, gate1: int, gate2: int) -> None:
        """
        Verbind twee gates met een draad.
        Gate nummers worden opgegeven als gate1 en gate2. 
        Moet later overgenomen worden door netlist die aangeeft welke gates verbonden zijn
        """
        if gate1 not in self.gate_dict or gate2 not in self.gate_dict:
            print(f"Een of beide gate nummers {gate1} of {gate2} bestaan niet.")
            return

        start = self.gate_dict[gate1]
        end = self.gate_dict[gate2]

        y1, x1, z1 = start
        y2, x2, z2 = end
        
        # Voegt lijn van gate tot eerste punt van pad toe
        self.add_wire(y1, x1, z1)

        '''
        Basis Manhattan-distance "algoritme" voor testen wires leggen
        Algoritme kan met a* vanuit hier worden uitgebreid!
        '''
        current_y, current_x, current_z = y1, x1, z1

        # loop om middelste stuk draad van pad te maken
        while (current_y, current_x, current_z) != (y2, x2, z2):
            # Verplaats in y-as
            if current_y != y2:
                current_y += 1 if current_y < y2 else -1
            # Verplaats in x-as
            elif current_x != x2:
                current_x += 1 if current_x < x2 else -1
            # Verplaats in z-as
            elif current_z != z2:
                current_z += 1 if current_z < z2 else -1

            # Voeg de draad toe op de huidige locatie
            self.add_wire(current_y, current_x, current_z)

        # Voegt lijn van laatste punt van pad tot eindgate toe
        self.add_wire(y2, x2, z2)
        self.wirecount -= 1


    def gate_location(self, nr_check)->int:
        return self.gate_dict[nr_check]

class user_input:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

    def score_request(self, score)-> None:
        print(f"er zijn {self.grid_edit.wirecount} draden")
        print(f"er zijn {self.grid_edit.wirecrosscount} die overelkaar lopen")
        print(f"dit geeft een score van c={score}") # score wordt gereturnd door functie costen_berekening in class output
    
    def load_gates(self, file_path: str)-> None:
            """gates toevoegen van de csv lijst, gebruikt de file path"""
            """gates toevoegen van de csv lijst, gebruikt de file path"""
            if not os.path.isfile(file_path):
                print(f"Bestand '{file_path}' niet gevonden!")
            else:
                try:
                    with open(file_path, mode='r') as file:
                        csv_reader = csv.reader(file)
                        next(csv_reader)  # sla de eerste regel over

                        for row in csv_reader:
                            if len(row) < 2:
                                print(f"Ongeldige regel in CSV-bestand: {row}")
                                continue

                            try:
                                y=int(row[0])
                                x=int(row[1])
                                z=int(row[2])
                                self.grid_edit.add_gate(y,x,z)
                            except ValueError:
                                print(f'print:error met waardes in regel:{row}')
                                continue

                    print("Alle gates zijn succesvol geladen uit het CSV-bestand.")
                except FileNotFoundError:
                    print(f"Fout: Het bestand '{file_path}' bestaat niet.")
                except ValueError:
                    print("Fout: Ongeldige waarden in het CSV-bestand.")

    def max_grid_values(self, file_path: str):
        """Bepaal de maximale y-, x-, en z-waarden uit een CSV-bestand.
        Het bestand moet een lijst van coördinaten bevatten.
        Retourneert een tuple (max_y, max_x, max_z)."""
         
        max_y, max_x = 0, 0  # Initiële waarden voor maxima

        if not os.path.isfile(file_path):
            print(f"Bestand '{file_path}' niet gevonden!")
            return max_y, max_x  # Zorg voor een veilige return bij fout

        try:
            with open(file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Sla de kopregel over

                for row in csv_reader:
                    if len(row) < 2:  # Controleer of er minimaal y en x aanwezig zijn
                        print(f"Ongeldige regel in CSV-bestand: {row}")
                        continue

                    try:
                        y = int(row[0])
                        x = int(row[1])

                        max_y = max(max_y, y)
                        max_x = max(max_x, x)
                        max_y=max_y+4
                        max_x=max_x+4
                    except ValueError:
                        print(f"Fout bij het verwerken van regel: {row}")
                        continue

            print(f"Maximale waarden gevonden: y={max_y}, x={max_x}")
            return max_y, max_x

        except Exception as e:
            print(f"Fout tijdens het lezen van het bestand: {e}")
            return max_y, max_x  # Zorg voor een veilige return

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
        score = (self.grid_edit.wirecount) + 300 * self.grid_edit.wirecrosscount
        return score
    
    def visualisatie(self):
        """
        Visualiseert de gates en wires in een 3D-omgeving.
        Gates worden weergegeven als blauwe punten en wires als rode lijnen.
        """
        # Gebruik het grid_edit object dat is doorgegeven aan de class
        grid_edit_obj = self.grid_edit
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')


        print(grid_edit_obj.gate_dict[2])
        print(grid_edit_obj.gate_nr)
        if not grid_edit_obj.gate_dict:
            print("geen gates in de dict")
            return
        
        # zet gates in visualisatie grid 
        for gate_nr, (y, x, z) in grid_edit.gate_dict.items():
            ax.scatter(x, y, z, color='blue', label=f'Gate {gate_nr}' if gate_nr == 1 else "", s=100)
        
         # maakt lijnen voor pad in visualisatie
        wires = self.grid_edit.wire_list
        if wires:
            wire_x, wire_y, wire_z = zip(*wires)
            
            ax.plot(wire_x, wire_y, wire_z, color='purple', linewidth=2, label='Wire Path')
        else:
            print("Geen wires gevonden")


        # Instellen van ticks met stappen van 1
        ax.set_xticks(range(int(ax.get_xlim()[0]), int(ax.get_xlim()[1]) + 2, 1))
        ax.set_yticks(range(int(ax.get_ylim()[0]), int(ax.get_ylim()[1]) + 2, 1))
        ax.set_zlim(bottom = 1)
        ax.set_zticks(range(1, 10, 1))

        # correctie om y-as om te draaien 
        '''
        Dit maakt het mogelijk dat de coordinaten 0,0 voor x,y onderaan begint
        '''
        ax.invert_yaxis()
        ax.invert_xaxis()

        # Labels and legend
        ax.set_xlabel("X-as")
        ax.set_ylabel("Y-as")
        ax.set_zlabel("Z-as")
        ax.set_title("3D Visualisatie van Gates en Wires")
        ax.legend()

        # Tweak the view
        ax.view_init(elev=30, azim=30)
        plt.show()    

class start:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

    def Auto_start_functie(self, user_path) ->None:
        """
        deels om te testen of het werkt maar je kan hier de grid opgeven, gates toevoegen en kijken wat de uitkomst is
        """
        grid_edit_obj = grid_edit()
        user_input_obj = user_input(grid_edit_obj)

        #geef eerst de maximaal breedte en hoogte y en x van de grid (hoogte standaard 3)
        
        max_y, max_x = user_input_obj.max_grid_values(user_path)

        grid_edit_obj.grid_create(max_y, max_x) #maakt de grid met de opgegeven hoogte en breedt
        
        # user_path=input("geef de file path op: ")
        user_input_obj.load_gates(user_path)

class algorithm:
    #def algorithm() ->None:
        #"grid_edit_obj.addgate(5,6,1)" om een gate toe tevoegen
        #"grid_edit_obj.addwire(5,6,1)" om een wire toe te voegen (z level is hier nodig)
        #""


    def manual_check():
        grid_edit_obj = grid_edit()
        user_input_obj = user_input(grid_edit_obj)
        output_obj = output(grid_edit_obj)
        # Maak een grid en voeg gates toe
        grid_edit_obj.grid_create(10, 10)
        grid_edit_obj.add_gate(1, 1, 1)
        grid_edit_obj.add_gate(5, 5, 1)
        grid_edit_obj.add_gate(5, 1, 1)
        grid_edit_obj.add_gate(2, 3, 1)

        # Verbind de gates
        grid_edit_obj.connect_gates(1, 2)


        # Visualiseer de resultaten
        score = output_obj.costen_berekening()
        user_input_obj.score_request(score)
        output_obj.print_grid()
        output_obj.visualisatie()
    
    manual_check()

#wanneer kruizen wires elkaar precies bij dit probleem als ze een moment dezelfde coordinaten delen en niet lid zijn van een doorlopende wire die twee gates met elkaar verbind dus de wires die deel zijn van dezelfde ketting kunnen niet als gekruist worden gezien tenzij ze overzichzelf heen kruizen vanuit een andere kant dus bijvoorbeeld x,y is 1,2 en xy is verbonden met x,y is 3,2 door middel van 2 wires  maar x,y 2,3 en 2,1 zijn ook verbonden met 2 wires. deze kruizen elkaar omdat ze allebei over 2,2 heen gaan maar niet de wires nooit hetzelfde pas afleggen dus ze delen niet meer dan 1 coordinaat.