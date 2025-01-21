import csv
import heapq
# using heap since it stores the lowest value first in the list
# that is convenient for prioritizing the shortest dinstance

class CircuitAlgorithm:
    def __init__(self, grid_size, netlist):
        self.grid_size = grid_size
        
        # a list of already placed wires
        self.netlist = netlist
        
        # sets up the grid
        self.grid = [[[None for _ in range(grid_size[2])]
                      for _ in range(grid_size[1])]
                      for _ in range(grid_size[0])]
        
        # to save paths
        self.paths = {}

    def check_valid(self, pos):
        x, y, z = pos

        # checks if the position is in the grid and if it is not already taken
        if 0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1] and 0 <= z < self.grid_size[2] and (self.grid[x][y][z] is None):
            return True
        else:
            return False
    
    
    def shortest_path(self, start: tuple, end: tuple):
        # calculates the shortest distance between 2 points
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
        
        # makes a priority list for the node
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        # a dict to keep track of the node
        origin = {}
        
        # a dict for the current cost for each node
        current_cost = {start: 0}
        
        # loops until there are no nodes left
        while open_set:
            # takes the lowest priority node out of the heap
            _, current = heapq.heappop(open_set)

            # stops if the current point is the end point
            if current == end:
                break
            
            # loops over the neighbors of the current point
            for dx, dy, dz in [(-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1)]:
                neighbor = (current[0] + dx, current[1] + dy, current[2] + dz)

                # checks if the neighbor is inside the grid
                if self.check_valid(neighbor) != True:
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
                    origin[neighbor] = current
        
        # returns the path from start to end
        return self.reconstruct_path(origin, start, end)
    
    def reconstruct_path(self, origin, start, end):
        current = end
        path = []

        # we start looping from the back to the start
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
    
    def path_placer(self, path, net_id):
        # loops over the coördinates in the path
        for x, y, z in path:
            
            # checks if the point in the grid is empty
            if self.grid[x][y][z] is None:
                # if empty 
                self.grid[x][y][z] = net_id
            
            else:
                # if not empty put down a cross for a crosspoint
                self.grid[x][y][z] = "X"
        
    def calculate_cost(self):
        n = sum(sum(sum(1 for cell in layer if cell is not None) for layer in row) for row in self.grid)
        k = sum(sum(sum(1 for cell in layer if cell == "X") for layer in row) for row in self.grid)
        return n + 300 * k
    
    def path_to_csv(self, path, filename):
        # opens file with given filename
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            # makes the header
            writer.writerow(['x', 'y' ,'z'])

            for x,y,z in path:
                writer.writerow([x, y ,z])


router = CircuitAlgorithm(grid_size=(5, 5, 2), netlist=[])
path = router.shortest_path((0, 0, 0), (3, 3, 0))
saved = router.path_to_csv(path, 'route.csv')
print(path)
