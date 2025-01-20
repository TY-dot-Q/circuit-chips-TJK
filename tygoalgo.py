import csv, os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

gate_nrstart =1

class grid_edit:
    grid=[]
    gate_dict={}
    wire_list=[]
    gate_nr = gate_nrstart
    

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
        print("grid succesfol gemaakt")

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
            gate_nrstart
            
        else:
            print(f"er staat al iets namelijk \"{self.grid[z][y][x]}\"")

    def gate_amount_count(self):
        grid_edit_obj=grid_edit()

        amount=0

        for item in grid_edit_obj.gate_dict:
            amount+=1
            item+=1

        #print(f"amount{amount}")

        return amount
    
    def add_wire (self, y, x, z) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een wire, checkt ook of er niet al een gate is. 
        """
        if not (0 <= z < len(self.grid) and 0 <= y < len(self.grid[0]) and 0 <= x < len(self.grid[0][0])):
            print(f"Error: Coordinates y={y}, x={x}, z={z} are out of bounds.")
            return

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
    
    def dichtstbij(self, gate_check, list_iligal_gates):
        """checkt wat de dichstbijzijnde gate is, geeft de gate terug en de afstand"""
        #pak de hoeveelheid gates

        #pak de coordinaten van de gate die wordt gevraagd
        print(f"gate_check{gate_check}")
        if gate_check <=0:
            return -1, -1
        
        y,x,z = self.gate_dict[gate_check]
        print(f"y={y} -- x={x} -- z={z}")
        gate_nr_teller = self.gate_amount_count()

        gate_return=0
        check_optimum=0
        #loop de andere gates
        if gate_nr_teller<1:
            print("te weinig gates om dit uit te voeren")
            return -1, -1

        while gate_nr_teller > 1:
            #test of de y,x en z waardes afstand samen groter is dan de vorige (in begin 0)
            if gate_nr_teller!=gate_check & gate_nr_teller not in list_iligal_gates: 
                test_y, test_x, test_z = self.gate_dict[gate_nr_teller]
                v1 = abs(test_y - y)
                v2 = abs(test_x - x) 
                v3 = abs(test_z - z)
                
                if check_optimum>(v3+v2+v1):
                    check_optimum =v3+v2+v1
                    gate_return=gate_nr_teller

            gate_nr_teller -=1
        
        return gate_return, check_optimum

                
class user_input:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

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
        score = self.grid_edit.wirecount + 300 * self.grid_edit.wirecrosscount
        return score
    
    def visualisatie(self):
            """
            Visualiseert de gates en wires in een 3D-omgeving.
            Gates worden weergegeven als blauwe punten en wires als rode lijnen.
            """
            # Gebruik het grid_edit object dat is doorgegeven aan de class
            grid_edit_obj = grid_edit()
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')

            print(grid_edit.gate_dict[2])
            print(grid_edit.gate_nr)
            if not grid_edit.gate_dict:
                print("geen gates in de dict")
                return
            
            # Plot gates
            for gate_nr, (y, x, z) in grid_edit.gate_dict.items():
                ax.scatter(x, y, z, color='blue', label=f'Gate {gate_nr}' if gate_nr == 1 else "", s=100)
            
            # Plot wires
            wires = grid_edit.wire_list
            if wires:
                wire_x, wire_y, wire_z = zip(*wires)  # Unpack wire coordinates
                ax.scatter(wire_x, wire_y, wire_z, color='red', label='Wire', s=50)

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
    

    def gate_nr(self):
        grid_edit_obj=grid_edit()

        amount=0

        for item in grid_edit_obj.gate_dict:
            amount+=1
            item+=1

        print(f"amount{amount}")

        return amount
        

    def use_algorithm(self) ->None:
        #"grid_edit_obj.addgate(5,6,1)" om een gate toe tevoegen
        #"grid_edit_obj.addwire(5,6,1)" om een wire toe te voegen (z level is hier nodig)
        min_value=99999999

        #pak gate hoeveel heid
        grid_edit_obj = grid_edit()
        
        start_teller =self.gate_nr()
        
        start_gate_r2=0

        print(f"aantal gates moet nu 5 zijn:({start_teller})")
        #loop dat alle gate nummers overgaat om te checken wat het beste start punt is
        while start_teller>1:
            current_gate = start_teller
            test_value=0
            list_gates1=[]
            list_gates2=[]

            #eerste loop maakt paren van 2
            while current_gate>=1:
                #skipt gates die al verbonden zijn
                if current_gate not in list_gates1:
                    print(f"current gate{current_gate}:")
                    #geeft een gate die nog niet verbonden is en de afstand (value) terug tot de opgegeven current_gate
                    connect_gate, value = grid_edit_obj.dichtstbij(current_gate, list_gates1) 
                    print(f"connect_gate: {connect_gate} -- value: {value}")

                    #-1, -1 wordt terug gegeven als er geen andere gate wordt gevonden
                    if connect_gate == -1 & value==-1:
                        start_gate_r2=current_gate
                        current_gate-=1
                        
                        continue
                        
                    #dubbel checkt of de connect_gate niet al in de lijst zit
                    elif connect_gate not in list_gates1:
                        #past de score aan
                        test_value+=value

                        #voegt de 2 gates die verbonden zijn aan de lijst zodat ze niet nog een keer gecontroleerd worden
                        list_gates1.append(connect_gate)
                        list_gates1.append(current_gate)
    
                current_gate-=1

            #gedeelte (2) koppel de gates nog 1 keer aan een andere

            current_gate=start_teller#reset de gate zodat hij weer alle langs kan
            
            #maak de eerste connectie van de overig gate als die er is
            if start_gate_r2!=-2:
                connect_gate, value = grid_edit_obj.dichtstbij(start_gate_r2, list_gates2) #list 2 omdat dit de tweede connectie wordt
                test_value+=value

                list_gates1.append(start_gate_r2)
                list_gates2.append(connect_gate)

            print(list_gates1)
            
            #maakt een connectie voor alle gates die niet voorkomen in list_gates1 en 2 (dus nog 1 connectie hebben)
            while current_gate>1:
                #skipt gates die al verbonden zijn voor de tweede keer
                if current_gate not in list_gates2:
                    #geeft een gate die nog niet verbonden is voor de tweede keer en de afstand (value) terug tot de opgegeven current_gate
                    connect_gate, value = grid_edit_obj.dichtstbij(current_gate, list_gates2) 
                    
                    #-1, -1 wordt terug gegeven als er geen andere gate wordt gevonden
                    if connect_gate == -1 & value==-1:
                        start_gate_r2=current_gate
                        current_gate-=1
                        
                        continue
                        
                    #dubbel checkt of de connect_gate niet al in de lijst zit
                    elif connect_gate not in list_gates2:
                        #past de score aan
                        test_value+=value

                        #voegt de 2 gates die verbonden zijn aan de lijst zodat ze niet nog een keer gecontroleerd worden
                        list_gates2.append(connect_gate)
                        list_gates2.append(current_gate)
    
                current_gate-=1

            #zet de test_value naar min_value als de score lager is (hoop is dat dit dan de laagste waarde geeft en dus de beste score)
            print(f"test_value===={test_value}")
            if test_value<min_value:
                min_value=test_value

            start_teller-=1

        return min_value #min_value

class start_the_code:
    def manual_check():
        grid_edit_obj = grid_edit()
        user_input_obj = user_input(grid_edit_obj)
        output_obj = output(grid_edit_obj)
        start_obj =start(grid_edit_obj)
        algorithm_obj=algorithm()
        
        path="gates.csv"
            

        start_obj.Auto_start_functie(path)
        
        print("De uiteindelijke grid is:")
        #output_obj.print_grid()

        print(algorithm_obj.use_algorithm())

        output_obj.costen_berekening()
        user_input_obj.score_request()

        #output_obj.visualisatie()
    
    manual_check()