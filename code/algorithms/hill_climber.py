import random
from code.classes.grid_edit import grid_edit
from code.algorithms.manhattan_distance import ManhattanDistance
import time
from datetime import datetime, timedelta

class hil_climber:
    #TODO
    #hou alle scores bij
    #hou alle laagste scores bij per iteratie

    """haalt een of meerdere wire verbinden tussen gates weg, en legt deze opnieuw met een bepaalde methode (zie reconstruct_ine)"""
    def __init__(self, grid_edit_obj):
        self.grid_edit = grid_edit_obj
        self.lowest_score=0
        self.netlist=[]

    def start_hill_climb(self, reset_amount, real_netlist, loop):
        """activeer om de hill climber te starten"""
        total_wirelist = self.grid_edit.wirepaths_list 
        self.netlist=real_netlist
        print(self.netlist) 
        print(reset_amount)


        if loop <=0:
            self.hill_climb(reset_amount, total_wirelist)
        else:
            self.lowest_score=self.grid_edit.score
            self.loop_climb(reset_amount, total_wirelist, loop)
        
    def reconstruct_line(self, chip_a, chip_b):
        """neemt een gegeven wire connection en legt deze opnieuw en gaat controleren of deze beter kan"""

        ManhattanDistance_obj=ManhattanDistance(self.grid_edit)

        #geef hier op welke manier je wilt gebruiken om de lijn opnieuw te leggen
        path = ManhattanDistance_obj.shortest_path(chip_a, chip_b)

        self.netlist.append((chip_a),(chip_b))
        self.grid_edit.add_wire(path)


    def remove_wire_connection(self, wireconnection):
        """verwijdert een complete lijn en verwijdert dit in de grid, verwacht nu van wire connection ((y,x,z), (y,x,z), etc)"""
        
        for i in range(len(wireconnection)):
            y = wireconnection[i][0]
            x = wireconnection[i][1]
            z = wireconnection[i][2]
            #print(self.grid_edit.grid[z][y][x])

            print(f"y={y}, x={x}, z={z}")
            self.grid_edit.remove_wire(y, x, z)

        print(wireconnection)
        self.grid_edit.remove_wire_parallel_set(wireconnection)

    def hill_climb(self, reset_amount, total_wirelist ):
        """reset_amount voor de hoeveelheid lijnen die je weg wilt halen, total_wirelist moet een list met alle lijnen die je hebt gelegt list, netlist moet de lijst zijn met de volgorde dat je draden hebt gelegt"""

        #seed zodat je dezelfde resultaten krijgt
        random.seed(31)

        oldwirelist=[]

        remakelist=[]
        i=0
        while i <= reset_amount:

            #pakt een random wire in de total_wirelist
            random_pick = random.randint(0, len(total_wirelist))
            wireconnection=total_wirelist[random_pick]
            oldwirelist.append(wireconnection)

            #zorgt dat de chips van de wirelist worden opgeslagen om later opnieuw te leggen
            remakelist.append(((self.netlist[random_pick][0]), (self.netlist[random_pick][1])))

            print(f"check(1){self.netlist[random_pick][0]}")
            print(f"check(2){self.netlist[random_pick][1]}")

            print(f"GROTE TEST KDLFHLSKD")
            print(f"netlist{self.netlist}")

            print (f"test zelfde lengte{len(self.netlist)} en {len(self.grid_edit.wirepaths_list)}")
            
            print(f"tussen gate {self.netlist[random_pick][0]} ({self.grid_edit.gate_dict[self.netlist[random_pick][0]]}) en  {self.netlist[random_pick][1]} ({self.grid_edit.gate_dict[self.netlist[random_pick][1]]}) --- wireconnection die gekozen is {wireconnection}")
            
            print(f"test remove{self.netlist[random_pick]}")
            print(f"random pick {random_pick}")
            self.netlist.pop(random_pick)

            #verwijder de complete wire lijn
            self.remove_wire_connection(wireconnection)
            i+=1

        print(f"test de remakelist:{remakelist}")
        #met de opgeslagen chips, maak de wire opnieuw
        i=0
        while i <= reset_amount:
            chip_a = remakelist[i][0]
            chip_b = remakelist[i][1]
            self.reconstruct_line(chip_a, chip_b)
            i+=1

        print(oldwirelist)
        return oldwirelist

    def reset_oude_grid(self, wirenet):
        """zet de oude grid weer terug in de huidige grid"""
        self.grid_edit.add_wire_parallel_set(wirenet)
        self.grid_edit.add_wire(wirenet)

    def remove_nieuw_wires(self, reset_amount):
        """haalt de nieuw gelgde wires weg"""
        
        remove_rate=len(self.netlist)

        while remove_rate > (len(self.netlist)-reset_amount):
            remove_wire=self.grid_edit.wirepaths_list[remove_rate]
            self.remove_wire_connection(remove_wire)
            remove_rate+=1


    def loop_climb(self, reset_amount, total_wirelist, loop):
        """loop over de hill_climb om meerdere keeren het aantal draden te verwijderen """
        start_tijd = datetime.now()
        eind_tijd=start_tijd+timedelta(minutes=loop)

        while datetime.now()<eind_tijd:
            print("de loop is nog nog bezig...")
            oldwirelist=self.hill_climb(reset_amount, total_wirelist)
            nieuwe_score=self.grid_edit.score

            if self.lowest_score>nieuwe_score:
                self.remove_nieuw_wires(reset_amount)
                self.reset_oude_grid(oldwirelist)
                #maak de oude grid weer aan als de score hoger is
            
            else:
                self.lowest_score=nieuwe_score
                #hou de nieuwe grid en reset de minimale score
