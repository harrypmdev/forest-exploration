import math
import random
from utility import *
from area import Area
from enemy import Enemy
from item import *

class GameBoard:
    """
    A class for the game board.

    Class Attributes:
    DIRECTIONS: tuple -- A tuple containing the directions the player can move

    Instance Attributes:
    size: int -- the dimension size of the board
    map: list -- a two dimensional list that stores the map
    visited: list -- a list of all visited areas
    item_field: list -- a list of items that can be spawned in this game
    current_location: Area -- the current area the player is in
    amulet_generated: bool -- whether the amulet has been generated yet
    records: dict -- a record of player achievements

    Public Methods:
    currently_in_battle -- return True if currently in battle, False if not
    print -- print the game map
    introduce -- print a game introductory message
    move -- move the player on the map
    look - print a description of the current area
    end_turn -- end the turn
    flee -- attempt to 'flee' the player
    """
    DIRECTIONS = ("north", "east", "south", "west")
    
    def __init__(self, size):
        """
        Create a GameBoard object.
    
        Arguments:
        size: int -- the dimension size of the board
        """
        tree, player = get_emojis(":evergreen_tree:", ":diamond_with_a_dot:")
        self.size = size
        self.map = [[tree for y in range(size)] for x in range(size)]
        self.visited = []
        self.item_field = self._generate_items()
        middle = (math.floor(size/2))
        self.current_location = Area(middle, middle, self, False)
        self.map[middle][middle] = player
        self.amulet_generated = False
        self.records = {
            "total moves": 0,
            "kills": 0
        }
    
    def _generate_items(self) -> list:
        """ 
        Generate the list of items the can be spawned in this game. 
        Returns a dictionary of items and their generation probability.
        """
        items = {}
        items[HealthItem("potion", "A potion that heals 10 health.", 10)] = 0.05
        items[HealthItem("berries", "A tasty food. Heals 3 health.", 3)] = 0.05
        items[HealthItem("tomahawk", "A one-time use weapon that deals 7 damage.", -7, target_item=True)] = 0.1
        items[HealthItem("sword", "A sword that will last for a short while.", -4, 5, True)] = 0.05
        items[HealthItem("katana", "A super deadly sword that deals 10 damage.", -10, 7, True)] = 0.05
        items[HealthItem("axe", "A weak but durable weapon. Deals 3 damage.", -3, 15, True)] = 0.05
        items[Amulet("amulet", "Could it be... the amulet of power? There's only one way to find out.")] = 0
        return items

    def _add_to_visited(self, location: Area):
        """ Add an area to visited locations and update map. """
        if not self._check_visited(location.y, location.x):
            self.visited.append(location)
        if self.currently_in_battle():
            self.map[location.y][location.x] = get_emojis(":collision:")[0]  
        else:
            self.map[location.y][location.x] = get_emojis(":radio_button:")[0]   

    def _update_amulet_generation_probability(self):
        """ C """
        for item in self.item_field:
            if item.name == "amulet":
                self.item_field[item] = int(not self.amulet_generated) * (1 / (self.size*self.size))  * len(self.visited)
    
    def _check_visited(self, y, x):
        for area in self.visited:
            if area.y == y and area.x == x:
                return True
        return False
    
    def _get_visited_area(self, y, x):
        for area in self.visited:
            if area.y == y and area.x == x:
                return area

    def currently_in_battle(self):
        for entity in self.current_location.entities:
            if type(entity) == Enemy and entity.alive:
                return True
        return False
    
    def print(self):
        print("")
        for row in self.map:
            print(" ".join(row))
        print("")
    
    def introduce(self, player):
        print("═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══\n"
              "Welcome to Forest Exploration!\n"
              f"Your game board has {self.size}x{self.size} dimensions.\n"
              f"Your player starts with {player.health} health.\n"
              "Enter 'tutorial' if it is your first time playing.\n"
              "═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══")

    def move(self, direction, fleeing = False):
        if direction not in self.DIRECTIONS:
            raise GameError("\nThe 'go' command must be followed by: North, East, South or West.\n")
        if self.in_battle and not fleeing:
            print("\nCannot travel whilst in battle! Enter 'flee' to attempt to flee.\n")
            return False
        new_x = self.current_location.x
        new_y = self.current_location.y
        if direction == "north":
            new_y = self.current_location.y - 1
        elif direction == "south":
            new_y = self.current_location.y + 1
        elif direction == "east":
            new_x = self.current_location.x + 1
        elif direction == "west":
            new_x = self.current_location.x - 1
        travel_string = f"\nYou travelled {direction.capitalize()}"
        if 4 >= new_x >= 0 and 4 >= new_y >= 0:
            self._update_amulet_generation_probability()
            self.records["total moves"] += 1
            if fleeing:
                print("Fled successfully!")
            print(travel_string)
            self._add_to_visited(self.current_location)
            if self._check_visited(new_y, new_x):
                self.current_location = self._get_visited_area(new_y, new_x)
            else:
                self.current_location = Area(new_y, new_x, self)
            self.map[self.current_location.y][self.current_location.x] = get_emojis(":diamond_with_a_dot:")[0]
            self.look()
        else:
            raise GameError("\nCannot move in this direction.\n")

    def look(self, line_break = True):
        line_break = "\n" if line_break else ""
        print(f"{line_break}{self.current_location.get_description()}")
        if self.currently_in_battle():
            print("A hostile creature is present! You are in battle.\n")
    
    def end_turn(self, player):
        self.in_battle = self.currently_in_battle()
        for entity in self.current_location.entities:
            if type(entity) == Enemy and entity.alive and player.alive:
                entity.attack(player)
    
    def flee(self):
        if not self.in_battle:
            print("\nCannot flee if not in battle! Move using 'go' command.\n")
            return False
        if random.random() > 0.3:
            try:
                self.move(random.choice(self.DIRECTIONS), True)
            except GameError:
                self.flee()
        else:
            print("\nFlee unsuccessful! You have not moved.\n")
        return True
