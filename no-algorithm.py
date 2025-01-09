class grid_edit:
    def __init__(self):
        """initaliseer de gridedit class"""
        self.max_z=3
        self.grid=[]
        self.gate_dict={}
        self.gatenr =1
        self.wirecount=0
        self.wirecrosscount=0
        self.score=0

    def grid_create (self, max_y, max_x) -> None:
        """
        creeert een array 3d grid gebaseerde op de globale max_z en opgegeven max_y en x
        let op dit vervangt alle waardes niet runnen nadat gates zijn opgegeven.
        """
        self.grid = [[[0 for _ in range(max_x)] for _ in range(max_y)] for _ in range(self.max_z)]
        print("grid succesfol gemaakt")

    def add_gate (self, y, x) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een nummer 1,2,3 etc en je kan hiermee dus gates toevoegen.
        gebruik x en y coordinaten
        """
        if self.grid[1][y][x] ==0:
            self.grid[1][y][x] = self.gatenr #voeg de gate toe
            print(f"gate met het nummer {self.gatenr} toegevoegd op de coordinaten y={y}, x={x} ")
            self.gatenr +=1
            
            self.gate_dict[self.gatenr] = y,x
        else:
            print(f"er staat al iets namelijk \"{self.grid[1][y][x]}\"")
    
    def add_wire (self, y, x, z) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een wire, checkt ook of er niet al een gate is. 
        """
        if self.grid[z][y][x] ==0:
            self.grid[z][y][x] = "+" #voeg de wire toe
            print(f"wire toegevoegd op de coordinaten y={y}, x={x} z={z} ")
            self.wirecount+=1

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

class output:
    def __init__(self, grid_edit_obj):
        self.grid_edit=grid_edit_obj

    def print_grid (self) -> None:
        """
        print de huidig grid status met gates en verschillende lagen.
        """
        for z in range(self.gridedit.max_z):
            print(f"laag {z}")
            for row in self.gridedit.grid[z]:
                print(row) 
        print("klaar met printen")

    def costen_berekening(self)->int:
        """berekent de score van de geplaatste draden"""
        score = self.grid_edit.wirecount + 300 * self.grid_edit.wirecrosscount
        return score

class algorithm:
    #def addgatelist()->None:
        #gates toevoegen van de csv lijst
        

    def Start_functie() ->None:
        """
        deels om te testen of het werkt maar je kan hier de grid opgeven, gates toevoegen en kijken wat de uitkomst is
        """
        grid_edit_obj = grid_edit()
        user_input_obj = user_input(grid_edit_obj)
        output_obj = output(grid_edit_obj)

        #geef eerst de maximaal breedte en hoogte y en x van de grid (hoogte standaard 3)
        user_hoogte = int(input("geeft de maximaale verticale hoogte: 'y'"))
        max_y = user_hoogte #maak lijn hierboven commentaar en verander user_hoogte naar een waarde

        user_breedte = int(input("geeft de maximaale horizontale lengte: 'x'"))
        max_x = user_breedte #maak lijn hierboven commentaar en verander user_hoogte naar een waarde

        grid_edit_obj.gridcreate(max_y, max_x) #maakt de grid met de opgegeven hoogte en breedt

    #def algorithm() ->None:
        #"grid_edit_obj.addgate(5,6)" om een gate toe tevoegen (altijd laag 1)
        #"grid_edit_obj.addwire(5,6,1)" om een wire toe te voegen (z level is hier nodig)
        #""

    def manual_check():
        grid_edit_obj = grid_edit()
        user_input_obj = user_input(grid_edit_obj)
        output_obj = output(grid_edit_obj)

        user_hoogte = int(input("geeft de maximaale verticale hoogte: 'y'"))
        max_y = user_hoogte

        user_breedte = int(input("geeft de maximaale horizontale lengte: 'x'"))
        max_x = user_breedte 

        grid_edit_obj.gridcreate(max_y, max_x) 

        user_input_obj.add_gate_request()
        user_input_obj.add_wire_request()

        
        print("De uiteindelijke grid is:")
        output_obj.printgrid()

        grid_edit_obj.costenberekening()
        user_input_obj.scorerequest()

    manual_check()