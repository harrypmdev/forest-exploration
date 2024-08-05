import random
import emoji
from effect import Effect
from entity import Entity
from player import Player
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
        "search", "quit", "go", "look"
        )

    def parse_move(self, move: str) -> bool:
        """
        Parses raw move from the user.
        Returns True if move passes turn,
        returns False if move does not pass turn.
        Raises exception if move is invalid.
        """
        command, noun, noun_two = self.split_move(move.lower())
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
            "quit": (exit, ()),
        }
        try:
            command_func, args = moves[command]
            command_func(*args)
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

    def parse_search(self, command, noun, board, player):
        entity_name = move.split("search ",1)[1]
        for entity in board.get_current_area_entities():
            print(entity.name)
            if entity.name == entity_name:
                if entity.alive:
                    print(f"\n{entity.name.capitalize()} is alive! Only dead creatures can be searched.\n")
                    return False
                found_items = entity.search(player)
                if found_items:
                    print("\nFound:")
                    for item in found_items:
                        print(f"{item.name}")
                else:
                    print("\nNo items found.")
                print("")
                return False
            raise GameError(f"\nNo entity called {entity_name} in area.\n") 
        return False

    def parse_punch(self, command, noun, board, player):
        entity_name = move[6:]
        for entity in board.get_current_area_entities():
            print("real entity name:" + entity.name + ", you entered:" + entity_name)
            if entity.name == entity_name:
                damage = -random.randrange(1, 3)
                entity.affect_health(Effect("you punched it", damage), False)
                if entity.alive:
                    print(f"\nYou punched {entity.name} dealing {str(abs(damage))} damage.\n")
                return True
            raise GameError(f"\nNo entity called {entity_name} in area.\n")  

    def parse_status_of(self, move, board, player):
        if " of " in move:
            entity_name = move.split(" of ",1)[1]
            for entity in board.get_current_area_entities():
                print(entity.name)
                if entity.name == entity_name:
                    entity.print_status()
                    return False
            raise GameError(f"\nNo entity called {entity_name} in area.\n")
        else:
            player.print_status()
            return False

    def parse_use(self, noun, target):
        for item in self.player.inventory:
            if item.name == noun:
                item.use(self.player, target)
                return False
        print (f"\nNo item named {noun} in inventory.\n")
        return False

    def parse_use_on(self, noun, noun_two):
        for entity in self.board.current_location.entities:
            if entity.name == noun_two:
                return self.parse_use(noun, entity)
        print (f"\nNo creature named {noun_two} in area.\n")
        return False

    def parse_describe(self, noun):
        for item in self.player.inventory:
            if item.name == noun:
                print(f"\n{item.description}\n")
                return False
        print (f"\nNo item named {noun} in inventory.\n")
        return False