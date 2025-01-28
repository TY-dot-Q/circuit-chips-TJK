#import

gate_nrstart = 1

class grid_edit:
    grid=[]
    gate_dict={}
    wirepaths_list=[]
    gate_nr = gate_nrstart
    wirecross_list = [] 
    overlapping_lijst = []
    

    def __init__(self):
        """initaliseer de gridedit class"""
        self.wirecount=0
        self.wirecrosscount=0
        self.score=0
        self.maximum_y = 0
        self.maximum_x = 0
        self.nummer = 0 

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
        gebruik y, x en z coordinaten coordinaten. Dit wordt automatische gedaan met de functie in autostart
        """
        if not (0 <= z < len(self.grid) and 0 <= y < len(self.grid[0]) and 0 <= x < len(self.grid[0][0])):
            print(f"Error: Coordinates y={y}, x={x}, z={z} are out of bounds.")
            return
    
        if self.grid[z][y][x] ==0:
            self.grid[z][y][x] = self.gate_nr #voeg de gate toe
            self.gate_dict[self.gate_nr] = (y,x,z)
            print(f"gate met het nummer {self.gate_nr} toegevoegd op de coordinaten y={y}, x={x}, z={z} controle:{self.gate_dict[self.gate_nr]} ")
            self.gate_nr +=1
            gate_nrstart
            
        else:
            print(f"er staat al iets namelijk \"{self.grid[z][y][x]}\"")

        amount=0

        for item in self.gate_dict:
            amount+=1
            item+=1

        #print(f"amount{amount}")

        return amount

    def overlapping(self, wire1, wire2):
        """
        Controleert of wire1 en wire2 opeenvolgende coördinaten delen.
        """
        overlap_temp = []
        for i in range(len(wire1) - 1):
            check1 = wire1[i:i + 2]
            for j in range(len(wire2) - 1):
                check2 = wire2[j:j + 2]
                if check1 == check2 or check1 == list(reversed(check2)):
                    sorted_pair = sorted([check1[0], check1[1]])
                    if sorted_pair not in overlap_temp:
                        overlap_temp.append(sorted_pair)  # Voeg beide coördinaten van de overlap toe
        return overlap_temp

    def check_all_overlaps(self): # VOEG TOE
        """
        Controleer alle wires voor overlappen met elkaar en sla de overlappen op in overlapping_lijst.
        """
        overlaplijst = []
        for i, wire1 in enumerate(self.wirepaths_list):
            for wire2 in self.wirepaths_list[i+1:]:
                overlaps = self.overlapping(wire1, wire2)
                if overlaps:
                    overlaplijst.extend(overlaps)
        
        # Zorg ervoor dat elk paar coördinaten slechts één keer voorkomt, ongeacht de volgorde
        unieke_overlappingen = []
        
        for overlap in overlaplijst:
            # Uniekheid controleren zonder volgorde
            if overlap not in unieke_overlappingen and tuple(reversed(overlap)) not in unieke_overlappingen:
                unieke_overlappingen.append(overlap)
            
        # Update de lijst van overlappen
        self.overlapping_lijst = unieke_overlappingen

        # Controleer of er geen overlappen zijn
        if not self.overlapping_lijst:
            return "Ja"  # Geen overlappingen gevonden

        print(f"Overlappingen gevonden: {self.overlapping_lijst}")
        return "Nee"
    
    def find_wirecross(self): # VOEG TOE
        # Stap 1: Verzamel alle elementen behalve de eerste en laatste uit elke sublijst
        wirecross = []
        for sublist in self.wirepaths_list:
            if len(sublist) > 2:
                wirecross.extend(sublist[1:-1])  # Pak alles behalve eerste en laatste element

        # Stap 2: Houd alleen de waarden die exact twee keer voorkomen
        wirecross = [item for item in wirecross if wirecross.count(item) == 2]
        print(f"\n\n** voor eindde Wirecrosses gevonden: {wirecross}\n\n")

        # Stap 3: Haal alle (y, x, z)-waarden uit overlappingen_lijst
        overlapping_values = [item for sublist in self.overlapping_lijst for item in sublist]

        # Stap 4: Verwijder waarden uit wirecross die ook in overlapping_values voorkomen
        wirecross = [item for item in wirecross if item not in overlapping_values]

        # Stap 5: Return de uiteindelijke wirecross-lijst
        wirecross2 = []
        for item in wirecross:
            if item not in wirecross2:
                wirecross2.append(item)

        self.wirecross_list = wirecross2
        self.wirecrosscount = len(wirecross2)
        print(f"\n\n** na eindde Wirecrosses gevonden: {self.wirecross_list}") # haal weg
        print(f"Wirecrosscount: {self.wirecrosscount}\n\n") # haal weg

    
    def add_wire (self, kortste_pad) ->None: # VOEG TOE 
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
                self.grid[z][y][x] = '+' #voeg de wire toe
                print(f"wire toegevoegd op de coordinaten y={y}, x={x} z={z} ")
            elif self.grid[z][y][x]=="+":

                print(f"Over kruisend draad heen op de coördinaten y={y}, x={x}, z={z}")
       
            else:
                print(f"er staat al iets namelijk: \"{self.grid[z][y][x]}\"")

    # Voeg de wirecount toe aan de lijst
    def update_wirecount(self) -> int: # VOEG TOE
        """
        Telt het totale aantal coördinaten in alle wirepaths (j van alle i) 
        en trekt daar de lengte van i af (om de begin- en eindpunten van elke wirepath uit te sluiten).
        
        Returns:
            int: Het berekende wirecount.
        """
        total_count = 0

        # Tel het totale aantal coördinaten in alle wirepaths
        for wirepath in self.wirepaths_list:
            total_count += len(wirepath)

        # Trek het aantal wirepaths af van het totaal
        wirecount = total_count - len(self.wirepaths_list)

        # Debug-informatie
        print(f"Totaal aantal coördinaten: {total_count}") #haal weg
        print(f"Aantal wirepaths: {len(self.wirepaths_list)}") #haal weg 
        print(f"Wirecount: {wirecount}")

        return wirecount

    def gate_location(self, nr_check)->int:
        return self.gate_dict[nr_check]
    
    def remove_wire(self, y, x, z):
        """verwijdert een wire op een opgegeven locatie in de grid (neemt y, x, z in als input voor de coordinaten)"""
        if self.grid[z][y][x]=="+":
            self.grid[z][y][x]=0
            print(f"wire op locatie y{y}, x{x}, z{z} succesvol verwijdert")
        else:
            print(f"er is op locate y{y}, x{x}, z{z} geen wire gevonden.")
    
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
