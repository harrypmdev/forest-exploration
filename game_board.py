""" A module for the GameBoard class utilised in Forest Exploration. """

import math
import random
from utility import *
from area import Area
from enemy import Enemy
from player import Player
from item import *

class GameBoard:
    """
    A class for the game board.

    Class Attributes:
    DIRECTIONS: dict -- A dictionary containing the directions the player
    can move, the axis it moves them on (0 for y, 1 for x) and the direction
    on the axis it moves them.

    Instance Attributes:
    size: int -- the dimension size of the board.
    map: list -- a two dimensional list that stores the map.
    visited: list -- a list of all visited areas.
    item_field: list -- a list of items that can be spawned in this game.
    current_location: Area -- the current area the player is in.
    amulet_generated: bool -- whether the amulet has been generated yet.
    records: dict -- a record of player achievements.

    Public Methods:
    currently_in_battle -- return True if currently in battle, False if not.
    print -- print the game map.
    introduce -- print a game introductory message.
    move -- move the player on the map.
    look - print a description of the current area.
    end_turn -- end the turn.
    flee -- attempt to 'flee' the player.
    """
    DIRECTIONS = {
        "north": (0, -1), 
        "east": (1, 1), 
        "south": (0, 1), 
        "west": (1, -1)
    }
    
    def __init__(self, size) -> None:
        """
        Create a GameBoard object.
    
        Arguments:
        size: int -- the dimension size of the board.
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

    def _add_to_visited(self, location: Area) -> None:
        """ 
        Check if a location is already on the visited list and add it if not.
        Update map for the visited area.
        
        Arguments:
        location: Area -- the new area that needs to be on the visited list.
        """
        if not self._check_visited(location.y, location.x):
            self.visited.append(location)
        if self.currently_in_battle():
            self.map[location.y][location.x] = get_emojis(":collision:")[0]  
        else:
            self.map[location.y][location.x] = get_emojis(":radio_button:")[0]   

    def _update_amulet_generation_probability(self) -> None:
        """ Update probability of amulet generating based on amount of areas visited. """
        for item in self.item_field:
            if item.name == "amulet":
                self.item_field[item] = int(not self.amulet_generated) * (1 / (self.size*self.size))  * len(self.visited)
    
    def _check_visited(self, y: int, x: int) -> bool:
        """ 
        Check if the player has visited an area at the given coordinates.

        Arguments:
        y: int -- the y coordinate to check.
        x: int -- the x coordinate to check.

        Returns True if it has been visited, False if not.
        """
        for area in self.visited:
            if area.y == y and area.x == x:
                return True
        return False
    
    def _get_visited_area(self, y: int, x: int) -> bool:
        """ 
        Return the area object for the given coordinates.
        Coordinates for a valid area that has already been visited
        must be provided.

        Arguments:
        y: int -- the y coordinate to retrieve
        x: int -- the x coordinate to retrieve

        Raises ValueError if passed invalid coordinates.

        Returns Area object for the coordinates in question.
        """
        for area in self.visited:
            if area.y == y and area.x == x:
                return area
        raise ValueError(f"Inappropriate coordinates provided: no area in visited list for coordinates y:{y}, x:{x}.")

    def currently_in_battle(self) -> bool:
        """ 
        Check if the player is currently in battle (hostile entities are present).
        Returns True if in battle, False if not.
        """
        for entity in self.current_location.entities:
            if type(entity) == Enemy and entity.alive:
                return True
        return False
    
    def print(self) -> None:
        """ Print the game board's map. """
        print("")
        for row in self.map:
            print(" ".join(row))
        print("")
    
    def introduce(self, player: Player) -> None:
        """ Print a game introductory message. """
        print("═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══\n"
              "Welcome to Forest Exploration!\n"
              f"Your game board has {self.size}x{self.size} dimensions.\n"
              f"Your player starts with {player.health} health.\n"
              "Enter 'tutorial' if it is your first time playing.\n"
              "═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══")

    def move(self, direction: str, fleeing: bool = False) -> bool:
        """
        Move in a specified direction on the game board's map.

        Arguments:
        direction: str -- the direction the player should move (north, east, south or west).
        fleeing: bool -- whether the player is currently fleeing (default False).

        Raises GameError if:
            The provided direction is invalid.
            An attempt to move while in battle is made but the player is not fleeing.
        
        Returns False
        """
        if direction not in self.DIRECTIONS.keys():
            raise GameError("\nThe 'go' command must be followed by: North, East, South or West.\n")
        if self.currently_in_battle() and not fleeing:
            raise GameError("\nCannot travel whilst in battle! Enter 'flee' to attempt to flee.\n")
        new_direction = [self.current_location.y, self.current_location.x]
        new_direction[self.DIRECTIONS[direction][0]] += self.DIRECTIONS[direction][1]
        if not (4 >= new_direction[0] >= 0 and 4 >= new_direction[1] >= 0):
            raise GameError("\nCannot move in this direction.\n")
        self.records["total moves"] += 1
        self._add_to_visited(self.current_location)
        self._update_amulet_generation_probability()
        if fleeing:
            print("Fled successfully!")
        print(f"\nYou travelled {direction.capitalize()}")
        if self._check_visited(*new_direction):
            self.current_location = self._get_visited_area(*new_direction)
        else:
            self.current_location = Area(*new_direction, self)
        self.map[self.current_location.y][self.current_location.x] = get_emojis(":diamond_with_a_dot:")[0]
        self.look()
        return False
            

    def look(self, line_break: bool = True) -> None:
        """ Print a description of the current area. """
        line_break = "\n" if line_break else ""
        print(f"{line_break}{self.current_location.get_description()}")
        if self.currently_in_battle():
            print("A hostile creature is present! You are in battle.\n")
    
    def end_turn(self, player: Player) -> None:
        """ Ends the turn, making all living enemies attack the player. """
        for entity in self.current_location.entities:
            if type(entity) == Enemy and entity.alive and player.alive:
                entity.attack(player)
    
    def flee(self) -> bool:
        """ 
        Attempt to 'flee' the player.

        Raises GameError is player is not in battle.

        Returns True.
        """
        if not self.currently_in_battle():
            raise GameError("\nCannot flee if not in battle! Move using 'go' command.\n")
        if random.random() > 0.3:
            try:
                self.move(random.choice(list(self.DIRECTIONS.keys())), True)
            except GameError:
                self.flee()
        else:
            print("\nFlee unsuccessful! You have not moved.\n")
        return True
