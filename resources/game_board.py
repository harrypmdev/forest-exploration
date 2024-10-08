"""A module for the GameBoard class utilised in the Forest Exploration game."""

import random
import math

from resources.utility import get_emojis
from resources.area import Area
from resources.game_state import GameState
from resources.errors import GameError


class GameBoard:
    """A class for the game board.

    Public Instance Attributes:
    size: int -- the dimension size of the board.
    map: list -- a two dimensional list that stores the map.
    visited: list -- a list of all visited areas.
    current_location: Area -- the current area the player is in.

    Public Methods:
    print -- print the game map.
    move -- move the player on the map.
    flee -- attempt to 'flee' the player to a different location on the map.
    """

    _DIRECTIONS = {"north": (0, -1), "east": (1, 1), "south": (0, 1), "west": (1, -1)}

    def __init__(self, size: int, game_state: GameState) -> None:
        """Constructor for GameBoard class.

        Arguments:
        size: int -- the dimension size of the board.
        game_state: GameState -- the game state for this game.
        """
        tree, player = get_emojis("tree", "player")
        self.size = size
        self.map = [[tree for y in range(size)] for x in range(size)]
        self.visited = []
        middle = math.floor(size / 2)
        self.current_location = Area(middle, middle, hostiles=False)
        self.map[middle][middle] = player
        self._game_state = game_state

    def print(self) -> None:
        """Print the game board's map."""
        print("")
        for row in self.map:
            print(" ".join(row))
        print("")

    def move(self, direction: str, fleeing: bool = False) -> bool:
        """Move in a specified direction on the game board's map.

        Arguments:
        direction: str -- the direction the player should move
                          (north, east, south or west).
        fleeing: bool -- whether the player is currently fleeing
                        (default False).

        Raises GameError if the provided direction is invalid.

        Returns False.
        """
        if direction not in self._DIRECTIONS.keys():
            raise GameError(
                "\nThe 'go' command must be followed by: "
                "North, East, South or West.\n"
            )
        new_coordinates = self._get_next_coordinates(direction)
        if not self._move_is_on_map(new_coordinates):
            raise GameError("\nCannot move in this direction.\n")
        self._game_state.records["total moves"] += 1
        self._update_map(new_coordinates)
        self._game_state.update_amulet_gen(self.size, len(self.visited))
        if fleeing:
            print(f"\nFled successfully! You travelled {direction.capitalize()}.")
        else:
            print(f"\nYou travelled {direction.capitalize()}.")
        print(f"\n{self.current_location.get_description()}")
        return False

    def flee(self) -> bool:
        """Attempt to 'flee' the player.

        Raises GameError is player is not in battle.

        Returns True.
        """
        if not self.current_location.in_battle():
            raise GameError(
                "\nCannot flee if not in battle! Move using 'go' command.\n"
            )
        if random.random() > 0.3:
            try:
                self.move(random.choice(list(self._DIRECTIONS.keys())), True)
                return False
            except GameError:
                self.flee()
        else:
            print("\nFlee unsuccessful! You have not moved.\n")
        return True

    def _update_map(self, new_coordinates: list[int, int]) -> None:
        # Update the map emojis, visited list and current_location
        self._add_to_visited(self.current_location)
        self._update_visited_emoji_on_map(self.current_location)
        self._update_current_location(new_coordinates)
        self._update_player_emoji_on_map()

    def _add_to_visited(self, location: Area) -> None:
        # Check if a location is already on the visited list and then
        # add if it isn't and update map for the visited area.
        if not self._check_visited(location.y, location.x):
            self.visited.append(location)

    def _check_visited(self, y: int, x: int) -> bool:
        # Return True if the player has visited an area at the given coordinates.
        for area in self.visited:
            if area.y == y and area.x == x:
                return True
        return False

    def _get_visited_area(self, y: int, x: int) -> bool:
        # Return the Area object for the given coordinates.
        for area in self.visited:
            if area.y == y and area.x == x:
                return area
        raise ValueError(
            f"Inappropriate coordinates provided: no area in visited list for coordinates y:{y}, x:{x}."
        )

    def _update_visited_emoji_on_map(self, area: Area) -> None:
        # Update the previous location on map with visited or battle emoji
        if area.in_battle():
            self.map[area.y][area.x] = get_emojis("battle")[0]
        else:
            self.map[area.y][area.x] = get_emojis("visited")[0]

    def _update_player_emoji_on_map(self) -> None:
        # Update map current location with player emoji
        player_emoji = get_emojis("player")[0]
        y, x = self.current_location.y, self.current_location.x
        self.map[y][x] = player_emoji

    def _update_current_location(self, new_coordinates: list[int, int]) -> None:
        # Update the board's current location to either the Area that was
        # generated when the player was there before if it has been visited
        # before, or set it to a new Area instance for newly visited locations.
        if self._check_visited(*new_coordinates):
            self.current_location = self._get_visited_area(*new_coordinates)
        else:
            probability = self._game_state.amulet_probability
            self.current_location = Area(*new_coordinates, probability)
            self._check_for_amulet(self.current_location)

    def _check_for_amulet(self, area: Area) -> None:
        # Check an area for the amulet and update the game state if found
        if any(item.name == "amulet" for item in area.items):
            self._game_state.amulet_generated = True

    def _get_next_coordinates(self, direction: str) -> list[int, int]:
        # Finds the coordinates the player is moving into for a given direction.
        new_coordinates = [self.current_location.y, self.current_location.x]
        axis = self._DIRECTIONS[direction][0]
        movement = self._DIRECTIONS[direction][1]
        new_coordinates[axis] += movement
        return new_coordinates

    def _move_is_on_map(self, new_coordinates: list[int, int]) -> bool:
        # Return True if coordinates are on map, False if not.
        return (
            self.size > new_coordinates[0] >= 0 and self.size > new_coordinates[1] >= 0
        )
