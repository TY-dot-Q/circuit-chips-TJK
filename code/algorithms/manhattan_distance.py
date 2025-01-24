class algorithm:
    def __init__(self, grid_edit_obj):
        self.grid_edit = grid_edit_obj

    def gate_nr(self):

        amount=0

        for item in self.grid_edit.gate_dict:
            amount+=1
            item+=1

        print(f"amount{amount}")

        return amount
    

    def check_valid(self, pos, end):
        y, x, z = pos
        # checks if the position is in the grid and if it is not already taken
        
        if 0 <= x < self.grid_edit.maximum_x and 0 <= y < self.grid_edit.maximum_y and 0 <= z < 7:
            if self.grid_edit.grid[z][y][x] == 0:
                return True
            elif pos == end:
                return True
            else:
                return False
        else:
            return False

    def shortest_path(self, gate_1, gate_2):
        # turns the gate numbers into their coordinates

        start = self.grid_edit.gate_dict[gate_1]
        end = self.grid_edit.gate_dict[gate_2]
        
        # sets up the heuristic
        def heuristic(a,b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

        # makes a priority list for the node
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        # a dict to keep track of the path traversed
        path_traversed = {}
        
        # a dict for the current cost for each node
        current_cost = {start: 0}
        counter = 0
        # loops until there are no nodes left
        while open_set:
            counter += 1

            
            # takes the lowest priority node out of the heap
            _, current = heapq.heappop(open_set)

            # stops if the current point is the end point
            if current == end:
                break
            
            neighbors = [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]

            # loops over the neighbors of the current point
            for dy, dx, dz in neighbors:
                neighbor = (current[0] + dy, current[1] + dx, current[2] + dz)

                # checks if the neighbor is inside the grid                
                if self.check_valid(neighbor, end) != True:
                    continue
                
                # cost for moving to the neighbor
                new_cost = current_cost[current] + 1

                if neighbor not in current_cost or new_cost < current_cost[neighbor]:
                    # updates costs to that of the neighbor
                    current_cost[neighbor] = new_cost

                    # calculates the priority, with current costs and the heuristic
                    priority = new_cost + heuristic(neighbor, end)

                    # adds neighbor to the prioritylist
                    heapq.heappush(open_set, (priority, neighbor))

                    # keeps track of the order
                    path_traversed[neighbor] = current
    
        # returns the path from start to end
        print(self.reconstruct_path(path_traversed, start, current))
        return self.reconstruct_path(path_traversed, start, current)

    def reconstruct_path(self, origin, start, end):
        # turns the gate numbers into their coordinates
        current = end
        
        path = []

        # we start looping from the back of the trail to the start
        while current != start:
            # appends to the pathlist
            path.append(current)
            
            # updates current
            current = origin[current]
        
        # adds the start point and reverses the list to go from start to end
        path.append(start)
        path.reverse()
        
        # returns the path
        return path

    def use_algorithm(self) ->None:
        #"self.grid_edit.addgate(5,6,1)" om een gate toe tevoegen
        #"self.grid_edit.addwire(5,6,1)" om een wire toe te voegen (z level is hier nodig)
        min_value=99999999

        #pak gate hoeveel heid
        
        start_teller =self.gate_nr()
        
        start_gate_r2=0

        print(f"aantal gates moet nu 5 zijn:({start_teller})")
        #loop dat alle gate nummers overgaat om te checken wat het beste start punt is
        while start_teller>1:
            current_gate = start_teller
            test_value=0
            list_gates1=[]
            list_gates2=[]

            #eerste loop maakt paren van 2
            while current_gate>=1:
                #skipt gates die al verbonden zijn
                if current_gate not in list_gates1:
                    print(f"current gate{current_gate}:")
                    #geeft een gate die nog niet verbonden is en de afstand (value) terug tot de opgegeven current_gate
                    connect_gate, value = self.grid_edit.dichtstbij(current_gate, list_gates1) 
                    print(f"connect_gate: {connect_gate} -- value: {value}")

                    #-1, -1 wordt terug gegeven als er geen andere gate wordt gevonden
                    if connect_gate == -1 & value==-1:
                        start_gate_r2=current_gate
                        current_gate-=1
                        
                        continue
                        
                    #dubbel checkt of de connect_gate niet al in de lijst zit
                    elif connect_gate not in list_gates1:
                        #past de score aan
                        test_value+=value

                        #voegt de 2 gates die verbonden zijn aan de lijst zodat ze niet nog een keer gecontroleerd worden
                        list_gates1.append(connect_gate)
                        list_gates1.append(current_gate)
    
                current_gate-=1

            #gedeelte (2) koppel de gates nog 1 keer aan een andere

            current_gate=start_teller#reset de gate zodat hij weer alle langs kan
            
            #maak de eerste connectie van de overig gate als die er is
            if start_gate_r2!=-2:
                connect_gate, value = self.grid_edit.dichtstbij(start_gate_r2, list_gates2) #list 2 omdat dit de tweede connectie wordt
                test_value+=value

                list_gates1.append(start_gate_r2)
                list_gates2.append(connect_gate)

            print(list_gates1)
            
            #maakt een connectie voor alle gates die niet voorkomen in list_gates1 en 2 (dus nog 1 connectie hebben)
            while current_gate>1:
                #skipt gates die al verbonden zijn voor de tweede keer
                if current_gate not in list_gates2:
                    #geeft een gate die nog niet verbonden is voor de tweede keer en de afstand (value) terug tot de opgegeven current_gate
                    connect_gate, value = self.grid_edit.dichtstbij(current_gate, list_gates2) 
                    
                    #-1, -1 wordt terug gegeven als er geen andere gate wordt gevonden
                    if connect_gate == -1 & value==-1:
                        start_gate_r2=current_gate
                        current_gate-=1
                        
                        continue
                        
                    #dubbel checkt of de connect_gate niet al in de lijst zit
                    elif connect_gate not in list_gates2:
                        #past de score aan
                        test_value+=value

                        #voegt de 2 gates die verbonden zijn aan de lijst zodat ze niet nog een keer gecontroleerd worden
                        list_gates2.append(connect_gate)
                        list_gates2.append(current_gate)
    
                current_gate-=1

            #zet de test_value naar min_value als de score lager is (hoop is dat dit dan de laagste waarde geeft en dus de beste score)
            print(f"test_value===={test_value}")
            if test_value<min_value:
                min_value=test_value

            start_teller-=1

        return min_value #min_value
