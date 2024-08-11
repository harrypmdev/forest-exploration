""" A module for the GameBoard class utilised in Forest Exploration. """

import math
import random
from utility import *
from area import Area
from enemy import Enemy
from game_state import GameState
from item import Item, HealthItem, Amulet
from game_error import GameError

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
    game_state: GameState -- the current game state

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
    
    def __init__(self, size: int, game_state: GameState) -> None:
        """
        Create a GameBoard object.
    
        Arguments:
        size: int -- the dimension size of the board.
        """
        tree, player = get_emojis(":evergreen_tree:", ":diamond_with_a_dot:")
        self.game_state = game_state
        self.size = size
        self.map = [[tree for y in range(size)] for x in range(size)]
        self.visited = []
        middle = (math.floor(size/2))
        self.current_location = Area(middle, middle, game_state, False)
        self.map[middle][middle] = player

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
        self.game_state.records["total moves"] += 1
        self._add_to_visited(self.current_location)
        self.game_state.update_amulet_generation_probability(self.size, len(self.visited))
        if fleeing:
            print(f"\nFled successfully! You travelled {direction.capitalize()}.")
        else:
            print(f"\nYou travelled {direction.capitalize()}.")
        if self._check_visited(*new_direction):
            self.current_location = self._get_visited_area(*new_direction)
        else:
            self.current_location = Area(*new_direction, self.game_state)
        self.map[self.current_location.y][self.current_location.x] = get_emojis(":diamond_with_a_dot:")[0]
        self.look()
        return False
            

    def look(self, line_break: bool = True) -> None:
        """ Print a description of the current area. """
        line_break = "\n" if line_break else ""
        print(f"{line_break}{self.current_location.get_description()}")
        if self.currently_in_battle():
            print("A hostile creature is present! You are in battle.\n")
    
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
        return False
