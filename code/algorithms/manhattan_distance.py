from code.classes import grid_edit
import csv, os
import heapq
import random

random.seed(0)

class ManhattanDistance():
    def __init__(self, grid_edit_obj):
        self.grid_edit = grid_edit_obj

    def check_valid(self, pos, end):
        """
        Checks if the position in the grid is inside and not already taken
        """
        y, x, z = pos
        
        # checks if the position is in the grid
        if 0 <= x < self.grid_edit.maximum_x and 0 <= y < self.grid_edit.maximum_y and 0 <= z < 7:
            # checks if the positions is the end position
            if pos == end:
                return True
            
            # else checks if the position is empty
            elif self.grid_edit.grid[z][y][x] == 0:
                return True        
        else:
            print(f"position {pos} is occupied")
            return False
    
    def shortest_path(self, gate_1, gate_2):
        """
        Finds the shortest path between two gates in the grid using A* and the Manhattan Distance as heuristic
        """
        # turns the gate numbers into coordinates
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
        
        # loops until there are no nodes left
        while open_set:
            # takes the lowest priority node out of the heap
            _, current = heapq.heappop(open_set)

            # stops if the current point is the end point
            if current == end:
                break
            
            # list of neighbor coordinates
            neighbors = random.shuffle([(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)])

            # loops over the neighbors of the current point
            for dy, dx, dz in neighbors:
                neighbor = (current[0] + dy, current[1] + dx, current[2] + dz)
                print(f"Checking neighbor: {neighbor}")

                # checks if the neighbor is inside the grid                
                if self.check_valid(neighbor, end) != True:
                    print(f"Neighbor {neighbor} is invalid")
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
        kortste_pad = self.reconstruct_path(path_traversed, start, current)

        #prints shortest path to terminal 
        print("")
        print(f"tussen gate {gate_1} en {gate_2}")
        print(f"gate {gate_1} {self.grid_edit.gate_dict[gate_1]} en gate {gate_2} {self.grid_edit.gate_dict[gate_2]}")
        print(f"is het kortst gevonden pad: {kortste_pad}")
        return kortste_pad

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
    
    def netlist_looper(self, netlist):
        """
        Loops over the netlist to connect the gates.
        """
        wirepaths_list=[]
        print(netlist)
        for i in range(len(netlist)):
            gate_1= netlist[i][0]
            gate_2= netlist[i][1]
            path = self.shortest_path(gate_1, gate_2)
            self.grid_edit.add_wire(path)
            wirepaths_list.append(path)
            
        self.grid_edit.wirepaths_list = wirepaths_list
        print("")
        print("complete wirepath list:")
        print(self.grid_edit.wirepaths_list)
        print("")

    def run(self, iterations):
        """
        Run the algorithm for the given amount of iterations
        """
