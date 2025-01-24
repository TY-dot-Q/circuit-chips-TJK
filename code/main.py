from code.classes import grid_edit
#from code.algorithms import ...
from code.visualisation import visualisation as vis


if __name__ =="__main__":

    #path voor het laden van de csv nodes
    path ="C:\\Users\\tygob\\Documents\\GitHub\\circuit-chips-TJK\\code"

    #maximale waardes die voorkomen in het csv bestand
    max_y, max_x, max_z =grid_edit.user_input.max_grid_values(path)
    
    #maak een grid met die maximale waardes
    grid_edit.grid_edit.grid_create(max_y, max_x, max_z)

    #importeer de gates naar de gecreerde gates.
    grid_edit.user_input.load_gates(path)

    #pas het algortime toe


    #check of de uitkomst toepasbaar is


    #visualiseer de grid
    vis.visualisatie()
