import random
from code.classes.grid_edit import grid_edit
from code.visualisation.visualisation import output
from code.algorithms.crossless.mh_nc import mh_nc
import time
from datetime import datetime, timedelta

from code.classes.user_input import user_input
from code.visualisation.visualisation import output



class hil_climber_nc:
    #TODO
    #hou alle scores bij
    #hou alle laagste scores bij per iteratie


    #bug fixes
    #gebruik crl f om te zoeken waar de bug is
        #voor nu ziet het er naar uit dat de netlist en wirelist niet samenlopen en dat het wires koppelts aan netlist connecties die niet kloppen.

    """haalt een of meerdere wire verbinden tussen gates weg, en legt deze opnieuw met een bepaalde methode (zie reconstruct_ine)"""
    def __init__(self, grid_edit_obj):
        user_input_obj = user_input(grid_edit_obj)
        output_obj = output(grid_edit_obj)

        self.user_input = user_input_obj
        self.output=output_obj

        self.grid_edit = grid_edit_obj
        self.lowest_score=0
        self.netlist=[] #locale versie niet hetzelfde als in main of andere py bestanden
        self.reset_amount=5

        correct_gate_check=0
        self.seed=31

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
            self.manual_update()
            self.lowest_score=self.grid_edit.score
            print(f"lowest_score{self.lowest_score}")
            self.loop_climb(loop)
        
    def reconstruct_line(self, chip_a, chip_b):
        """neemt een gegeven wire connection en legt deze opnieuw en gaat controleren of deze beter kan"""

        ManhattanDistance_obj=mh_nc(self.grid_edit)

        #geef hier op welke manier je wilt gebruiken om de lijn opnieuw te leggen


        ##print(f"wirepaths_list{self.grid_edit.wirepaths_list}")
        ##print(f"lengte: {len(self.grid_edit.wirepaths_list)}")
        ##print("")
        path = ManhattanDistance_obj.shortest_path(chip_a, chip_b)

        self.netlist.append((chip_a, chip_b))
        self.grid_edit.add_wire(path)

        ##print("test76")
        ##print(len(self.grid_edit.wirepaths_list))
        self.grid_edit.wirepaths_list.append(path)
        ##print(len(self.grid_edit.wirepaths_list))
        ##print("")
        ##print(f"gate {chip_a} en {chip_b} ---- lengte netlist: {len(self.netlist)}")

    def remove_wire_connection(self, wireconnection, remove_number):
        """verwijdert een complete lijn en verwijdert dit in de grid, verwacht nu van wire connection ((y,x,z), (y,x,z), etc)"""
        
        for i in range(len(wireconnection)):
            y = wireconnection[i][0]
            x = wireconnection[i][1]
            z = wireconnection[i][2]
            #print(self.grid_edit.grid[z][y][x])

            ##print(f"y={y}, x={x}, z={z}")
            self.grid_edit.remove_wire(y, x, z)

        self.grid_edit.wirepaths_list.pop(remove_number)


    def hill_climb(self):
        """reset_amount voor de hoeveelheid lijnen die je weg wilt halen, total_wirelist moet een list met alle lijnen die je hebt gelegt list, netlist moet de lijst zijn met de volgorde dat je draden hebt gelegt"""

        #seed zodat je dezelfde resultaten krijgt
        
        random.seed(self.seed)
        print(self.seed)
        self.seed+=1

        oldwirelist=[]

        remakelist=[]
        i=0
        while i < self.reset_amount:
            #pakt een random wire in de total_wirelist
            ##print(len(self.grid_edit.wirepaths_list))
            
            random_pick = random.randint(0, len(self.grid_edit.wirepaths_list)-1)
            #print(self.grid_edit.wirepaths_list)
            wireconnection=self.grid_edit.wirepaths_list[random_pick]
            oldwirelist.append(wireconnection)
            #zorgt dat de chips van de wirelist worden opgeslagen om later opnieuw te leggen
            remakelist.append(((self.netlist[random_pick][0]), (self.netlist[random_pick][1])))

            ##print("")
            print(f"TEST HILL_CLIMB LIJN VERWIJDERING NUMMER {i+1}---------------------------------------------------")
            #print(f"netlist{self.netlist}")
            ##print(f"volledige lijn: {self.grid_edit.wirepaths_list}")

            print(f"random pick is: {random_pick}")
            print (f"netlist: {len(self.netlist)} -- wirepaths: {len(self.grid_edit.wirepaths_list)}")
            
            print(f"{i}tussen gate {self.netlist[random_pick][0]} {self.grid_edit.gate_dict[self.netlist[random_pick][0]]} en  {self.netlist[random_pick][1]} {self.grid_edit.gate_dict[self.netlist[random_pick][1]]}")
            ##print(f"wire path heeft een lengte van ({len(wireconnection)})")
            ##print("")
            ##print(f"{wireconnection}")
            ##print("")

            self.netlist.pop(random_pick)

            #verwijder de complete wire lijn
            self.remove_wire_connection(wireconnection, random_pick)

            i+=1

        ##print(f"test de remakelist:{remakelist}")
        ##print(f"old wire list: {oldwirelist}")

        ##print("")
        ##print("")
        
        #met de opgeslagen chips, maak de wire opnieuw
        i=0
        while i < self.reset_amount:
            ##print("")
            ##print("")
            ##print(f"REMAKE VAN DE LIJNEN {i+1}----------------------------------------------")
            chip_a = remakelist[i][0]
            chip_b = remakelist[i][1]
            
            ##print(chip_a, chip_b)
            self.reconstruct_line(chip_a, chip_b)
            i+=1

        ##print(oldwirelist)
        return oldwirelist, remakelist

    def reset_oude_grid(self, wirenet, oldnetlist):
        """zet de oude grid weer terug in de huidige grid"""
        ##print(f"RESET OUDE GRID IS NU GEACTIVEERD LALALALALALLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLl")
        ##print(wirenet)
        ##print("")
        #fix de wirenet hier

        ##print(len(self.netlist))
        ##print(len(self.grid_edit.wirepaths_list))
        
        i=0
        while i < self.reset_amount:
            ##print(f"ronde nummer {i+1}")
            self.grid_edit.add_wire(wirenet[i])
            ##print(f"toevoegen van wirepath: {wirenet[i]}")

            self.grid_edit.wirepaths_list.append(wirenet[i])

            self.netlist.append(oldnetlist[i])

            i+=1
            ##print("")

        ##print("test 44")
        
        ##print(len(self.netlist))
        ##print(self.netlist)
        
        ##print("")
        ##print(len(self.grid_edit.wirepaths_list))
        ##print(self.grid_edit.wirepaths_list)

    def remove_nieuw_wires(self):
        """haalt de nieuw gelgde wires weg"""
        ##print(self.netlist)
        remove_rate=len(self.netlist)
        length_of_netlist = len(self.netlist)

        ##print(f"lengte van netlist")
        ##print(len(self.netlist))

        ##print("")
        ##print("verwijderen van nieuwe draden --------------------")
        remove_number=0
        cycle_count=self.reset_amount

        while cycle_count>0:
            ##print("")
            remove_number = -1
            ##print(f"REMOVE OLD WIRE TO RESET GRID{cycle_count}-------------------------------------------------------------------------")
            ##print(f"remove_rate: {remove_rate}")
            ##print(f"todat test: {length_of_netlist-self.reset_amount}")
            ##print(f"lengte van de netlist {len(self.netlist)} lengte wirepathlist: {len(self.grid_edit.wirepaths_list)}")

            #check welke hij weghaalt, welke hij gates dat zijn en hoeveelste lijn dit moet zijn

            ##print(f"verwijderen van {remove_number} in de lijst  -- netlist:{self.netlist[remove_number]} -- {self.netlist[remove_number][0]} {self.grid_edit.gate_dict[self.netlist[remove_number][0]]}-- {self.netlist[remove_number][1]} {self.grid_edit.gate_dict[self.netlist[remove_number][1]]}")
            ##print(f"dit is het pad:")


            ##print(f"de wirelist{self.grid_edit.wirepaths_list[remove_number]}")
            ##print(f"de wirepathlist: {self.grid_edit.wirepaths_list}")
            ##print(f"de netlist die moet matchen: {self.netlist}")
            #print(f"test1{self.grid_edit.wirepaths_list[remove_number]}")
            #print(f"test2 met remove nummer {remove_number} geeft list {self.grid_edit.wirepaths_list[remove_number]}")
            
            ##print(self.grid_edit.wirepaths_list[remove_number])
            ##print("")

            remove_wire=self.grid_edit.wirepaths_list[remove_number] #verwijdert de path
            self.netlist.pop(remove_number)#verwijdert de connection
            
            self.remove_wire_connection(self.grid_edit.wirepaths_list[remove_number], remove_number)

            #for items in remove_wire:
                #print(remove_wire)
                #print(remove_wire[items])
                #self.remove_wire_connection(remove_wire[items])
                #print("test")

            ##print(f"remove wire teskt{remove_wire}")

            ##print(self.netlist)
            #print(f"test welke netlist connectie wordt weg gehaald{self.netlist[remove_number]}")
            ##print(remove_number)

            cycle_count-=1

        
        ##print("test hij komt uit de loop")

    def save_score(self):
        """houdt de score bij om een graph te kunnen maken"""

    def update_score(self):
        """update de wires en de cross manuely"""
        self.grid_edit.update_wirecount()
        self.grid_edit.find_wirecross()
        self.grid_edit.score = self.grid_edit.wirecount + (300 * self.grid_edit.wirecrosscount)

    def manual_update(self):
        """gebruikt update manier vanuit visualisation.py om de score te updaten"""
        wirecount = self.grid_edit.update_wirecount()
        self.grid_edit.find_wirecross() 

            # Compute cost and score
        self.output.costen_berekening(wirecount)
        match_wires = self.user_input.match_wirepaths_to_nets(self.netlist)
        self.output.write_to_csv(wirecount, "test_hill_climb")
        ##print(self.grid_edit.valide_counter, self.grid_edit.netlist_counter)

    def loop_climb(self, loop):
        """loop over de hill_climb om meerdere keeren het aantal draden te verwijderen """
        start_tijd = datetime.now()
        eind_tijd=start_tijd+timedelta(minutes=loop)

        valid_check=True
        invalid_count=0
        valid_count=0
        improvementcoun=0

        loopcounter=0

        while loopcounter<70: #datetime.now()<eind_tijd:
            print(f"de loop is nog nog bezig...({loopcounter})")
            print("")
            ##print("")
            oldwirelist, remakenetlist =self.hill_climb()
            
            self.manual_update()

            print(f"check 1 = {len(self.grid_edit.overlapping_lijst)} check 2 = {self.grid_edit.valide_counter} check 3 = {self.grid_edit.netlist_counter}")

            if (len(self.grid_edit.overlapping_lijst) == 0 and self.grid_edit.valide_counter == self.grid_edit.netlist_counter):
                valid_check=True #succes = ja
                valid_count+=1
            else:
                valid_check=True #succes = nee
                invalid_count+=1

            ##print(self.grid_edit.wirecount) 
            ##print(self.grid_edit.wirecrosscount)
            
            nieuwe_score=self.grid_edit.score
            ##print(f"de nieuwe score is:({nieuwe_score}) de oude score is:({self.lowest_score})")
            ##print(self.grid_edit.wirepaths_list)
            ##print("")
            ##print(self.netlist)

            print(f"lowest score check : {self.lowest_score} -- {nieuwe_score} -- {valid_check}")

            if self.lowest_score>=nieuwe_score and valid_check==True:
                print("dus de nieuwe score wordt behouden")
                self.lowest_score=nieuwe_score
                improvementcoun+=1
                #hou de nieuwe grid en reset de minimale score

            elif valid_check==1:
                print("dus de oude grid wordt terug gezet")
                print("remove_nieuw_wires")
                self.remove_nieuw_wires()

                print("reset_oude_grid")
                self.reset_oude_grid(oldwirelist, remakenetlist)
                #maak de oude grid weer aan als de score hoger is

            loopcounter+=1

        print(f"loop times = {loopcounter}")
        print(f"valid solutions={valid_count}")
        print(f"invalid solutions = {invalid_count}")
        print(f"keren dat een beter score gevonden is: {improvementcoun}")
        print(f"beste score={self.lowest_score}")
