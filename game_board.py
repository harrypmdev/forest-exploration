import math
from utility import *
from area import Area

class GameBoard:

    def __init__(self, size):
        tree, player = get_emojis(":evergreen_tree:", ":diamond_with_a_dot:")
        self.size = size
        self.board = [[tree for x in range(size)] for y in range(size)]
        self.visited = []
        middle = (math.floor(size/2))
        self.current_location = Area(middle, middle)
        self.board[middle][middle] = player

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

    def add_to_visited(self, location):
        self.visited.append(location) 
        self.board[location.y][location.x] = get_emojis(":radio_button:")[0]
    
    def add_to_current_area_entities(self, entity):
        self.current_location.entities.append(entity)
    
    def get_current_area_entities(self):
        return self.current_location.entities

    def parse_move(self, move, player):
        if move == "map":
            self.print()
        elif move in ("N", "E", "S", "W"):
            self.move(move)
        else:
            return False
    
    def check_visited(self, y, x):
        for area in self.visited:
            if area.y == y and area.x == x:
                return True
        return False
    
    def get_visited_area(self, y, x):
        for area in self.visited:
            if area.y == y and area.x == x:
                return area
    
    def move(self, direction):
        new_x = self.current_location.x
        new_y = self.current_location.y
        if direction == "N":
            new_y = self.current_location.y - 1
        elif direction == "S":
            new_y = self.current_location.y + 1
        elif direction == "E":
            new_x = self.current_location.x + 1
        elif direction == "W":
            new_x = self.current_location.x - 1
        if 4 >= new_x >= 0 and 4 >= new_y >= 0:
            if not self.check_visited(new_y, new_x):
                self.add_to_visited(self.current_location)
                self.current_location = Area(new_y, new_x)
            else:
                self.current_location =self.get_visited_area(new_y, new_x)
                self.board[new_y][new_x] = get_emojis(":radio_button:")[0]
            self.board[self.current_location.y][self.current_location.x] = get_emojis(":diamond_with_a_dot:")[0]
            for location in self.visited:
                print(str(location.y), str(location.x))
        else:
            raise GameError("\nCannot move in this direction.\n")
        
