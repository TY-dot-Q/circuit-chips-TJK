class gridedit:
    def __init__(self, max_z):
        """initaliseer de gridedit class"""
        self.max_z=max_z
        self.grid=[]
        self.gatenr =1
        self.wirecount=0
        self.wirecrosscount=0
        self.score=0

    def gridcreate (self, max_y, max_x) -> None:
        """
        creeert een array 3d grid gebaseerde op de globale max_z en opgegeven max_y en x
        let op dit vervangt alle waardes niet runnen nadat gates zijn opgegeven.
        """
        self.grid = [[[0 for _ in range(max_x)] for _ in range(max_y)] for _ in range(self.max_z)]
        print("grid succesfol gemaakt")

    def addgate (self, y, x) ->None:
        """
        vervangt de 0 waarde van de gridcreate met een nummer 1,2,3 etc en je kan hiermee dus gates toevoegen.
        gebruik x en y coordinaten
        """
        if self.grid[1][y][x] ==0:
            self.grid[1][y][x] = self.gatenr #voeg de gate toe
            print(f"gate met het nummer {self.gatenr} toegevoegd op de coordinaten y={y}, x={x} ")
            self.gatenr +=1
        else:
            print(f"er staat al iets namelijk \"{self.grid[1][y][x]}\"")
    
    def addwire (self, y, x, z) ->None:
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

    def costenberekening(self)->None:
        """berekent de score van de geplaatste draden"""
        self.score = self.wirecount + 300 * self.wirecrosscount

class userinput:
    def __init__(self, gridedit_obj):
        self.gridedit=gridedit_obj

    def addgaterequest(self)->None:
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
                self.gridedit.addgate(y,x)
            except ValueError:
                print("eroor: ongeldige invoer")      

    def addwirerequest(self)->None:
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
                self.gridedit.addwire(y,x, z)
            except ValueError:
                print("eroor: ongeldige invoer")  
    
    def scorerequest(self)->None:
        print(f"er zijn {self.gridedit.wirecount} draaden")
        print(f"er zijn {self.gridedit.wirecrosscount} die overelkaar lopen")
        print(f"dit geeft een score van c={self.gridedit.score}")

class output:
    def __init__(self, gridedit_obj):
        self.gridedit=gridedit_obj

    def printgrid (self) -> None:
        """
        print de huidig grid status met gates en verschillende lagen.
        """
        for z in range(self.gridedit.max_z):
            print(f"laag {z}")
            for row in self.gridedit.grid[z]:
                print(row) 
        print("klaar met printen")



def Startfunctie() ->None:
    """
    deels om te testen of het werkt maar je kan hier de grid opgeven, gates toevoegen en kijken wat de uitkomst is
    """
    #vraag de gates op, tot dat de user "stop" typt, dan maak de grid en print het met de functies hiervboven
    user_hoogte = int(input("geeft de maximaale verticale hoogte: 'y'"))
    max_y = user_hoogte

    user_breedte = int(input("geeft de maximaale horizontale lengte: 'x'"))
    max_x = user_breedte
    
    gridedit_obj = gridedit(max_z=3)
    gridedit_obj.gridcreate(max_y, max_x)


    userinput_obj = userinput(gridedit_obj)
    userinput_obj.addgaterequest()
    userinput_obj.addwirerequest()

    output_obj = output(gridedit_obj)
    print("De uiteindelijke grid is:")
    output_obj.printgrid()

    gridedit_obj.costenberekening()
    userinput_obj.scorerequest()


Startfunctie()