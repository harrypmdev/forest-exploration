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
    VALID_MOVES = (
        "help", "tutorial", "inventory", 
        "status", "status of", "punch", 
        "use", "use on", "describe", "map",
        "search", "quit", "go", "look", 
        "flee", "take", "drop"
    )

    def __init__(self, player: Player) -> None:
        """
        Create a Parser object.
    
        Arguments:
        player: Player -- the player for which moves are being parsed.
        """
        self.player = player
        self.board = player.board

    def parse_move(self, move: str) -> bool:
        """
        Parse raw move from the user.

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
            "status of": (self._parse_status_of, (noun, )),
            "punch": (self._parse_punch, (noun, )),
            "use": (self._parse_use, (noun, self.player)),
            "use on": (self._parse_use_on, (noun, noun_two)),
            "describe": (self._parse_describe, (noun, )),
            "search": (self._parse_search, (noun, )),
            "take": (self._parse_take, (noun, )),
            "drop": (self._parse_drop, (noun, )),
            "go": (self.board.move, (noun, )),
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

    def _split_move(self, move: str) -> (str, str, str):
        """
        Take user input and split it into parts.

        Raises GameError if move is invalid.

        Returns a tuple with three strings:
            First string: The command being used (use, look etc.).
            Second and third string: The 'nouns' (objects) they are being used on (sword, ogre etc.).
        Returns empty strings if command does not use two nouns.
        """
        parts = move.split(" ")
        command = parts[0].lower()
        if command not in self.VALID_MOVES:
            raise GameError(f"\n{command} is not a valid command! Try again.\n")
        if len(parts) == 1:
            return command, "", ""
        if len(parts) == 2:
            return command, parts[1], ""
        if parts[0] == "status" and parts[1] == "of":
            command="status of"
            return command, parts[2], ""
        if parts[0] == "use" and parts[2] == "on":
            command="use on"
            return command, parts[1], parts[3]
        else:
            raise GameError(f"\n'{command}' does not work in this way! Enter 'tutorial' for tutorial or 'help' for valid moves list.\n")

    def _parse_search(self, noun: str) -> bool:
        """
        Parse moves which use the 'search' command.
        
        Arguments:
        noun: str -- the enemy that should be searched.

        Raises GameError if passed an entity name for an entity
        that does not exist in the area.
        
        Returns False.
        """
        for entity in self.board.current_location.entities:
            if entity.name == noun:
                if type(entity) != Enemy:
                    print(f"\nOnly enemies can be searched, {noun} is not an enemy.\n")
                    return False
                if entity.alive:
                    print(f"\n{entity.name.capitalize()} is alive! Only dead creatures can be searched.\n")
                else:
                    searched_items = entity.search(self.player)
                    if not searched_items:
                        print("\nNo items found.\n")
                        return False
                    print("\nFound:")
                    for item in searched_items:
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
                entity.affect_health(Effect("you punched it", damage), False)
                if entity.alive:
                    print(f"\nYou punched {entity.name} dealing {str(abs(damage))} damage.\n")
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
        for entity in self.board.get_current_area_entities():
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
            if item.name == noun:
                item.use(self.player, target)
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