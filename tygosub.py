grid =[]
gatenr=1
max_z = 3#layers

def gridcreate (max_y, max_x) -> None:
    global grid, max_z
    grid = [[[0 for _ in range(max_y)] for _ in range(max_x)] for _ in range(max_z)]
    print("grid succesfol gemaakt")

def printgrid () -> None:
    global grid
    global max_z
    for z in range(max_z):
        print(f"laag {z}")
        for row in grid[z]:
            print(row) 
    print("klaar met printen")

def addgate (x, y) ->None:
    global grid, gatenr

    grid[1][y][x] = gatenr #voeg de gate toe

    print(f"gate met het nummer {gatenr} toegevoegd op de coordinaten y={y}, x={x} ")
    gatenr=gatenr+1

def addgaterequest()->None:
    print("geef de cordinaten van de gates, typ: 'stop' wanneer je klaar bent")
    while True:
        user_coordinates = input("coordinaten bijv: 'x,y'")
        if user_coordinates.lower()=="stop":
            break
        
        try:
            y, x = map(int, user_coordinates.split(','))
            addgate(y,x)
        except ValueError:
            print("eroor: ongeldige invoer")

def _init_() ->None:
    #vraag de gates op, tot dat de user "stop" typt, dan maak de grid en print het met de functies hiervboven
    user_hoogte = int(input("geeft de maximaale verticale hoogte: 'y'"))
    max_y = user_hoogte

    user_breedte = int(input("geeft de maximaale horizontale lengte: 'x'"))
    max_x = user_breedte
    
    gridcreate(max_y, max_x)

    addgaterequest()

    print("de uiteindelijke grid is:")
    printgrid()

_init_()