import math
from utility import *

class GameBoard:

    def __init__(self, size):
        tree, player = get_emojis(":evergreen_tree:", ":diamond_with_a_dot:")
        self.size = size
        self.entities = []
        self.board = [[tree for x in range(size)] for y in range(size)]
        self.visited = []
        middle = (math.floor(size/2))
        self.current_location = (middle, middle)
        self.board[middle][middle] = player
        self.visited.append((middle, middle))

    def print(self):
        print("\n")
        for row in self.board:
            print(" ".join(row))
        print("\n")
    
    def introduce(self, player):
        print("═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══\n"
              "Welcome to Forest Exploration!\n"
              f"Your game board has {self.size}x{self.size} dimensions.\n"
              f"Your player starts with {player.health} health.\n"
              "Enter N, E, S or W to travel North, East, South and West.\n"
              "═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══")

    def add_to_visited(self,x, y):
        self.visited.append((x, y)) 
        self.board[x][y] = get_emojis(":radio_button:")[0]

    def parse_move(self, move, player):
        if move == "map":
            self.print()
        else:
            return False
