""" A module for the Parser class utilised in Forest Exploration. """

import random
import emoji
from effect import Effect
from entity import Entity
from player import Player
from enemy import Enemy
from utility import *
from game_board import GameBoard
from game_error import GameError
from game_state import GameState

class Parser:
    """
    A class for the parser, which interprets the players input during the game.

    Class Attributes:
    VALID_MOVES: tuple -- a tuple of all valid moves the player can input.

    Instance Attributes:
    player: Player -- the player for which moves are being parsed.
    board: GameBoard -- the board the player is on

    Public Methods:
    parse_move -- parse a raw move from the user
    """
    _ONE_WORD_MOVES = (
        "help", "tutorial", "inventory", 
        "status", "quit", "look",
        "flee", "map"
    )
    _TWO_WORD_MOVES = (
        "punch", "use", "describe",
        "go", "search", "drop", "take"
    )
    _MOVES = _ONE_WORD_MOVES + _TWO_WORD_MOVES

    def __init__(self, player: Player, board: GameBoard, game_state: GameState) -> None:
        """
        Create a Parser object.
    
        Arguments:
        player: Player -- the player for which moves are being parsed.
        """
        self.player = player
        self.board = board
        self.game_state = game_state

    def parse_move(self, move: str) -> bool:
        """
        Parse raw move from the user.

        Arguments:
        move: str -- the move string the user inputted

        Raises GameError if move is invalid.

        Returns True if move passes turn in battle, returns False if not.
        """
        command, noun, noun_two = self._split_move(move.lower())
        # A dictionary of moves and their respective subroutine
        moves = {
            "help": (print_help, ()),
            "tutorial": (print_tutorial, ()),
            "inventory": (self.player.print_inventory, ()),
            "status": (self.player.print_status, ()),
            "status of": (self._parse_status_of, (noun,)),
            "punch": (self._parse_punch, (noun,)),
            "use": (self._parse_use, (noun, self.player)),
            "use on": (self._parse_use_on, (noun, noun_two)),
            "describe": (self._parse_describe, (noun,)),
            "search": (self._parse_search, (noun,)),
            "take": (self._parse_take, (noun,)),
            "drop": (self._parse_drop, (noun,)),
            "go": (self.board.move, (noun,)),
            "map": (self.board.print, ()),
            "look": (self.board.look, ()),
            "flee": (self.board.flee, ()),
            "quit": (exit, ()),
        }
        try:
            command_func, args = moves[command]
            return command_func(*args)
        except KeyError:
            raise GameError(f"\n{command} not a valid move! Try again.\n")     

    def _split_move(self, move: str) -> tuple[str, str, str]:
        """
        Take user input and split it into parts.

        Raises GameError if move is invalid.

        Returns a tuple with 3 elements:
            1: str -- The command being used (use, look etc.).
            2: str -- The first 'noun' (object) the command is being used on (sword, ogre etc.).
            3: str -- The second 'noun' (object) the command is being used on.
        Returns empty strings if command does not use two nouns.
        """
        parts = move.strip().split(" ")
        command = parts[0].lower()
        if command not in self._MOVES:
            raise GameError(f"\n{command} is not a valid command! Try again.\n")
        if len(parts) == 1 and parts[0] in self._ONE_WORD_MOVES:
            return command, "", ""
        elif len(parts) == 2 and parts[0] in self._TWO_WORD_MOVES:
            return command, parts[1], ""
        elif len(parts) == 3 and parts[0] == "status" and parts[1] == "of":
            command="status of"
            return command, parts[2], ""
        elif len(parts) == 4 and parts[0] == "use" and parts[2] == "on":
            command="use on"
            return command, parts[1], parts[3]
        raise GameError(f"\n'{command}' does not work in this way!\n"
                        "Enter 'tutorial' for tutorial or 'help '"
                        "for valid moves list.\n")

    def _parse_search(self, noun: str) -> bool:
        """
        Parse moves which use the 'search' command.
        
        Arguments:
        noun: str -- the enemy that should be searched.

        Raises GameError if:
            1 -- Passed an entity name for an entity that does not exist.
            2 -- Passed an entity name for an entity that is alive.
            3 -- Passed an entity name for an entity that is not hostile.
        
        Returns False.
        """
        for entity in self.board.current_location.entities:
            if entity.name == noun:
                if not entity.hostile:
                    raise GameError(f"\nOnly enemies can be searched, {noun} is not an enemy.\n")
                if entity.alive:
                    raise GameError(f"\n{entity.name.capitalize()} is alive!\n"
                                    "Only dead creatures can be searched.\n")
                found_items = entity.search()
                self.player.inventory.extend(found_items)
                if not found_items:
                    print("\nNo items found.\n")
                    return False
                print("\nFound:")
                for item in found_items:
                    print(item.name)
                print("")
                return False
        raise GameError(f"\nNo enemy named {noun} in area.\n")
    
    def _parse_take(self, noun:str) -> bool:
        """
        Parse moves which use the 'take' command.
        
        Arguments:
        noun: str -- the item which should be picked up.

        Raises GameError if passed an item name for an item
        that does not exist in the inventory.
        
        Returns False.
        """
        for index, item in enumerate(self.board.current_location.items):
            if item.name == noun:
                self.player.inventory.append(self.board.current_location.items.pop(index))
                print(f"\nTook {item.name}!\n")
                return False
        raise GameError(f"No item present called {item.name}.")

    def _parse_drop(self, noun: str) -> bool:
        """
        Parse moves which use the 'drop' command.
        
        Arguments:
        noun: str -- the item which should be dropped.

        Raises GameError if passed an item name for an item
        that does not exist in the inventory.
        
        Returns False.
        """
        for index, item in enumerate(self.player.inventory):
            if item.name == noun:
                self.board.current_location.items.append(self.player.inventory.pop(index))
                print(f"\nDropped {item.name}.\n")
                return False
        raise GameError(f"\nNo item named {noun} in inventory.\n")

    def _parse_punch(self, noun: str) -> bool:
        """
        Parse moves which use the 'punch' command.
        
        Arguments:
        noun: str -- the entity which should be punched.

        Raises GameError if passed an entity name for an entity
        that does not exist in the area.
        
        Returns True.
        """
        for entity in self.board.current_location.entities:
            if entity.name == noun:
                damage = -random.randrange(1, 3)
                punch_attack = Effect("you used punch attack", damage)
                punch_message = entity.affect_health(punch_attack)
                print(punch_message)
                return True
        raise GameError(f"\nNo entity called {noun} in area.\n")  

    def _parse_status_of(self, noun: str) -> bool:
        """
        Parse moves which use the 'status of' command.
        
        Arguments:
        noun: str -- the entity for which the status should be printed.

        Raises GameError if passed an entity name for an entity
        that does not exist in the area.
        
        Returns False.
        """
        for entity in self.board.current_location.entities:
            if entity.name == noun:
                entity.print_status()
                return False
        raise GameError(f"\nNo entity called {noun} in area.\n")

    def _parse_use(self, noun: str, target: Entity) -> bool:
        """
        Parse moves which use the 'use' command.
        
        Arguments:
        noun: str -- the item which should be used.
        target: Entity -- the entity which the item should be used on.

        Raises GameError if passed an item name for an item
        that does not exist in the inventory.
        
        Returns True.
        """
        for item in self.player.inventory:
            if item.name == noun and item.name != "amulet":
                use_message = item.use(target)
                print(use_message)
                if target.hostile and not target.alive:
                    self.game_state.records["score"] += 10
                return True
            if item.name == noun and item.name == "amulet":
                print(item.activate())
                return True
        raise GameError(f"\nNo item named {noun} in inventory.\n")

    def _parse_use_on(self, noun: str, noun_two: str) -> bool:
        """
        Parse moves which use the 'use on' command.
        
        Arguments:
        noun: str -- the item which should be used.
        noun_two: str -- the name of the entity which the item should be used on.

        Raises GameError if passed an entity name for an entity
        that does not exist in the area.
        
        Returns True.
        """
        for entity in self.board.current_location.entities:
            if entity.name == noun_two:
                return self._parse_use(noun, entity)
        raise GameError(f"\nNo creature named {noun_two} in area.\n")

    def _parse_describe(self, noun: str) -> bool:
        """
        Parse moves which use the 'describe' command.
        
        Arguments:
        noun: str -- the item which should be described.

        Raises GameError if passed an item name for an item
        that does not exist in the inventory.
        
        Returns False.
        """
        for item in self.player.inventory:
            if item.name == noun:
                print(f"\n{item.description}\n")
                return False
        raise GameError(f"\nNo item named {noun} in inventory.\n")