import csv, os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class grid_edit:
    def __init__(self):
        """initaliseer de gridedit class"""
        self.grid=[]
        self.gate_dict={}
        self.wire_list=[]
        self.gatenr =1
        self.wirecount=0
        self.wirecrosscount=0
        self.score=0

    def grid_create (self, max_y, max_x, max_z) -> None:
        """
        creeert een array 3d grid gebaseerde op de globale max_z en opgegeven max_y en x
        let op dit vervangt alle waardes niet runnen nadat gates zijn opgegeven.
        """
        self.grid = [[[0 for _ in range(max_x)] for _ in range(max_y)] for _ in range(max_z)]
        print("grid succesfol gemaakt")

    def add_gate (self, y, x, z) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een nummer 1,2,3 etc en je kan hiermee dus gates toevoegen.
        gebruik x en y coordinaten
        """
        if self.grid[z][y][x] ==0:
            self.grid[z][y][x] = self.gatenr #voeg de gate toe
            self.gate_dict[self.gatenr] = (y,x,z)
            print(f"gate met het nummer {self.gatenr} toegevoegd op de coordinaten y={y}, x={x}, z={z} ")
            self.gatenr +=1
            
            
        else:
            print(f"er staat al iets namelijk \"{self.grid[z][y][x]}\"")
    
    def add_wire (self, y, x, z) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een wire, checkt ook of er niet al een gate is. 
        """
        if self.grid[z][y][x] ==0:
            self.grid[z][y][x] = "+" #voeg de wire toe
            self.wirecount+=1
            self.wire_list.append((y,x,z))
            print(f"wire toegevoegd op de coordinaten y={y}, x={x} z={z} ")
        elif self.grid[z][y][x]=="+":
            self.wirecrosscount+=1
            print(f"kruisende draad toegevoegd op de coordinaten y={y}, x={x} z={z} ")

        else:
            print(f"er staat al iets namelijk: \"{self.grid[z][y][x]}\"")

    def gate_location(self, nr_check)->int:
        return self.gate_dict[nr_check]

class user_input:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj
        auto_y =5
        auto_x=5
        auto_z=3

    def add_gate_request(self)->None:
        """
        geeft een makkelijke manier om meerdere gates toe te voegen
        herhaalt de addgatefunctie totdat de user stop typ. de input is y,x coordinaten
        """
        print("geef de cordinaten van de gates, typ: 'stop' wanneer je klaar bent")
        while True:
            user_coordinates = input("coordinaten bijv: 'y,x'")
            if user_coordinates.lower()=="stop":
                break
            
            try:
                y, x = map(int, user_coordinates.split(','))
                self.grid_edit.add_gate(y,x)
            except ValueError:
                print("eroor: ongeldige invoer")      

    def add_wire_request(self)->None:
        """
        geeft een makkelijke manier om meerdere wires toe te voegen
        herhaalt de addwire functie totdat de user stop typ. de input is y,x, z coordinaten
        """
        print("geef de cordinaten van de wires, typ: 'stop' wanneer je klaar bent")
        while True:
            user_coordinates = input("coordinaten bijv: 'y,x,z'")
            if user_coordinates.lower()=="stop":
                break
            
            try:
                y, x, z = map(int, user_coordinates.split(','))
                self.grid_edit.add_wire(y,x, z)
            except ValueError:
                print("eroor: ongeldige invoer")  
    
    def score_request(self)->None:
        print(f"er zijn {self.grid_edit.wirecount} draaden")
        print(f"er zijn {self.grid_edit.wirecrosscount} die overelkaar lopen")
        print(f"dit geeft een score van c={self.grid_edit.score}")
    
    def load_gates(self, file_path: str)->None:
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
                                z=int(row[2]) if len(row)>2 else 3
                                self.grid_edit.add_gate(y,x,z)
                            except ValueError:
                                print(f'print:error met waardes in regel:{row}')
                                continue

                    print("Alle gates zijn succesvol geladen uit het CSV-bestand.")
                except FileNotFoundError:
                    print(f"Fout: Het bestand '{file_path}' bestaat niet.")
                except ValueError:
                    print("Fout: Ongeldige waarden in het CSV-bestand.")

    def max_grid_values(self, file_path: str) -> tuple:
        """Bepaal de maximale y-, x-, en z-waarden uit een CSV-bestand.
        Het bestand moet een lijst van coördinaten bevatten.
        Retourneert een tuple (max_y, max_x, max_z)."""
        
        
        max_y, max_x, max_z = 0, 0, 0  # Initiële waarden voor maxima

        if not os.path.isfile(file_path):
            print(f"Bestand '{file_path}' niet gevonden!")
            return max_y, max_x, max_z  # Zorg voor een veilige return bij fout

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
                        z = int(row[2]) if len(row) > 2 else 0  # Standaardwaarde voor z

                        max_y = max(max_y, y)
                        max_x = max(max_x, x)
                        max_z = max(max_z, z)
                    except ValueError:
                        print(f"Fout bij het verwerken van regel: {row}")
                        continue

            print(f"Maximale waarden gevonden: y={max_y}, x={max_x}, z={max_z}")
            return max_y, max_x, max_z

        except Exception as e:
            print(f"Fout tijdens het lezen van het bestand: {e}")
            return max_y, max_x, max_z  # Zorg voor een veilige return

