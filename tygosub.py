grid =[]
max_z = 3 #diepte oftewel de layers
max_y = 0 # verticale hoogte
max_x = 0 # horizontale lengte


def gridcreate (size) -> None:
    global grid
    rows, cols = size
    layers = 3
    grid = [[[0 for _ in range(cols)] for _ in range(rows)] for _ in range(layers)]

def printgrid (max_z, max_y, max_x) -> None:
    global grid
    for z in range(max_z):
        for y in range(max_y):
            for x in range(max_x):
                print(f"Value at grid[{z}][{y}][{x}] = {grid[z][y][x]}")

def addgate (x,y, gate_name) ->None:
    global grid 
    
    grid[1][y][x]= gate_name

    if y > max_y: #bepaald de grid hoogte en breedte
        max_y = y
    
    if x > max_x:
        max_x = x

    print(f"gate met de naam {gate_name} toegevoegd op de coordinaten y={y}, x={x} ")

def _init_() ->None:
    #vraag de gates op, tot dat de user "stop" typt, dan maak de grid en print het met de functies hiervboven
    global max_y, max_x
    print("geef de cordinaten van de gates, typ: 'stop' wanneer je klaar bent")

    