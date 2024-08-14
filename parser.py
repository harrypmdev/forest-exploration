"""A module for the Parser class utilised in Forest Exploration."""

import random

from effect import Effect
from entity import Entity
from player import Player
from utility import print_help, print_tutorial, print_key
from item import Item, HealthItem, Amulet
from game_board import GameBoard
from game_error import GameError
from game_state import GameState


class Parser:
    """
    A class for the parser, which interprets the players input during the game.

    Public Methods:
    parse_move: bool -- parse a raw move from the user
    """

    _ONE_WORD_MOVES = (
        "help",
        "tutorial",
        "inventory",
        "status",
        "quit",
        "look",
        "flee",
        "map",
        "key",
    )
    _TWO_WORD_MOVES = ("punch", "use", "describe", "go", "search", "drop", "take")
    _MOVES = _ONE_WORD_MOVES + _TWO_WORD_MOVES

    def __init__(self, player: Player, board: GameBoard, game_state: GameState) -> None:
        """
        Create a Parser object.

        Arguments:
        player: Player -- the player for which moves are being parsed.
        """
        self._player = player
        self._board = board
        self._game_state = game_state

    def parse_move(self, move: str) -> bool:
        """
        Parse raw move from the user.

        Arguments:
        move: str -- the move string the user inputted

        Raises GameError if move is invalid.

        Returns True if move passes turn in battle, returns False if not.
        """
        command, noun, noun_two = self._split_move(move.lower())
        score = self._game_state.records["score"]
        description = f"\n{self._board.current_location.get_description()}"
        # Dictionary of commands and their relevant subroutines and arguments
        MOVE_SUBROUTINES = {
            "help": (print_help, ()),
            "tutorial": (print_tutorial, ()),
            "key": (print_key, ()),
            "inventory": (self._player.print_inventory, ()),
            "status": (self._player.print_status, (score,)),
            "status of": (self._parse_status_of, (noun,)),
            "punch": (self._parse_punch, (noun,)),
            "use": (self._parse_use, (noun, self._player)),
            "use on": (self._parse_use_on, (noun, noun_two)),
            "describe": (self._parse_describe, (noun,)),
            "search": (self._parse_search, (noun,)),
            "take": (self._parse_take, (noun,)),
            "drop": (self._parse_drop, (noun,)),
            "go": (self._parse_go, (noun,)),
            "map": (self._board.print, ()),
            "flee": (self._board.flee, ()),
            "look": (print, (description,)),
            "quit": (exit, ()),
        }
        command_func, args = MOVE_SUBROUTINES[command]
        return command_func(*args)

    def _split_move(self, move: str) -> tuple[str, str, str]:
        # Take user input and split it into parts.
        if move == "":
            raise GameError("Please enter a command.\n")
        parts = move.strip().split(" ")
        command = parts[0].lower()
        if command not in self._MOVES:
            raise GameError(f"\n{command} is not a valid command! Try again.\n")
        if len(parts) == 1 and parts[0] in self._ONE_WORD_MOVES:
            return command, "", ""
        elif len(parts) == 2 and parts[0] in self._TWO_WORD_MOVES:
            return command, parts[1], ""
        elif len(parts) == 3 and parts[0] == "status" and parts[1] == "of":
            command = "status of"
            return command, parts[2], ""
        elif len(parts) == 4 and parts[0] == "use" and parts[2] == "on":
            command = "use on"
            return command, parts[1], parts[3]
        raise GameError(
            f"\n'{command}' does not work in this way!\n"
            "Enter 'tutorial' for tutorial or 'help '"
            "for valid moves list.\n"
        )

    def _parse_go(self, direction: str) -> bool:
        # Parse moves which use the 'go' command
        if self._board.current_location.in_battle():
            raise GameError(
                "\nCannot travel whilst in battle! "
                "Enter 'flee' to attempt to flee.\n"
            )
        return self._board.move(direction)

    def _parse_search(self, noun: str) -> bool:
        # Parse moves which use the 'search' command.
        for entity in self._board.current_location.entities:
            if entity.name == noun:
                if not entity.hostile:
                    raise GameError(
                        f"\nOnly enemies can be searched, {noun} is not an enemy.\n"
                    )
                if entity.alive:
                    raise GameError(
                        f"\n{entity.name.capitalize()} is alive!\n"
                        "Only dead creatures can be searched.\n"
                    )
                found_items = entity.search()
                self._player.inventory.extend(found_items)
                if not found_items:
                    print("\nNo items found.\n")
                    return False
                print("\nFound:")
                for item in found_items:
                    print(item.name)
                print("")
                return False
        raise GameError(f"\nNo enemy named {noun} in area.\n")

    def _parse_take(self, noun: str) -> bool:
        # Parse moves which use the 'take' command.
        for index, item in enumerate(self._board.current_location.items):
            if item.name == noun:
                self._player.inventory.append(
                    self._board.current_location.items.pop(index)
                )
                print(f"\nTook {item.name}!\n")
                return False
        raise GameError(f"\nNo item present called {noun}.\n")

    def _parse_drop(self, noun: str) -> bool:
        # Parse moves which use the 'drop' command.
        for index, item in enumerate(self._player.inventory):
            if item.name == noun:
                self._board.current_location.items.append(
                    self._player.inventory.pop(index)
                )
                print(f"\nDropped {item.name}.\n")
                return False
        raise GameError(f"\nNo item named {noun} in inventory.\n")

    def _parse_punch(self, noun: str) -> bool:
        # Parse moves which use the 'punch' command.
        for entity in self._board.current_location.entities:
            if entity.name == noun:
                damage = -random.randrange(1, 3)
                punch_attack = Effect("you used punch attack", damage)
                punch_message = entity.apply_effect(punch_attack)
                print(f"\n{punch_message}")
                if entity.hostile and not entity.alive:
                    self._game_state.update_kill_records()
                print("")
                return True
        raise GameError(f"\nNo entity called {noun} in area.\n")

    def _parse_status_of(self, noun: str) -> bool:
        # Parse moves which use the 'status of' command.
        for entity in self._board.current_location.entities:
            if entity.name == noun:
                entity.print_status()
                return False
        raise GameError(f"\nNo entity called {noun} in area.\n")

    def _parse_use(self, entered_item: str, target: Entity) -> bool:
        # Parse moves which use the 'use' command.
        for item in self._player.inventory:
            if item.name == entered_item and type(item) is HealthItem:
                self._parse_use_health_item(item, target)
                return True
            elif item.name == entered_item and type(item) is Amulet:
                self._parse_use_amulet_item(item)
                return False
        raise GameError(f"\nNo item named {entered_item} in inventory.\n")

    def _parse_use_health_item(self, item: Item, target: Entity):
        # Parse the 'use' command on HealthItems
        if item.target_item and target.name == "player":
            raise GameError("\nThis item must be targeted at a creature.\n")
        use_message = target.apply_effect(item.get_effect())
        print(f"\n{use_message}")
        if target.hostile and not target.alive:
            self._game_state.update_kill_records()
        if target.cured:
            self._game_state.update_score(10)
        if item.broken:
            self._player.inventory.remove(item)
            if not item.one_time_use:
                print(f"{item.name.capitalize()} broke!")
        print("")

    def _parse_use_amulet_item(self, item: Item):
        # Parse the 'use' command on Amulets
        item.activate()
        self._game_state.win(self._player.health)

    def _parse_use_on(self, noun: str, noun_two: str) -> bool:
        # Parse moves which use the 'use on' command.
        for entity in self._board.current_location.entities:
            if entity.name == noun_two:
                return self._parse_use(noun, entity)
        raise GameError(f"\nNo creature named {noun_two} in area.\n")

    def _parse_describe(self, noun: str) -> bool:
        # Parse moves which use the 'describe' command.
        for item in self._player.inventory:
            if item.name == noun:
                print(f"\n{item.description}\n")
                return False
        raise GameError(f"\nNo item named {noun} in inventory.\n")
