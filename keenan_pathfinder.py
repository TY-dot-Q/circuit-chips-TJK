import heapq
# using heap since it stores the lowest value first in the list
# that is convenient for prioritizing the shortest dinstance

class Circuitrouter:
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

                if self.check_valid(neighbor) != True:
                    continue

                



        return 