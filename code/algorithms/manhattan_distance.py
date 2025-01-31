from code.classes import grid_edit
import heapq
import random
import time
import numpy as np

random.seed(time.time())

class ManhattanDistance():
    def __init__(self, grid_edit_obj):
        self.grid_edit = grid_edit_obj

    def check_valid(self, pos: tuple[int], end: tuple[int]) -> bool:
        """
        Controleert of de positie in het rooster binnen de grenzen valt en nog niet bezet is.

        Args
            pos (tuple[int]): huidige positie
            end (tuple[int]): eindpositie

        Returnt
            bool: True als de positie geldig is, anders False.
        """
        y, x, z = pos
        
        # checkt of positie niet buiten grid valt
        if 0 <= x <= self.grid_edit.maximum_x and 0 <= y <= self.grid_edit.maximum_y and 0 <= z <= 7:
            
            # checkt of positie leeg is of de eindpositie is
            if pos == end or self.grid_edit.grid[z][y][x] == 0:
                return True
        else:
            return False

    def check_intersection(self, pos: tuple[int], neighbor: tuple[int]) -> bool:
        """
        Controleert of de positie van de buur in het grid binnen de grenzen valt
        en of een kruising gemaakt kan worden zonder parallelle lijnen te vormen.
        Args:
            pos (tuple[int]): current position
            neighbor (tuple[int]): neighbors position 
        Returns:
            bool: True als draad kan worden gelegd, anders False
        """
        y, x, z = neighbor
        
        # checks of positie binnen grid valt
        if 0 <= x <= self.grid_edit.maximum_x and 0 <= y <= self.grid_edit.maximum_y and 0 <= z <= 7:
            
            # else checks of positie leeg is
            if self.grid_edit.grid[z][y][x] == '+': 
                return True
            else:
                return False
    
    def check_parallel(self, pos: tuple[int], neighbor: tuple[int])->bool:
        """
        Controleert of verplaatsen naar de buur positie parallelle draden creëert.
        Args
            pos (tuple[int]): huidige positie
            neighbor (tuple[int]): positie van de buur
        Returns
            bool: True als de draden niet parallel lopen, anders False.
        """
        # coordinaten van buren
        y, x, z = neighbor
        
        # checks of positie niet buiten grenzen van grid valt
        if 0 <= x <= self.grid_edit.maximum_x and 0 <= y <= self.grid_edit.maximum_y and 0 <= z <= 7:
            
            # check of draad niet al in parallel set staat
            parallel_check = (pos, neighbor)
            if parallel_check not in self.grid_edit.parallel_set:
                return True
        else:
            return False
        
    
    def shortest_path(self, gate_1: int, gate_2: int) -> list[(tuple[int])]:
        """
        Zoekt het kortste pad tussen twee poorten in het raster met behulp van A*
        en de Manhattan-afstand als heuristiek.
        Args
            gate_1 (int): nummer van de startpoort
            gate_2 (int): nummer van de eindpoort
        Returns
            kortste_pad (list[tuple[int]]): een lijst met coördinaten van het afgelegde pad
            van de startpoort naar de eindpoort.
        """
        # geeft gate coordinaten
        start = self.grid_edit.gate_dict[gate_1]
        end = self.grid_edit.gate_dict[gate_2]
        
        # set up voor de heuristic
        def heuristic(a,b):
            """
            Manhattan Distance heuristiek voor algoritme
            Args
                a (tuple[int]): positie van de eerste coördinaat
                b (tuple[int]): positie van de tweede coördinaat
            Returns
                int: een scorewaarde die aangeeft hoeveel het kost om van a naar b te gaan in het raster.
            """
            return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

        # maakt prioriteitenlijst voor algoritme
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        # Een dictionary om het gevolgde pad bij te houden
        path_traversed = {}
        
        #
        intersection_check = False

        # dict met kosten van huidige node 
        current_cost = {start: 0}
        
        # loopt tot geen node meer over is
        while open_set:
            # neemt laagste prioriteit uit heap
            _, current = heapq.heappop(open_set)

            # stops als eindpunt is bereikt
            if current == end:
                break
            
            # lijst coordinaten buren
            neighbors = [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]
            random.shuffle(neighbors)

            # loopt over buren van huidige coordinaat
            for dy, dx, dz in neighbors:
                neighbor = (current[0] + dy, current[1] + dx, current[2] + dz)
                
                if not self.check_parallel(current, neighbor):
                    continue

                # checkt of buur in grid zit              
                if self.check_valid(neighbor, end) != True:
                    intersection_check = True    

                    if self.check_intersection(current, neighbor) != True:
                        intersection_check = False
                        continue
                
                # kosten voor bewegen naar buren
                new_cost = current_cost[current] + 1
                

                # extra kosten kruising
                if intersection_check:
                    new_cost += 300

                
                if neighbor not in current_cost or new_cost < current_cost[neighbor]:
                    # updates kosten 
                    current_cost[neighbor] = new_cost

                    # bereken prioriteit met kosten en heuristiek
                    priority = new_cost + heuristic(neighbor, end)

                    # voegt buur toe aan prioriteitenlijst
                    heapq.heappush(open_set, (priority, neighbor))

                    # houdt volgorde bij
                    path_traversed[neighbor] = current

        # returnt pad van start tot eind
        kortste_pad = self.reconstruct_path(path_traversed, start, current)

        #print pad naar terminal
        print("")
        print(f"gate {gate_1} {self.grid_edit.gate_dict[gate_1]} en gate {gate_2} {self.grid_edit.gate_dict[gate_2]}")
        print(f"is het kortst (lengte:{len(kortste_pad)}) gevonden pad:")
        print(kortste_pad)
        print("")
        return kortste_pad

    def reconstruct_path(self, origin: dict[(tuple[int]), (tuple[int])], start: (tuple[int]), end: (tuple[int])) -> list[(tuple[int])]:
        """
        Reconstrueert het pad van eind naar begin
        Args
            origin (dict[(tuple[int]), (tuple[int])]): een dictionary die het pad bijhoudt dat het algoritme door het raster volgt
            start (tuple[int]): de coördinaten van de startpoort
            end (tuple[int]): de coördinaten van de eindpoort

        Returnt
            list [(tuple[int])]: een lijst met het gevolgde pad van start naar eind
        """
        current = end
        path = []

        # loop van eind spoor naar start
        while current != start:
            path.append(current)
            
            # update current
            current = origin[current]
        
        # voegt startpunt toe en maakt pad van start naar eind
        path.append(start)
        path.reverse()
        
        # returnt pad
        return path
    
    def netlist_looper(self, netlist: (tuple[int])) -> None:
        """
        Loopt door de netlijst en verbindt de poorten met draden.
        Args:
            netlist (list[(tuple[int])]): een lijst met de poortnummers die verbonden moeten worden
        Returns:
            None
        """

        wirepaths_list=[]
        
        # loopt over items in  list
        for i in range(len(netlist)):
            gate_1 = netlist[i][0]
            gate_2 = netlist[i][1]
            
            # korste pad tussen 2 gates
            path = self.shortest_path(gate_1, gate_2)
            
            # voegt draad toe in grid
            self.grid_edit.add_wire(path)
            
            wirepaths_list.append(path)
            
            # voegt parallele lijn toe om paralelle lijnen te voorkomen
            self.grid_edit.add_wire_parallel_set(path)

        self.grid_edit.wirepaths_list = wirepaths_list