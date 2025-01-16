import csv
import heapq
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Grid Edit Class ---
class grid_edit:
    def __init__(self):
        self.grid = []
        self.gate_dict = {}
        self.wire_list = []
        self.gate_nr = 1
        self.wirecount = 0
        self.wirecrosscount = 0

    def grid_create(self, max_y, max_x):
        self.grid = [[[0 for _ in range(max_x)] for _ in range(max_y)] for _ in range(7)]
        print("Grid succesvol gemaakt")

    def add_gate(self, y, x, z):
        if not (0 <= z < len(self.grid) and 0 <= y < len(self.grid[0]) and 0 <= x < len(self.grid[0][0])):
            print(f"Error: Coordinates y={y}, x={x}, z={z} are out of bounds.")
            return

        if self.grid[z][y][x] == 0:
            self.grid[z][y][x] = self.gate_nr
            self.gate_dict[self.gate_nr] = (y, x, z)
            print(f"Gate {self.gate_nr} toegevoegd op y={y}, x={x}, z={z}")
            self.gate_nr += 1
        else:
            print(f"Er staat al iets: \"{self.grid[z][y][x]}\"")

    def add_wire(self, path, net_id):
        for y, x, z in path:
            if self.grid[z][y][x] == 0:
                self.grid[z][y][x] = "+"
                self.wirecount += 1
                self.wire_list.append((y, x, z))
            elif self.grid[z][y][x] == "+":
                self.wirecrosscount += 1
                self.grid[z][y][x] = "X"

    def print_grid(self):
        for z, layer in enumerate(self.grid):
            print(f"Laag {z}")
            for row in layer:
                print(row)

# --- Circuit Algorithm Class ---
class CircuitAlgorithm:
    def __init__(self, grid_edit_obj):
        self.grid_edit = grid_edit_obj

    def check_valid(self, pos):
        y, x, z = pos
        grid = self.grid_edit.grid
        return (0 <= z < len(grid) and 0 <= y < len(grid[0]) and 0 <= x < len(grid[0][0]) and grid[z][y][x] == 0)

    def shortest_path(self, start, end):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

        open_set = []
        heapq.heappush(open_set, (0, start))
        origin = {}
        current_cost = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == end:
                break

            for dy, dx, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
                neighbor = (current[0] + dy, current[1] + dx, current[2] + dz)
                if not self.check_valid(neighbor):
                    continue

                new_cost = current_cost[current] + 1
                if neighbor not in current_cost or new_cost < current_cost[neighbor]:
                    current_cost[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, end)
                    heapq.heappush(open_set, (priority, neighbor))
                    origin[neighbor] = current

        return self.reconstruct_path(origin, start, end)

    def reconstruct_path(self, origin, start, end):
        current = end
        path = []
        while current != start:
            path.append(current)
            current = origin[current]
        path.append(start)
        path.reverse()
        return path

    def calculate_cost(self):
        grid = self.grid_edit.grid
        n = sum(sum(row.count("+") for row in layer) for layer in grid)
        k = sum(sum(row.count("X") for row in layer) for layer in grid)
        return n + 300 * k

# --- Testing the Integration ---
grid = grid_edit()
grid.grid_create(10, 10)
grid.add_gate(2, 2, 0)
grid.add_gate(7, 7, 0)

router = CircuitAlgorithm(grid)
start_gate = grid.gate_dict[1]
end_gate = grid.gate_dict[2]
path = router.shortest_path(start_gate, end_gate)
grid.add_wire(path, net_id=1)

print("\nGrid na plaatsen van de draad:")
grid.print_grid()
print(f"\nTotale kosten: {router.calculate_cost()}")