class output:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

    def print_grid (self, max_z) -> None:
        """
        print de huidig grid status met gates en verschillende lagen.
        """
        for z in range(max_z):
            print(f"laag {z}")
            for row in self.grid_edit.grid[z]:
                print(row) 
        print("klaar met printen")

    def costen_berekening(self)->int:
        """berekent de score van de geplaatste draden"""
        score = self.grid_edit.wirecount + 300 * self.grid_edit.wirecrosscount
        return score
    
    def visualisatie(self)->None:
        

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

        for gate_nr, (y,x,z) in self.grid_edit.gate_dict.items():
            ax.scatter(y,x,z, color='blue', label=f'gate{gate_nr}')
        
            for z in range(len(self.grid_edit.grid)):
                for y in range(len(self.grid_edit.grid[z])):
                    for x in range(len(self.grid_edit.grid[z][y])):
                        if self.grid_edit.grid[z][y][x] == "+":
                            ax.scatter(x, y, z, color='red', label='Wire')

        ax.set_xlabel('X-as')
        ax.set_ylabel('Y-as')
        ax.set_zlabel('Z-as')

        plt.show()


class start:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

    def Start_functie(self) ->None:
        """
        deels om te testen of het werkt maar je kan hier de grid opgeven, gates toevoegen en kijken wat de uitkomst is
        """
        grid_edit_obj = grid_edit()

        #geef eerst de maximaal breedte en hoogte y en x van de grid (hoogte standaard 3)
        user_hoogte = int(input("geeft de maximaale verticale hoogte: 'y'"))
        max_y = user_hoogte #maak lijn hierboven commentaar en verander user_hoogte naar een waarde

        user_breedte = int(input("geeft de maximaale horizontale lengte: 'x'"))
        max_x = user_breedte #maak lijn hierboven commentaar en verander user_hoogte naar een waarde

        grid_edit_obj.grid_create(max_y, max_x, 3) #maakt de grid met de opgegeven hoogte en breedt

    def Auto_start_functie(self, user_path) ->None:
        """
        deels om te testen of het werkt maar je kan hier de grid opgeven, gates toevoegen en kijken wat de uitkomst is
        """
        grid_edit_obj = grid_edit()
        user_input_obj = user_input(grid_edit_obj)

        #geef eerst de maximaal breedte en hoogte y en x van de grid (hoogte standaard 3)
        

        # user_path=input("geef de file path op: ")
        user_input_obj.load_gates(user_path)

        max_y, max_x, max_z = user_input_obj.max_grid_values(user_path)


        grid_edit_obj.grid_create(max_y, max_x, max_z) #maakt de grid met de opgegeven hoogte en breedt
    

class algorithm:
    #def algorithm() ->None:
        #"grid_edit_obj.addgate(5,6,1)" om een gate toe tevoegen
        #"grid_edit_obj.addwire(5,6,1)" om een wire toe te voegen (z level is hier nodig)
        #""

    def manual_check():
        grid_edit_obj = grid_edit()
        user_input_obj = user_input(grid_edit_obj)
        output_obj = output(grid_edit_obj)
        start_obj =start(grid_edit_obj)
        
        path="C:\\Users\\tygob\\Documents\\GitHub\\circuit-chips-TJK\\code"
            
        start_obj.Start_functie()

        user_input_obj.load_gates(path)
        
        user_input_obj.add_gate_request()
        user_input_obj.add_wire_request()

        
        print("De uiteindelijke grid is:")
        output_obj.print_grid(3)

        output_obj.costen_berekening()
        user_input_obj.score_request()

        output_obj.visualisatie()

    manual_check() #maak commentaar als je het niet handmatig wil checken