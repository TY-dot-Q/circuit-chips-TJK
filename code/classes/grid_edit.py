#import

gate_nrstart = 1

class grid_edit:
    """
    Deze class is bedoeld om de grid te bewerken, gegevens bij te houden
    en te controleren op fouten.
    """

    def __init__(self):
        """
        initaliseer de gridedit class
        """
        self.wirecount=0
        self.wirecrosscount=0
        self.score=0
        self.maximum_y = 0
        self.maximum_x = 0
        self.nummer = 0
        self.grid=[]
        self.gate_dict={}
        self.wirepaths_list=[]
        self.gate_nr = gate_nrstart
        self.wirecross_list = [] 
        self.overlapping_lijst = []
        self.parallel_set = set()
        self.valide_counter = 0
        self.netlist_counter = 0
        self.histolijst_nc=[]

        self.wire_cross_count=[]

    def grid_create (self, max_y, max_x) -> None:
        """
        creeert een array 3D grid gebaseerde op de globale max_z en opgegeven max_y en x
        let op dit vervangt alle waardes niet runnen nadat gates zijn opgegeven.
        returnt niets
        """
        self.grid = [[[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)] for _ in range(8)]
        self.wire_crossing_count = [[[0 for _ in range(max_x+1)] for _ in range(max_y+1)] for _ in range(8)]
        print("grid succesvol gemaakt")

    def add_gate (self, y, x, z) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een nummer 1,2,3 etc en je kan hiermee dus gates toevoegen.
        gebruik y, x en z coordinaten coordinaten. Dit wordt automatische gedaan met de functie in autostart
        returnt het aantal gates
        """
        # Controleer of de opgegeven coördinaten binnen de grenzen van de grid vallen
        if not (0 <= z < len(self.grid) and 0 <= y < len(self.grid[0]) and 0 <= x < len(self.grid[0][0])):
            print(f"Error: Coordinates y={y}, x={x}, z={z} are out of bounds.")
            return

        # Voeg de gate toe aan de grid
        if self.grid[z][y][x] ==0:
            self.grid[z][y][x] = self.gate_nr #voeg de gate toe
            self.gate_dict[self.gate_nr] = (y,x,z) #voeg de coordinaten toe aan de gate_dict met de gate_nr als key
            print(f"gate met het nummer {self.gate_nr} toegevoegd op de coordinaten y={y}, x={x}, z={z} controle:{self.gate_dict[self.gate_nr]} ")
            self.gate_nr +=1
            gate_nrstart
            
        else:
            print(f"er staat al iets namelijk \"{self.grid[z][y][x]}\"")

        # tel aantal gates
        amount=0
        for item in self.gate_dict:
            amount+=1
            item+=1

        return amount

    def overlapping(self, wire1, wire2):
        """
        Controleert of wire1 en wire2 opeenvolgende coördinaten delen.
        Geeft deze overlappende coördinaten terug in een lijst.
        """
        overlap_temp = []
        # Loop door alle opeenvolgende coördinatenparen van beide wires
        for i in range(len(wire1) - 1):
            check1 = wire1[i:i + 2]
            # Controleer of de coördinatenparen van wire1 en wire2 overeenkomen
            for j in range(len(wire2) - 1):
                check2 = wire2[j:j + 2]
                # Voeg de overlappende coördinaten toe aan de lijst
                if check1 == check2 or check1 == list(reversed(check2)):
                    sorted_pair = sorted([check1[0], check1[1]])
                    
                    # Voeg alleen unieke coördinaten toe
                    if sorted_pair not in overlap_temp:
                        overlap_temp.append(sorted_pair)
        return overlap_temp

    def check_all_overlaps(self): 
        """
        Controleer alle wires voor overlappen met elkaar
        slaat de overlappen op in overlapping_lijst.
        """
        overlaplijst = []
        # Loop door alle combinaties van wirepaths
        for i, wire1 in enumerate(self.wirepaths_list):
            for wire2 in self.wirepaths_list[i+1:]:
                overlaps = self.overlapping(wire1, wire2)
                if overlaps:
                    overlaplijst.extend(overlaps)
        
        unieke_overlappingen = []
        # Loop door de lijst van overlappen
        for overlap in overlaplijst:
            # Uniekheid controleren zonder volgorde
            if overlap not in unieke_overlappingen and tuple(reversed(overlap)) not in unieke_overlappingen:
                unieke_overlappingen.append(overlap)
            
        # Update de lijst van overlappen
        self.overlapping_lijst = unieke_overlappingen
        print(f"Overlappingen gevonden: {self.overlapping_lijst}")
        
    
    def find_wirecross(self):
        """
        Zoekt de kruisingen van de wires en slaat deze op in wirecross_list.
        de functie geeft de wirecross_list terug direct in self.wirecross_list
        """
        # Maakt lijst van alle coördinaten behalve de eerste of laatste van een wirepath
        wirecross = []
        for sublist in self.wirepaths_list:
            if len(sublist) > 2:
                wirecross.extend(sublist[1:-1]) 

        # Houdt alleen de waarden die exact twee keer of drie keer voorkomen
        wirecross = [item for item in wirecross if wirecross.count(item) == 2 or wirecross.count(item) == 3]
        print(f"\n\n** voor einde Wirecrosses gevonden: {wirecross}\n\n")

        # Haalt alle (y, x, z) waarden uit overlappingen_lijst
        overlapping_values = [item for sublist in self.overlapping_lijst for item in sublist]

        # Verwijdert waarden uit wirecross die ook in overlapping_values voorkomen
        wirecross = [item for item in wirecross if item not in overlapping_values]

        # update de uiteindelijke wirecross-lijst
        wirecross2 = []
        for item in wirecross:
            if item in wirecross2:
                self.wirecrosscount += 1

            # Voegt alleen unieke waarden toe
            if item not in wirecross2:
                wirecross2.append(item)

        # Update de lijst van wirecrosses
        self.wirecross_list = wirecross2

    
    def add_wire (self, kortste_pad) ->None: 
        """
        vervangt de 0 waarde van de gridcreate met een wire.
        checkt ook of er niet al een gate is. 
        """
        # Check of er een kortste pad is
        if not kortste_pad:
            print("Er is geen pad teruggegeven door shortest_path!")
            return
        # Check of het kortste pad minimaal 2 coördinaten bevat
        if len(kortste_pad) < 2:
            print("Het pad teruggegeven door shortest_path is te kort!")
        
        # Loop door de coördinaten van het kortste pad
        for coordinate in kortste_pad:
            y, x, z = coordinate

            # Controleer of de opgegeven coördinaten binnen de grenzen van de grid vallen
            if not (0 <= z < len(self.grid) and 0 <= y < len(self.grid[0]) and 0 <= x < len(self.grid[0][0])):
                print(f"Error: Coordinates y={y}, x={x}, z={z} are out of bounds.")
                return

            # Voeg de wire toe aan de grid
            if self.grid[z][y][x] == 0:
                self.grid[z][y][x] = '+' 
                print(f"wire toegevoegd op de coordinaten y={y}, x={x} z={z} ")
                self.wire_crossing_count[z][y][x]= 1

            # Controleer of er al een wire ligt
            elif self.grid[z][y][x]=="+":
                print(f"Over kruisend draad heen op de coördinaten y={y}, x={x}, z={z}")
                self.wire_crossing_count[z][y][x]+=1
       
            else:
                print(f"er staat al iets namelijk: \"{self.grid[z][y][x]}\"")

    
    def update_wirecount(self) -> int:
        """
        Telt het totale aantal coördinaten in alle wirepaths (j van alle i) 
        en trekt daar de lengte van i af (om de begin- en eindpunten van elke wirepath uit te sluiten).
        Returns de berekende wirecount als integer.
        """
        total_count = 0

        # Tel het totale aantal coördinaten in alle wirepaths
        for wirepath in self.wirepaths_list:
            total_count += len(wirepath)

        # Trek het aantal wirepaths af van het totaal
        wirecount = total_count - len(self.wirepaths_list)

        return wirecount

    def gate_location(self, nr_check)->int:
        """
        geeft de coordinaten van een gate terug
        """
        return self.gate_dict[nr_check]
    
    def remove_wire(self, y, x, z):
        """
        verwijdert een wire op een opgegeven locatie in de grid 
        (neemt y, x, z in als input voor de coordinaten)
        """
        # Controleer of de opgegeven coördinaten binnen de grenzen van de grid vallen
        if self.grid[z][y][x]=="+":

            # Verwijder de wire van de grid
            if self.wire_cross_count!=1:
                self.grid[z][y][x]=0
                print(f"wire op locatie y{y}, x{x}, z{z} succesvol verwijdert")
            
            # Verlaag de wire_crossing_count
            else:
                self.wire_crossing_count[z][y][x]-=1
                print(f"wirecountverlaagt er staat dus nog steeds een draad")
        else:
            print(f"er is op locate y{y}, x{x}, z{z} geen wire gevonden.")
    
    def dichtstbij(self, gate_check, list_iligal_gates):
        """
        checkt wat de dichstbijzijnde gate is, geeft de gate terug en de afstand
        """
        # check of de gate bestaat
        if gate_check <=0:
            return -1, -1
        
        # ophalen coordinaten van de gate
        y,x,z = self.gate_dict[gate_check]
        gate_nr_teller = self.gate_amount_count()

        gate_return=0
        check_optimum=0
        # check of er genoeg gates zijn
        if gate_nr_teller<1:
            print("te weinig gates om dit uit te voeren")
            return -1, -1

        # test of de y,x en z waardes afstand samen groter is dan de vorige (in begin 0)
        while gate_nr_teller > 1:
            if gate_nr_teller!=gate_check & gate_nr_teller not in list_iligal_gates: 
                test_y, test_x, test_z = self.gate_dict[gate_nr_teller]
                v1 = abs(test_y - y)
                v2 = abs(test_x - x) 
                v3 = abs(test_z - z)
                
                # check of de afstand kleiner is dan de vorige
                if check_optimum>(v3+v2+v1):
                    check_optimum =v3+v2+v1
                    gate_return=gate_nr_teller

            gate_nr_teller -=1
        
        return gate_return, check_optimum

    def add_wire_parallel_set(self, wire: list[(tuple[int])])-> None:
        """
        voegt de coordinaten combinaties van een wire toe aan de parallel set.
        Args:
            wire: lijst van de coordinaten van wire
            in volgorde van de start gate naar de eind gate
        Returns:
            None
        """

        # Voeg de coordinaten combinaties van de wire toe aan de parallel set
        for i in range(len(wire) - 1):
            parallel = (wire[i], wire[i + 1])
            reverse_parallel = (wire[i + 1], wire[i])
            self.parallel_set.add(parallel)
            self.parallel_set.add(reverse_parallel)
    
    def remove_wire_parallel_set(self, wire: list[(tuple[int])])-> None:
        """
        removes the coordinate combinations of a wire to the parallel set

        Args:
            wire: a list of the coordinates of wire
            in order of the start gate to the end gate
        
        Returns:
            None
        """
        counter=0
        counter2=0
        for item in self.parallel_set:
            for i in item:
                counter2+=1

        print(f"aantal parrallel set coordinaten:{counter2}")

        for item in self.wirepaths_list:
            for i in item:
                counter+=1
        print(f"aantal wires:{counter}")    
        print("")
        

        for i in range(len(wire) - 1):
            parallel = (wire[i], wire[i + 1])
            reverse_parallel = (wire[i + 1], wire[i])
            self.parallel_set.remove(parallel)
            self.parallel_set.remove(reverse_parallel)
    
    def reset_grid(self):
        """
        Reset de grid en alle data voor nieuwe berekeningen tijdens volgende iteratie
        """
        # maak een nieuwe grid aan
        self.grid_create(self.maximum_y, self.maximum_x)

        self.gate_nr = gate_nrstart
        # Voeg de gates toe aan de grid
        for gate_nr, (y, x, z) in self.gate_dict.items():
            self.grid[z][y][x] = gate_nr  # Keep gate numbers in place
        
        # Reset data voor nieuwe berekeningen
        self.wirepaths_list = []
        self.parallel_set = set()
        self.wirecross_list = []
        self.overlapping_lijst = []
        self.wirecount = 0
        self.wirecrosscount = 0
        self.valide_counter = 0

        print("Grid reset! Gates remain, but all wires are removed.")
