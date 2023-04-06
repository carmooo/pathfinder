import heapq
import tkinter as tk
from collections import deque


class GridApp:
    def __init__(self, n=5, m=5):
        self.n = n
        self.m = m
        self.square_size = 30
        self.source_node = (0, 0)
        self.destination_node = (n - 1, m - 1)
        self.is_dragging_source = False
        self.is_dragging_destination = False
        self.square_colors = [['white' for _ in range(self.m)] for _ in range(self.n)]
        self.square_states = [[False for _ in range(self.m)] for _ in range(self.n)]
        self.path_squares = [[False for _ in range(self.m)] for _ in range(self.n)]

        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.n * self.square_size, height=self.m * self.square_size, bg='white')
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.on_square_click)
        self.canvas.bind('<B1-Motion>', self.on_square_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_square_release)

        self.draw_grid()

        self.btn = tk.Button(self.root, text='Find Shortest Path', command=self.find_shortest_path)
        self.btn.pack()

        # self.reset_btn = tk.Button(self.root, text='Reset', command=self.__init__(self.n, self.m))
        # self.reset_btn.pack()

        self.root.mainloop()

    def draw_grid(self):
        for i in range(self.n):
            for j in range(self.m):
                x1 = i * self.square_size
                y1 = j * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = 'blue' if self.square_states[i][j] else 'white'
                if self.path_squares[i][j]:
                    color = 'yellow'
                if (i, j) == self.source_node:
                    color = 'red'
                if (i, j) == self.destination_node:
                    color = 'green'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')

    def on_square_click(self, event):
        x = event.x // self.square_size
        y = event.y // self.square_size
        if (x, y) not in [self.source_node, self.destination_node]:  # Skip if clicked square is source or destination node
            self.square_states[x][y] = not self.square_states[x][y]
        else:
            if (x, y) == self.source_node:
                self.is_dragging_source = True
            else:
                self.is_dragging_destination = True
        self.canvas.delete('all')
        self.draw_grid()

    def on_square_drag(self, event):
        if self.is_dragging_source:
            x = event.x // self.square_size
            y = event.y // self.square_size
            if 0 <= x < self.n and 0 <= y < self.m and not self.square_states[x][y] and (x, y) != self.destination_node:
                self.source_node = (x, y)
        elif self.is_dragging_destination:
            x = event.x // self.square_size
            y = event.y // self.square_size
            if 0 <= x < self.n and 0 <= y < self.m and not self.square_states[x][y] and (x, y) != self.source_node:
                self.destination_node = (x, y)
        self.canvas.delete('all')
        self.draw_grid()

    def on_square_release(self, event):
        self.is_dragging_source = False
        self.is_dragging_destination = False

    def find_shortest_path(self):
        # Create a set to store visited nodes
        visited = set()
        # Create a dictionary to store the distance from the source node to each node
        distances = {self.source_node: 0}
        # Create a dictionary to store the parent node of each visited node
        parent = {}

        while True:
            # Find the node with the smallest distance that has not been visited
            min_dist = float('inf')
            min_node = None
            for i in range(self.n):
                for j in range(self.m):
                    node = (i, j)
                    if node not in visited and not self.square_states[i][j]:
                        if node in distances and distances[node] < min_dist:
                            min_dist = distances[node]
                            min_node = node

            if min_node is None:
                break

            visited.add(min_node)

            # Explore neighboring nodes
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = min_node[0] + dx, min_node[1] + dy

                # Skip nodes outside of the grid
                if 0 <= nx < self.n and 0 <= ny < self.m:
                    # Calculate the distance to the neighboring node
                    new_dist = distances[min_node] + 1

                    # Update the distance and parent of the neighboring node if it's a shorter path
                    if (nx, ny) not in distances or new_dist < distances[(nx, ny)]:
                        distances[(nx, ny)] = new_dist
                        parent[(nx, ny)] = min_node

        if self.destination_node in parent:
            # If destination is found, backtrack to find the path
            path = []
            node = self.destination_node
            while node != self.source_node:
                path.append(node)
                node = parent[node]
            path.reverse()

            # Update square colors to show the shortest path
            for node in path:
                self.path_squares[node[0]][node[1]] = True

            self.canvas.delete('all')
            self.draw_grid()
        else:
            print("No path found")


if __name__ == '__main__':
    n = 15  # Number of rows
    m = 22  # Number of columns
    app = GridApp(n, m)
