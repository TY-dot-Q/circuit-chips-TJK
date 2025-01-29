from code.classes import grid_edit
import csv, os
import heapq
import random
import time

random.seed(10)

class ManhattanDistance():
    def __init__(self, grid_edit_obj):
        self.grid_edit = grid_edit_obj

    def check_valid(self, pos: tuple[int], end: tuple[int]) -> bool:
        """
        Checks if the position in the grid is inside and not already taken
        
        Args:
            pos (tuple[int]): current position
            end (tuple[int]): end position
        
        Returns:
            bool: True if valid, False otherwise
        """
        y, x, z = pos
        
        # checks if the position is in the grid
        if 0 <= x <= self.grid_edit.maximum_x and 0 <= y <= self.grid_edit.maximum_y and 0 <= z <= 7:
            
            # checks if the position is empty or the end position
            if pos == end or self.grid_edit.grid[z][y][x] == 0:
                return True
        else:
            #print(f"position {pos} is occupied")
            return False

    def check_intersection(self, pos: tuple[int], neighbor: tuple[int]) -> bool:
        """
        Checks if the position of the neighbor in the grid is inside the grid
        and if an intersection can be made without making parallel lines
        
        Args:
            pos (tuple[int]): current position
            neighbor (tuple[int]): neighbors position 

        Returns:
            bool: True if wire can be made, False otherwise
        """
        y, x, z = neighbor
        
        # checks if the position is in the grid
        if 0 <= x <= self.grid_edit.maximum_x and 0 <= y <= self.grid_edit.maximum_y and 0 <= z <= 7:
            
            # else checks if the position is empty
            if self.grid_edit.grid[z][y][x] == '+': 
                return True
            else:
                return False
    
    def check_parallel(self, pos: tuple[int], neighbor: tuple[int])->bool:
        """
        Checks if moving to the neighboring position creates parallel wires

        Args:
            pos tuple[int]: current position
            neighbor tuple[int]: position of the neighbor

        Returns:
            bool: True if wires don't run parallel, False otherwise
        """
        
        y, x, z = neighbor
        
        # checks if the position is in the grid
        if 0 <= x <= self.grid_edit.maximum_x and 0 <= y <= self.grid_edit.maximum_y and 0 <= z <= 7:
            
            # checks if the the wire already is in the parallelset
            parallel_check = (pos, neighbor)
            if parallel_check not in self.grid_edit.parallel_set:
                return True
        else:
            return False
        
    
    def shortest_path(self, gate_1: int, gate_2: int) -> list[(tuple[int])]:
        """
        Finds the shortest path between two gates in the grid using A*
        and the Manhattan Distance as heuristic
        
        Args:
            gate_1 (int): number of the start gate
            gate_2 (int): number of the end gate
        
        Returns:
            kortste_pad (list[tuple[int]]): a list of coordinates of the traversed path
            from the start gate to the end gate
        """
        # turns the gate numbers into coordinates
        start = self.grid_edit.gate_dict[gate_1]
        end = self.grid_edit.gate_dict[gate_2]
        
        # sets up the heuristic
        def heuristic(a,b):
            """
            Manhattan Distance heuristic for the algorithm

            Args:
                a (tuple[int]): position of the first coordinate
                b (tuple[int]): position of the second coordinate

            Returns:
                int: a score value of how much it would cost to go from a to b in the grid
            """
            return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

        # makes a priority list for the algorithm
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        # a dict to keep track of the path traversed
        path_traversed = {}
        
        #
        intersection_check = False

        # a dict for the current cost for each node
        current_cost = {start: 0}
        
        # loops until there are no nodes left
        while open_set:
            # takes the lowest priority node out of the heap
            _, current = heapq.heappop(open_set)

            # stops if the current point is the end point
            if current == end:
                break
            
            # list of neighbor coordinates
            neighbors = [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]
            random.shuffle(neighbors)

            # loops over the neighbors of the current point
            for dy, dx, dz in neighbors:
                neighbor = (current[0] + dy, current[1] + dx, current[2] + dz)
                #print(f"Checking neighbor: {neighbor}")
                
                if not self.check_parallel(current, neighbor):
                    continue

                # checks if the neighbor is inside the grid                
                if self.check_valid(neighbor, end) != True:
                    #print(f"Neighbor {neighbor} is invalid")
                    intersection_check = True    

                    if self.check_intersection(current, neighbor) != True:
                        intersection_check = False
                        continue
                
                # cost for moving to the neighbor
                new_cost = current_cost[current] + 1
                if intersection_check:
                    new_cost += 5

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
        kortste_pad = self.reconstruct_path(path_traversed, start, current)

        #prints shortest path to terminal 
        print("")
        print(f"gate {gate_1} {self.grid_edit.gate_dict[gate_1]} en gate {gate_2} {self.grid_edit.gate_dict[gate_2]}")
        print(f"is het kortst (lengte:{len(kortste_pad)}) gevonden pad:")
        print(kortste_pad)
        print("")
        return kortste_pad

    def reconstruct_path(self, origin: dict[(tuple[int]), (tuple[int])], start: (tuple[int]), end: (tuple[int])) -> list[(tuple[int])]:
        """
        Reconstructs the path from end to start

        Args:
            origin dict[(tuple[int]), (tuple[int])]: a dict that keeps track of the path that the algorithm follows through the grid
            start (tuple[int]): the coordinates of the starting gate
            end (tuple[int]): the coordinates of the ending gate

        Returns:
            list [(tuple[int])]: a list of the path traversed from the start to the end
        """
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
    
    def netlist_looper(self, netlist: (tuple[int])) -> None:
        """
        Loops over the netlist and connects the gates with wires.

        Args:
            netlist list[(tuple[int])]: a list of the gate numbers that need to be connected
        
        Returns:
            None
        """
        # sets up the wirepathlist
        wirepaths_list=[]
        print(netlist)
        
        # loops over the items in the list
        for i in range(len(netlist)):
            gate_1 = netlist[i][0]
            gate_2 = netlist[i][1]
            
            # finds the shortest path between the gates
            path = self.shortest_path(gate_1, gate_2)
            
            # adds the wire in the grid
            self.grid_edit.add_wire(path)
            
            wirepaths_list.append(path)
            
            # adds the combination of coordinates to the parallel set to prevent parallel lines
            self.grid_edit.add_wire_parallel_set(path)

        self.grid_edit.wirepaths_list = wirepaths_list
        print("")
        print("complete wirepath list:")
        print(self.grid_edit.wirepaths_list)
        print("")

    def run(self, iterations):
        """
        Run the algorithm for the given amount of iterations
        """
