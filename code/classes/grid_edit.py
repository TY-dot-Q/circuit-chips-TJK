#import

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
        gebruik y, x en z coordinaten coordinaten. Dit wordt automatische gedaan met de functie in autostart
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

        amount=0

        for item in self.gate_dict:
            amount+=1
            item+=1

        #print(f"amount{amount}")

        return amount
    
    def add_wire (self, kortste_pad) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een wire,  
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
    
    def remove_wire(self, y, x, z):
        """verwijdert een wire op een opgegeven locatie (neemt y, x, z in als input)"""
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