import random
from classes.grid_edit import grid_edit
from algorithms.manhattan_distance import ManhattanDistance

class hil_climber:
    """haalt een of meerdere wire verbinden tussen gates weg, en legt deze opnieuw met een bepaalde methode (zie reconstruct_ine)"""
    def __init__(self, grid_edit_obj):
        self.grid_edit = grid_edit_obj

    def reconstruct_line(self, chip_a, chip_b):
        """neemt een gegeven wire connection en legt deze opnieuw en gaat controleren of deze beter kan"""

        #geef hier op welke manier je wilt gebruiken om de lijn opnieuw te leggen
        ManhattanDistance.shortest_path(chip_a, chip_b)


    def remove_wire_connection(self, wireconnection):
        """verwijdert een complete lijn en verwijdert dit in de grid, verwacht nu van wire connection ((y,x,z), (y,x,z), etc)"""
        
        for i in range(len(wireconnection)):
            y = wireconnection[i][0]
            x = wireconnection[i][1]
            z = wireconnection[i][2]
            grid_edit.remove_wire(y,x,z)

    def loop_hill_climb(self, reset_amount, total_wirelist, netlist ):
        """reset_amount voor de hoeveelheid lijnen die je weg wilt halen, total_wirelist moet een list met alle lijnen die je hebt gelegt list, netlist moet de lijst zijn met de volgorde dat je draden hebt gelegt"""

        #seed zodat je dezelfde resultaten krijgt
        random.seed(31)

        remakelist=[]

        for i in reset_amount:

            #pakt een random wire in de total_wirelist
            random_pick = random.randomint(0, len(total_wirelist))
            wireconnection=total_wirelist[random_pick]

            #zorgt dat de chips van de wirelist worden opgeslagen om later opnieuw te leggen
            remakelist.append(netlist[random_pick][0])
            remakelist.append(netlist[random_pick][1])

            #verwijder de complete wire lijn
            self.remove_wire_connection(wireconnection)


        #met de opgeslagen chips, maak de wire opnieuw
        i=0
        for i in reset_amount:
            chip_a = remakelist[i][0]
            chip_b = remakelist[i][1]
            self.reconstruct_line(chip_a, chip_b)