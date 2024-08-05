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

    def __init__(self, player, board):
        self.player = player
        self.board = board
        self.valid_moves = (
        "help", "tutorial", "inventory", 
        "status", "status of", "punch", 
        "use", "use on", "describe", "map",
        "search", "quit", "go", "look", 
        "flee", "take"
        )

    def parse_move(self, move: str) -> bool:
        """
        Parses raw move from the user.
        Returns True if move passes turn,
        returns False if move does not pass turn.
        Raises exception if move is invalid.
        """
        command, noun, noun_two = self.split_move(move.lower())
        # A dictionary of moves and their respective subroutine
        moves = {
            "help": (print_help, ()),
            "tutorial": (print_tutorial, ()),
            "inventory": (self.player.print_inventory, ()),
            "status": (self.player.print_status, ()),
            "status of": (self.parse_status_of, (noun, )),
            "punch": (self.parse_punch, (noun, )),
            "use": (self.parse_use, (noun, self.player)),
            "use on": (self.parse_use_on, (noun, noun_two)),
            "describe": (self.parse_describe, (noun, )),
            "search": (self.parse_search, (noun, )),
            "take": (self.parse_take, (noun, )),
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

    def split_move(self, move: str) -> (str, str, str):
        """
        Takes user input and returns the command being used (use, look etc.) as well 
        as the 'nouns' (objects) they are being used on (sword, ogre etc.).
        Nouns are empty strings if command does not use it.
        """
        parts = move.split(" ")
        command = parts[0].lower()
        if command not in self.valid_moves:
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

    def parse_search(self, noun: str) -> bool:
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
        print (f"\nNo enemy named {noun} in area.\n")
        return False
    
    def parse_take(self, noun:str) -> bool:
        for index, item in enumerate(self.board.current_location.items):
            if item.name == noun:
                self.player.inventory.append(self.board.current_location.items.pop(index))
                print(f"\nTook {item.name}!\n")
        return False

    def parse_punch(self, noun: str) -> bool:
        for entity in self.board.current_location.entities:
            if entity.name == noun:
                damage = -random.randrange(1, 3)
                entity.affect_health(Effect("you punched it", damage), False)
                if entity.alive:
                    print(f"\nYou punched {entity.name} dealing {str(abs(damage))} damage.\n")
                return True
        print(f"\nNo entity called {noun} in area.\n")
        return False     

    def parse_status_of(self, noun: str) -> bool:
        for entity in self.board.get_current_area_entities():
            if entity.name == noun:
                entity.print_status()
                return False
        print(f"\nNo entity called {noun} in area.\n")
        return False

    def parse_use(self, noun: str, target: Entity) -> bool:
        for item in self.player.inventory:
            if item.name == noun:
                item.use(self.player, target)
                return True
        print (f"\nNo item named {noun} in inventory.\n")
        return True

    def parse_use_on(self, noun: str, noun_two: str) -> bool:
        for entity in self.board.current_location.entities:
            if entity.name == noun_two:
                return self.parse_use(noun, entity)
        print (f"\nNo creature named {noun_two} in area.\n")
        return True

    def parse_describe(self, noun) -> bool:
        for item in self.player.inventory:
            if item.name == noun:
                print(f"\n{item.description}\n")
                return False
        print (f"\nNo item named {noun} in inventory.\n")
        return False