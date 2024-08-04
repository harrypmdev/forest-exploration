import math
import random
from utility import *
from area import Area
from enemy import Enemy

class GameBoard:

    def __init__(self, size):
        tree, player = get_emojis(":evergreen_tree:", ":diamond_with_a_dot:")
        self.size = size
        self.board = [[tree for x in range(size)] for y in range(size)]
        self.visited = []
        middle = (math.floor(size/2))
        self.current_location = Area(middle, middle, self, False)
        self.board[middle][middle] = player
        self.in_battle = False

    def print(self):
        print("\n")
        for row in self.board:
            print(" ".join(row))
        print("")
    
    def introduce(self, player):
        print("═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══\n"
              "Welcome to Forest Exploration!\n"
              f"Your game board has {self.size}x{self.size} dimensions.\n"
              f"Your player starts with {player.health} health.\n"
              "Enter N, E, S or W to travel North, East, South and West.\n"
              "Enter 'tutorial' if it is your first time playing.\n"
              "═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══")

    def add_to_visited(self, location):
        if not self.check_visited(location.y, location.x):
            self.visited.append(location) 
        self.board[location.y][location.x] = get_emojis(":radio_button:")[0]
    
    def add_to_current_area_entities(self, entity):
        self.current_location.entities.append(entity)
    
    def get_current_area_entities(self):
        return self.current_location.entities

    def parse_move(self, move, player):
        if move == "map":
            return self.print()
        elif move in ("n", "e", "s", "w"):
            return self.move(move)
        elif move == "look":
            return self.look()
        elif move == "flee":
            return self.flee()
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
    
    def move(self, direction, flee = False):
        if self.in_battle and not flee:
            print("\nCannot travel whilst in battle! Enter 'flee' to attempt to flee.\n")
            return False
        new_x = self.current_location.x
        new_y = self.current_location.y
        if direction == "n":
            new_y = self.current_location.y - 1
            travel_string = "\nYou travelled North."
        elif direction == "s":
            new_y = self.current_location.y + 1
            travel_string = "\nYou travelled South."
        elif direction == "e":
            new_x = self.current_location.x + 1
            travel_string = "\nYou travelled East."
        elif direction == "w":
            new_x = self.current_location.x - 1
            travel_string = "\nYou travelled West."
        if 4 >= new_x >= 0 and 4 >= new_y >= 0:
            print("Fled successfully!")
            print(travel_string)
            self.add_to_visited(self.current_location)
            if self.check_visited(new_y, new_x):
                self.current_location = self.get_visited_area(new_y, new_x)
            else:
                self.current_location = Area(new_y, new_x, self)
            self.board[self.current_location.y][self.current_location.x] = get_emojis(":diamond_with_a_dot:")[0]
            self.look()
            if self.currently_in_battle():
                print("A hostile creature is present! You are now in battle.\n")
        else:
            raise GameError("\nCannot move in this direction.\n")

    def look(self, line_break = True):
        line_break = "\n" if line_break else ""
        print(f"{line_break}{self.current_location.description}")
        if len(self.current_location.entities) == 0:
            print("There are no living creatures present except you.")
        elif len(self.current_location.entities) == 1:
            print(f"There is {self.current_location.entities[0].indefinite_name()}.")
        else:
            print("There are multiple creatures present:")
            for entity in self.current_location.entities:
                if not entity.alive:
                    print(f"A dead {entity.name}")
                else:
                    sick_string = " (it looks sick and weak)" if entity.sick == True else ""
                    hostile_string = " (hostile) " if type(entity) == Enemy else ""
                    print(f"{entity.name.capitalize()}{sick_string}{hostile_string}")
        print("")
    
    def end_turn(self, player):
        self.in_battle = self.currently_in_battle()
        for entity in self.current_location.entities:
            if type(entity) == Enemy and entity.alive:
                entity.attack(player)
        
    def currently_in_battle(self):
        for entity in self.current_location.entities:
            if type(entity) == Enemy and entity.alive:
                return True
        return False
    
    def flee(self):
        directions = ("n", "e", "s", "w")
        if random.random() > 0.55:
            try:
                self.move(random.choice(directions), True)
            except GameError:
                flee(self)
        else:
            print("Flee unsuccessful! You have not moved.\n")
        return True
