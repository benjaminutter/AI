#######################################################
#### MazeGame uses a grid of rows X cols to demonstrate
#### pathfinding using A*.
#### Benjamin Utter
#### AI, Spring 2024
#######################################################
import tkinter as tk
from queue import PriorityQueue

class Cell:
    def __init__(self, x, y, is_wall=False):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

class MazeGame:
    def __init__(self, root, maze):
        self.root = root
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.agent_pos = (0, 0)
        self.goal_pos = (self.rows - 1, self.cols - 1)
        self.cells = [[Cell(x, y, maze[x][y] == 1) for y in range(self.cols)] for x in range(self.rows)]
        self.cells[self.agent_pos[0]][self.agent_pos[1]].g = 0
        self.cells[self.agent_pos[0]][self.agent_pos[1]].h = self.heuristic(self.agent_pos)
        self.cells[self.agent_pos[0]][self.agent_pos[1]].f = self.heuristic(self.agent_pos)
        self.cell_size = 30
        # Create labels for algorithm titles
        self.label_astar = tk.Label(root, text="<- A* Algorithm", bg='black')
        self.label_astar.pack(side=tk.TOP)
        self.label_greedy = tk.Label(root, text="Greedy Best-First Algorithm ->", bg='black')
        self.label_greedy.pack(side=tk.TOP)
        # Create two canvas widgets for displaying paths
        self.canvas_astar = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas_greedy = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas_astar.pack(side=tk.LEFT)
        self.canvas_greedy.pack(side=tk.RIGHT)

        self.draw_maze(self.canvas_astar)
        self.draw_maze(self.canvas_greedy)

        self.find_path_a_star()
        self.find_path_greedy_best_first()

    def draw_maze(self, canvas):
        # Function to draw the maze on a given canvas
        for x in range(self.rows):
            for y in range(self.cols):
                color = 'maroon' if self.maze[x][y] == 1 else 'white'
                canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size, (x + 1) * self.cell_size, fill=color)

    def heuristic(self, pos):
        # Heuristic function to estimate the distance from a position to the goal
        return abs(pos[0] - self.goal_pos[0]) + abs(pos[1] - self.goal_pos[1])

    def find_path_a_star(self):
        # A* search algorithm to find the shortest path
        open_set = PriorityQueue()
        open_set.put((0, self.agent_pos))
        while not open_set.empty():
            current_cost, current_pos = open_set.get()
            current_cell = self.cells[current_pos[0]][current_pos[1]]
            if current_pos == self.goal_pos:
                self.reconstruct_path(current_cell, self.canvas_astar)
                break
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (current_pos[0] + dx, current_pos[1] + dy)
                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and not self.cells[new_pos[0]][new_pos[1]].is_wall:
                    new_g = current_cell.g + 1
                    if new_g < self.cells[new_pos[0]][new_pos[1]].g:
                        self.cells[new_pos[0]][new_pos[1]].g = new_g
                        self.cells[new_pos[0]][new_pos[1]].h = self.heuristic(new_pos)
                        self.cells[new_pos[0]][new_pos[1]].f = new_g + self.cells[new_pos[0]][new_pos[1]].h
                        self.cells[new_pos[0]][new_pos[1]].parent = current_cell
                        open_set.put((self.cells[new_pos[0]][new_pos[1]].f, new_pos))

    def find_path_greedy_best_first(self):
        # Greedy Best-First search algorithm to find the path
        open_set = PriorityQueue()
        open_set.put((0, self.agent_pos))
        while not open_set.empty():
            _, current_pos = open_set.get()
            current_cell = self.cells[current_pos[0]][current_pos[1]]
            print("Visiting:", current_pos)  # Add this line to print the position being visited
            if current_pos == self.goal_pos:
                self.reconstruct_path(current_cell, self.canvas_greedy)
                break
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (current_pos[0] + dx, current_pos[1] + dy)
                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and not self.cells[new_pos[0]][new_pos[1]].is_wall:
                    if not self.cells[new_pos[0]][new_pos[1]].parent:
                        self.cells[new_pos[0]][new_pos[1]].parent = current_cell
                        open_set.put((self.heuristic(new_pos), new_pos))

    def reconstruct_path(self, current_cell, canvas):
        # Function to reconstruct and draw the path on a canvas
        while current_cell.parent:
            x, y = current_cell.x, current_cell.y
            canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size, (x + 1) * self.cell_size, fill='green')
            current_cell = current_cell.parent
    
        # Ensure to draw the final cell of the path
        x, y = current_cell.x, current_cell.y
        canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size, (x + 1) * self.cell_size, fill='green')


# Define maze
maze1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]
# Create the main window
root = tk.Tk()
root.title("Maze")

# Create MazeGame instances for each maze and display them
game1 = MazeGame(root, maze1)

# Start the GUI event loop
root.mainloop()
