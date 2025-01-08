grid =[]
gatenr=1
max_z = 3#layers

def gridcreate (max_y, max_x) -> None:
    """
    creeert een array 3d grid gebaseerde op de globale max_z en opgegeven max_y en x
    let op dit vervangt alle waardes niet runnen nadat gates zijn opgegeven.
    """
    global grid, max_z
    grid = [[[0 for _ in range(max_y)] for _ in range(max_x)] for _ in range(max_z)]
    print("grid succesfol gemaakt")

def printgrid () -> None:
    """
    print de huidig grid status met gates en verschillende lagen.
    """
    global grid
    global max_z
    for z in range(max_z):
        print(f"laag {z}")
        for row in grid[z]:
            print(row) 
    print("klaar met printen")

def addgate (y, x) ->None:
    """
    vervangt de 0 waarde van de gridcreate met een nummer 1,2,3 etc en je kan hiermee dus gates toevoegen.
    gebruik x en y coordinaten
    """
    global grid, gatenr

    grid[1][y][x] = gatenr #voeg de gate toe

    print(f"gate met het nummer {gatenr} toegevoegd op de coordinaten y={y}, x={x} ")
    gatenr=gatenr+1

def addwire (y, x, z) ->None:
    """
    vervangt de 0 waarde van de gridcreate met een wire, checkt ook of er niet al een gate is. 
    """
    global grid
    if grid[z][y][x] ==0:
        grid[z][y][x] = "+" #voeg de wire toe
        print(f"wire toegevoegd op de coordinaten y={y}, x={x} z={z} ")
    
    else:
        print(f"er staat al iets namelijk: \"{grid[z][y][x]}\"")

def addgaterequest()->None:
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
            addgate(y,x)
        except ValueError:
            print("eroor: ongeldige invoer")      

def addwirerequest()->None:
    """
    geeft een makkelijke manier om meerdere gates toe te voegen
    herhaalt de addgatefunctie totdat de user stop typ. de input is y,x coordinaten
    """
    print("geef de cordinaten van de wires, typ: 'stop' wanneer je klaar bent")
    while True:
        user_coordinates = input("coordinaten bijv: 'y,x,z'")
        if user_coordinates.lower()=="stop":
            break
        
        try:
            y, x, z = map(int, user_coordinates.split(','))
            addwire(y,x, z)
        except ValueError:
            print("eroor: ongeldige invoer")     


def _init_() ->None:
    """
    deels om te testen of het werkt maar je kan hier de grid opgeven, gates toevoegen en kijken wat de uitkomst is
    """
    #vraag de gates op, tot dat de user "stop" typt, dan maak de grid en print het met de functies hiervboven
    user_hoogte = int(input("geeft de maximaale verticale hoogte: 'y'"))
    max_y = user_hoogte

    user_breedte = int(input("geeft de maximaale horizontale lengte: 'x'"))
    max_x = user_breedte
    
    gridcreate(max_y, max_x)

    addgaterequest()
    addwirerequest()

    print("de uiteindelijke grid is:")
    printgrid()

_init_()