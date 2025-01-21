import csv, os
import matplotlib.pyplot as plt
import heapq
from mpl_toolkits.mplot3d import Axes3D


class grid_edit:
    

    def __init__(self, max_y, max_x):
        """initaliseer de gridedit class"""
        self.wirecount=0
        self.wirecrosscount=0
        self.score=0
        self.grid=[]
        self.gate_dict={}
        self.wire_list=[]
        self.gate_nr =1
        self.grid_create(max_y, max_x)

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
            grid_edit = self.grid_edit
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
        user_input_obj = user_input(self.grid_edit)

        #geef eerst de maximaal breedte en hoogte y en x van de grid (hoogte standaard 3)
        
        max_y, max_x = user_input_obj.max_grid_values(user_path)

        self.grid_edit.grid_create(max_y, max_x) #maakt de grid met de opgegeven hoogte en breedt
        
        # user_path=input("geef de file path op: ")
        user_input_obj.load_gates(user_path)

class algorithm:
    def __init__(self, grid_edit_obj):
        self.grid_edit = grid_edit_obj

    def heuristic(self, start, end):
        sy, sx, sz = start
        ey, ex, ez = end
        return abs(sy - ey) + abs(sx - ex) + abs(sz - ez)

    def check_valid(self, pos):
        # checks if the position is in the grid and if it is not already taken
        y, x, z = pos

        # Ensure the position is within the grid bounds
        if not (0 <= z < len(self.grid_edit.grid) and 
                0 <= y < len(self.grid_edit.grid[0]) and 
                0 <= x < len(self.grid_edit.grid[0][0])):
            return False

        # Ensure the position is not already occupied
        if self.grid_edit.grid[z][y][x] != 0:  # Assuming 0 means an empty cell
            return False

        return True
    
    def shortest_path(self, start, end):
        start = self.grid_edit.gate_location(start)
        end = self.grid_edit.gate_location(end)
        open_set = [(0, start)]
        origin = {}
        current_cost = {start: 0}
        estimated_cost = {start: self.heuristic(start, end)}
        closed_set = set()

        while open_set:

            # takes the lowest priority node out of the heap
            _, current = heapq.heappop(open_set)

            # stops if the current point is the end point
            if current == end:
                self.reconstruct_path(origin, current)
                return True

            # adds this node to the processed node list
            closed_set.add(current)
            
            # loops over the neighbors of the current point
            for dx, dy, dz in [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]:
                neighbor = (current[0] + dx, current[1] + dy, current[2] + dz)

                # checks if the neighbor is inside the grid
                if self.check_valid(neighbor) != True:
                    continue
                
                # cost for moving to the neighbor
                temp_current_cost = current_cost[current] + 1


                if neighbor not in current_cost or temp_current_cost < current_cost[neighbor]:
                    origin[neighbor] = current
                    
                    # updates costs to that of the neighbor
                    current_cost[neighbor] = temp_current_cost

                    # calculates the priority, with current costs and the heuristic
                    estimated_cost = temp_current_cost + self.heuristic(neighbor, end)
                    


                    # adds neighbor to the prioritylist
                    heapq.heappush(open_set, (estimated_cost, neighbor))
            
        return False
        
    def reconstruct_path(self, origin, current):
        while current in origin:
            y, x, z = current
            self.grid_edit.add_wire(y,x,z)
            current = origin[current]

    def connect_gates(self):
        # Haal alle gates op uit de gate_dict
        gates = list(self.grid_edit.gate_dict.values())
        if len(gates) < 2:
            print("Er zijn niet genoeg gates om verbindingen te maken.")
            return
        # Bereken verbindingen: elke gate verbinden met de twee dichtstbijzijnde buren
        connections = {}
        for i, gate in enumerate(gates):
            distances = sorted(
                ((self.heuristic(gate, other_gate), other_gate) for j, other_gate in enumerate(gates) if i != j)
            )
            connections[gate] = [distances[0][1], distances[1][1]]  # Twee dichtstbijzijnde gates

        # Leg verbindingen via wires
        for start, neighbors in connections.items():
            for neighbor in neighbors:
                if not self.shortest_path_path(start, neighbor):
                    print(f"Kan geen pad vinden tussen {start} en {neighbor}.")
    
class run_code:    
    def manual_check():
        grid_edit_obj = grid_edit(5,5)
        user_input_obj = user_input(grid_edit_obj)
        output_obj = output(grid_edit_obj)
        start_obj =start(grid_edit_obj)
        algorithm_obj=algorithm(grid_edit_obj)
        
        path="gates.csv"
            
        start_obj.Auto_start_functie(path)
        
        print("De uiteindelijke grid is:")
        #output_obj.print_grid()

        algorithm_obj.shortest_path(1,5)
        output_obj.costen_berekening()
        user_input_obj.score_request()

        output_obj.visualisatie()
    
    manual_check()
