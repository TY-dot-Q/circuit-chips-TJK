from itertools import cycle
import csv, os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation
import heapq

gate_nrstart = 1

class grid_edit:
    grid=[]
    gate_dict={}
    wirepaths_list=[]
    gate_nr = gate_nrstart
    

    def __init__(self):
        """initaliseer de gridedit class"""
        self.wirecount=0
        self.wirecrosscount=0
        self.score=0
        self.maximum_y = 0
        self.maximum_x = 0

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
            gate_nrstart
            
        else:
            print(f"er staat al iets namelijk \"{self.grid[z][y][x]}\"")

    def gate_amount_count(self): # zit volgens mij al in code keenan

        amount=0

        for item in self.gate_dict:
            amount+=1
            item+=1

        #print(f"amount{amount}")

        return amount
    
    def add_wire (self, kortste_pad) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een wire, checkt ook of er niet al een gate is. 
        """
        # tests if shortest path is valid and filled
        if not kortste_pad:
            print("Er is geen pad teruggegeven door shortest_path!")
            return
        if len(kortste_pad) < 2:
            print("Het pad teruggegeven door shortest_path is te kort!")
        
        # Loop to put all coordinates from shortest path in grid!
        for coordinate in kortste_pad:
            y, x, z = coordinate

            # Checks if coordinates of path are not out of bounds 
            if not (0 <= z < len(self.grid) and 0 <= y < len(self.grid[0]) and 0 <= x < len(self.grid[0][0])):
                print(f"Error: Coordinates y={y}, x={x}, z={z} are out of bounds.")
                return

            # adds wire to grid 
            if self.grid[z][y][x] == 0:
                self.grid[z][y][x] = '+'
                print(f"wire toegevoegd op de coordinaten y={y}, x={x} z={z} ")

            # if there's a wire already than add one for 'kruizingen'/kortsluiting
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
                                x=int(row[2])
                                y=int(row[1])
                                z=0
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
                        y = int(row[1])
                        x = int(row[2])

                        max_y = max(max_y, y)
                        max_x = max(max_x, x)
                        
                    except ValueError:
                        print(f"Fout bij het verwerken van regel: {row}")
                        continue

            max_y = max_y + 1
            max_x = max_x + 1

            self.grid_edit.maximum_x = max_x
            self.grid_edit.maximum_y = max_y

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

class start:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

    def Auto_start_functie(self, user_path) ->None:
        """
        deels om te testen of het werkt maar je kan hier de grid opgeven, gates toevoegen en kijken wat de uitkomst is
        """
        user_input_obj = user_input(self.grid_edit)

        #geef eerst de maximaal breedte en hoogte y en x van de grid (hoogte standaard 3)
        
        max_y, max_x = user_input_obj.max_grid_values(user_path)
        print(max_x, max_y)
        self.grid_edit.grid_create(max_y, max_x) #maakt de grid met de opgegeven hoogte en breedt
        
        # user_path=input("geef de file path op: ")
        user_input_obj.load_gates(user_path)

class algorithm:
    def __init__(self, grid_edit_obj):
        self.grid_edit = grid_edit_obj

    def gate_nr(self):

        amount=0

        for item in self.grid_edit.gate_dict:
            amount+=1
            item+=1

        print(f"amount{amount}")

        return amount
    

    def check_valid(self, pos, end):
        y, x, z = pos
        # checks if the position is in the grid and if it is not already taken
        
        if 0 <= x < self.grid_edit.maximum_x and 0 <= y < self.grid_edit.maximum_y and 0 <= z < 7:
            if self.grid_edit.grid[z][y][x] == 0:
                return True
            elif pos == end:
                return True
            else:
                return False
        else:
            return False

    def shortest_path(self, gate_1, gate_2):
        # turns the gate numbers into their coordinates

        start = self.grid_edit.gate_dict[gate_1]
        end = self.grid_edit.gate_dict[gate_2]
        
        # sets up the heuristic
        def heuristic(a,b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

        # makes a priority list for the node
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        # a dict to keep track of the path traversed
        path_traversed = {}
        
        # a dict for the current cost for each node
        current_cost = {start: 0}
        counter = 0
        # loops until there are no nodes left
        while open_set:
            counter += 1

            
            # takes the lowest priority node out of the heap
            _, current = heapq.heappop(open_set)

            # stops if the current point is the end point
            if current == end:
                break
            
            neighbors = [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]

            # loops over the neighbors of the current point
            for dy, dx, dz in neighbors:
                neighbor = (current[0] + dy, current[1] + dx, current[2] + dz)

                # checks if the neighbor is inside the grid                
                if self.check_valid(neighbor, end) != True:
                    continue
                
                # cost for moving to the neighbor
                new_cost = current_cost[current] + 1

                if neighbor not in current_cost or new_cost < current_cost[neighbor]:
                    # updates costs to that of the neighbor
                    current_cost[neighbor] = new_cost

                    # calculates the priority, with current costs and the heuristic
                    priority = new_cost + heuristic(neighbor, end)

                    # adds neighbor to the prioritylist
                    heapq.heappush(open_set, (priority, neighbor))

                    # keeps track of the order
                    path_traversed[neighbor] = current
    
        # returns the path from start to end
        kortste_pad = self.reconstruct_path(path_traversed, start, current)

        #prints shortest path to terminal 
        print(kortste_pad)

        # counts wires and prints amount of wires 
        if kortste_pad:
            self.grid_edit.wirecount += len(kortste_pad) - 1
            print(f"Wirecount bijgewerkt: {self.grid_edit.wirecount}")
        
        # puts single wirepath in wirepaths_list 
        self.grid_edit.wirepaths_list.append(kortste_pad)

        #add wires of path to grid
        self.grid_edit.add_wire(kortste_pad)

        # returns shortest path (noodzakelijk voor add_wire functie)
        return kortste_pad

    def reconstruct_path(self, origin, start, end):
        # turns the gate numbers into their coordinates
        current = end
        path = []

        # we start looping from the back of the trail to the start
        while current != start:
            # appends to the pathlist
            path.append(current)
            
            # updates current
            current = origin[current]
        
        # adds the start point and reverses the list to go from start to end
        path.append(start)
        path.reverse()
        
        # returns the path
        return path

    def use_algorithm(self) ->None:
        #"self.grid_edit.addgate(5,6,1)" om een gate toe tevoegen
        #"self.grid_edit.addwire(5,6,1)" om een wire toe te voegen (z level is hier nodig)
        min_value=99999999

        #pak gate hoeveel heid
        
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
                    connect_gate, value = self.grid_edit.dichtstbij(current_gate, list_gates1) 
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
                connect_gate, value = self.grid_edit.dichtstbij(start_gate_r2, list_gates2) #list 2 omdat dit de tweede connectie wordt
                test_value+=value

                list_gates1.append(start_gate_r2)
                list_gates2.append(connect_gate)

            print(list_gates1)
            
            #maakt een connectie voor alle gates die niet voorkomen in list_gates1 en 2 (dus nog 1 connectie hebben)
            while current_gate>1:
                #skipt gates die al verbonden zijn voor de tweede keer
                if current_gate not in list_gates2:
                    #geeft een gate die nog niet verbonden is voor de tweede keer en de afstand (value) terug tot de opgegeven current_gate
                    connect_gate, value = self.grid_edit.dichtstbij(current_gate, list_gates2) 
                    
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
        path="gates.csv"

        grid_edit_obj = grid_edit()
        user_input_obj = user_input(grid_edit_obj)
        output_obj = output(grid_edit_obj)
        start_obj =start(grid_edit_obj)
        algorithm_obj=algorithm(grid_edit_obj)
            
        start_obj.Auto_start_functie(path)
        print("De uiteindelijke grid is:")
        output_obj.print_grid()
        algorithm_obj.shortest_path(1,2)
        algorithm_obj.shortest_path(2,3)
        algorithm_obj.shortest_path(3,4)
        algorithm_obj.shortest_path(4,5)
        algorithm_obj.shortest_path(5,1)
        print(algorithm_obj.use_algorithm())

        def write_to_csv(wirepaths_list):
            # Open het CSV-bestand in 'append' mode
            with open('wirepaths.csv', 'a', newline='') as csvfile:
                kolom = ['nummer', 'pad', 'succes', 'score', 'aantal_wires', 'aantal_kruizingen']
                writer = csv.DictWriter(csvfile, fieldnames=kolom)

                # Als het bestand leeg is, schrijf dan eerst de header (kolomnamen)
                csvfile.seek(0, 2)  # Ga naar het einde van het bestand
                if csvfile.tell() == 0:  # Als het bestand leeg is
                    writer.writeheader()

                # Genereer nummer voor de nieuwe rij
                with open('wirepaths.csv', 'r', newline='') as check_csvfile:
                    reader = csv.reader(check_csvfile)
                    rows = list(reader)
                    nummer = len(rows)  # Nummer is gelijk aan het aantal rijen, zodat het begint bij 1

                    # Dit zijn de andere gegevens die je wilt toevoegen. Pas deze aan op basis van je eigen logica.
                    data = {
                        'nummer': nummer,
                        'pad': str(wirepaths_list),  # Zet de wirepath om in een string
                        'succes': 'ja',  # Voorbeeld, pas aan volgens je logica succes als er geen overlapping is dus twee twee 
                        'score': 100,  # Voorbeeld
                        'aantal_wires': grid_edit_obj.wirecount,  # Aantal items in de wirepath
                        'aantal_kruizingen': grid_edit_obj.wirecrosscount  # Voorbeeld, pas aan volgens je logica
                    }

                    # Schrijf de rij naar het bestand
                    writer.writerow(data)
                    nummer += 1  # Verhoog het nummer voor de volgende rij

            print("CSV-bestand succesvol geschreven.")

        
        # Voeg de wirepaths toe aan de CSV
        write_to_csv(grid_edit_obj.wirepaths_list)
        output_obj.print_grid()

        print("CSV-bestand succesvol geschreven.")

        output_obj.costen_berekening()
        user_input_obj.score_request()

        output_obj.visualisatie()
    
    manual_check()

    """
    * in de code van keenan bevind gaat de row van max x en y ervan uit dat de numering van chips row 0 is maar row0 is in gates.
    csv de rij van y dus is in gates ook de numering toegevoegd

    * ik heb de wire count toegevoegd en werkend gemaakt. Deze werkt vanuit de functie shortest_path in de class algorithm
      de wire count wordt geinitieerd in grid edit init en wordt daar bijgehouden voor een heel netwerk

      ook wirecross count is werkend en loopt via add wire als een wire wordt gelegd om de plek van een + dan kruizen twee draden 
      en zal een cross worden neergelegd. 

    * Vanuit de functie shortest_path in de class algorithm wordt bij elke pad dat gevonden wordt de wirepaths_list in de 
      in de initializer van de grid edit bijgewerkt zodat elk pad als lijst wordt toegevoegd in de lijst wirepaths_list.

    * gate_amount_count kan volgens mij weg omdat deze functie al in de algorithm class van Keenan zit.

    * add_wire voegt nu bij elke iteratie van de functie shortest_path. ZO komt elke wire in het grid terecht weergegeven door '+'

    * nieuwe functie animatie zorgt voor de setup van de animatie in mathplotlib; visualisatie zorgt nu alleen nog voor de weergave

    * De animatie haalt de info voor de paden uit de wirepaths_list die in de __init__ is aangemaakt 
    Hieruit haalt de functie het pad van een netwerk als de visualisatie wordt aangeroepen. 
    
    * Er wordt een csv bestand aangemaakt in de ! working directory! waarbij ook wordt gekeken naar kruisingen
    er moet ook gekeken worden naar overlappingen en naar de score maar dat fix ik later. 

    **Wat ik nog ga doen**
    - rekening houden met kruisingen en overlappingen in visualisatie en in csv bestand 
   elke lijst vergeleken worden met alle lijsten of 2x dezelfde coordinaten voorkomen achter elkaar. je moet dus 2x checken 
    een x normaal en een x als je de lijst omdraait die wordt gecheckt. hoe dat moet naamvanlijst[::-1] of naamvanlijst.reverse()

    - voor een kruising kan je in de init een nieuwe list aanmaken die de coordinaten van een kruising bijhoudt en die wordt 
    vervolgens aangeroepen in de visualisatie om daar rood puntje van de maken. 

    - berekenen score
    """
