import random
from code.classes.grid_edit import grid_edit
from code.visualisation.visualisation import output
from code.algorithms.manhattan_distance import ManhattanDistance
import time
from datetime import datetime, timedelta


class hil_climber:
    #TODO
    #hou alle scores bij
    #hou alle laagste scores bij per iteratie


    #bug fixes

    """haalt een of meerdere wire verbinden tussen gates weg, en legt deze opnieuw met een bepaalde methode (zie reconstruct_ine)"""
    def __init__(self, grid_edit_obj):
        self.grid_edit = grid_edit_obj
        self.lowest_score=0
        self.netlist=[] #locale versie niet hetzelfde als in main of andere py bestanden
        self.reset_amount=5

        #testen (houdt bij wat de aanpassingen zijn die het maakt)
        self.first_length=-1
        
        self.remadelines=[]

    def start_hill_climb(self, reset_amount, real_netlist, loop):
        """activeer om de hill climber te starten"""
        print("")
        print("")
        print("-----------------START HILL CLIMBING PROCESS ---------------------------------------------------------------------")
        print("")
        
        self.grid_edit.wirepaths_list 
        self.netlist=real_netlist
        self.reset_amount=reset_amount
        
        
        #print(self.netlist) 
        #print(reset_amount)

        if loop <=0:
            self.hill_climb()
        else:
            self.update_score()
            self.lowest_score=self.grid_edit.score
            print(f"lowest_score{self.lowest_score}")
            self.loop_climb(loop)
        
    def reconstruct_line(self, chip_a, chip_b):
        """neemt een gegeven wire connection en legt deze opnieuw en gaat controleren of deze beter kan"""

        ManhattanDistance_obj=ManhattanDistance(self.grid_edit)

        #geef hier op welke manier je wilt gebruiken om de lijn opnieuw te leggen
        path = ManhattanDistance_obj.shortest_path(chip_a, chip_b)

        self.netlist.append((chip_a, chip_b))
        self.grid_edit.add_wire(path)
        self.grid_edit.add_wire_parallel_set(path)
        self.grid_edit.wirepaths_list.append
        print("")
        print(f"gate {chip_a} en {chip_b} ---- lengte netlist: {len(self.netlist)}")

    def remove_wire_connection(self, wireconnection):
        """verwijdert een complete lijn en verwijdert dit in de grid, verwacht nu van wire connection ((y,x,z), (y,x,z), etc)"""
        
        for i in range(len(wireconnection)):
            y = wireconnection[i][0]
            x = wireconnection[i][1]
            z = wireconnection[i][2]
            #print(self.grid_edit.grid[z][y][x])

            print(f"y={y}, x={x}, z={z}")
            self.grid_edit.remove_wire(y, x, z)

        self.grid_edit.remove_wire_parallel_set(wireconnection)

    def hill_climb(self, ):
        """reset_amount voor de hoeveelheid lijnen die je weg wilt halen, total_wirelist moet een list met alle lijnen die je hebt gelegt list, netlist moet de lijst zijn met de volgorde dat je draden hebt gelegt"""

        #seed zodat je dezelfde resultaten krijgt
        random.seed(31)

        oldwirelist=[]

        remakelist=[]
        i=0
        while i < self.reset_amount:

            #pakt een random wire in de total_wirelist
            random_pick = random.randint(0, len(self.grid_edit.wirepaths_list ))
            wireconnection=self.grid_edit.wirepaths_list [random_pick]
            oldwirelist.append(wireconnection)

            #zorgt dat de chips van de wirelist worden opgeslagen om later opnieuw te leggen
            remakelist.append(((self.netlist[random_pick][0]), (self.netlist[random_pick][1])))

            print("")
            print(f"TEST HILL_CLIMB LIJN VERWIJDERING NUMMER {i+1}---------------------------------------------------")
            #print(f"netlist{self.netlist}")
            print(f"random pick is: {random_pick}")
            print (f"netlist: {len(self.netlist)} -- wirepaths: {len(self.grid_edit.wirepaths_list)}")
            
            print(f"tussen gate {self.netlist[random_pick][0]} {self.grid_edit.gate_dict[self.netlist[random_pick][0]]} en  {self.netlist[random_pick][1]} {self.grid_edit.gate_dict[self.netlist[random_pick][1]]}")
            print(f"wire path heeft een lengte van ({len(wireconnection)})")
            print("")
            print(f"{wireconnection}")
            print("")

            self.netlist.pop(random_pick)

            #verwijder de complete wire lijn
            self.remove_wire_connection(wireconnection)
            i+=1

        print(f"test de remakelist:{remakelist}")

        print("")
        print("")
        
        #met de opgeslagen chips, maak de wire opnieuw
        i=0
        while i < self.reset_amount:
            print("")
            print("")
            print(f"REMAKE VAN DE LIJNEN {i+1}----------------------------------------------")
            chip_a = remakelist[i][0]
            chip_b = remakelist[i][1]
            self.reconstruct_line(chip_a, chip_b)
            i+=1

        print(oldwirelist)
        return oldwirelist, remakelist

    def reset_oude_grid(self, wirenet, netlist):
        """zet de oude grid weer terug in de huidige grid"""
        print(f"RESET OUDE GRID IS NU GEACTIVEERD LALALALALALLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLl")
        print(wirenet)
        print("")
        #fix de wirenet hier

        i=0
        while i < self.reset_amount:
            print(f"ronde nummer {i+1}")
            self.grid_edit.add_wire(wirenet[i])
            print(f"toevoegen van wirepath: {wirenet[i]}")

            self.grid_edit.add_wire_parallel_set(wirenet[i])
            print(f"toevoegen van wire_parrallel set: {wirenet[i]}")

            self.netlist.append(netlist[i])

            i+=1
            print("")

    def remove_nieuw_wires(self):
        """haalt de nieuw gelgde wires weg"""
        remove_rate=len(self.netlist)
        length_of_netlist = len(self.netlist)

        print(f"lengte van netlist")

        print("")
        print("verwijderen van nieuwe draden --------------------")

        while remove_rate > length_of_netlist-self.reset_amount:
            print(f"remove_rate: {remove_rate}")
            print(f"todat test: {length_of_netlist-self.reset_amount}")
            remove_number = remove_rate-1

            #check welke hij weghaalt, welke hij gates dat zijn en hoeveelste lijn dit moet zijn
            print(f"verwijderen van {remove_number} in de lijst  -- netlist:{self.netlist[remove_number]} -- {self.netlist[remove_number][0]} {self.grid_edit.gate_dict[self.netlist[remove_number][0]]}-- {self.netlist[remove_number][1]} {self.grid_edit.gate_dict[self.netlist[remove_number][1]]}")
            print(f"dit is het pad:")
            print(self.grid_edit.wirepaths_list[remove_number])
            print("")
            


            remove_wire=self.grid_edit.wirepaths_list[remove_number]
            self.remove_wire_connection(remove_wire)

            print(f"test welke netlist connectie wordt weg gehaald{self.netlist[remove_number]}")
            self.netlist.pop(remove_number)
            remove_rate-=1

        
        print("test hij komt uit de loop")

    def save_score(self):
        """houdt de score bij om een graph te kunnen maken"""

    def update_score(self):
        """update de wires en de cross manuely"""
        self.grid_edit.update_wirecount()
        self.grid_edit.find_wirecross()
        self.grid_edit.score = self.grid_edit.wirecount + (300 * self.grid_edit.wirecrosscount)

    def loop_climb(self, loop):
        """loop over de hill_climb om meerdere keeren het aantal draden te verwijderen """
        start_tijd = datetime.now()
        eind_tijd=start_tijd+timedelta(minutes=loop)

        loopcounter=0

        while datetime.now()<eind_tijd:
            print(f"de loop is nog nog bezig...({loopcounter})")
            print("")
            print("")
            oldwirelist, remakelist =self.hill_climb()
            
            self.update_score()
            print(self.grid_edit.wirecount, self.grid_edit.wirecrosscount)
            
            nieuwe_score=self.grid_edit.score
            print(f"de nieuwe score is:({nieuwe_score}) de oude score is:({self.lowest_score})")

            if self.lowest_score<nieuwe_score:
                print("dus de oude score wordt behouden")
                self.remove_nieuw_wires()
                self.reset_oude_grid(oldwirelist, remakelist)
                #maak de oude grid weer aan als de score hoger is
            
            else:
                print("dus de nieuwe score wordt behouden")
                self.lowest_score=nieuwe_score
                #hou de nieuwe grid en reset de minimale score
            loopcounter+=1
