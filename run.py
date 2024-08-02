import math
import os
from game_board import GameBoard
from player import Player
from effect import Effect
from item import *
from utility import *

def parse_move(move, board, player):
    board_moves = ("N", "E," "S", "S", "map")
    if move == "help":
        print("\nValid moves:\n"
        "inventory - prints your current inventory\n"
        "status - prints your current status\n"
        "map - prints the map\n"
        "use (item name) - uses an item\n"
        "use (item name) on (target) - uses an item on a target\n"
        "N - moves North\n"
        "E - moves East\n"
        "S - moves South\n"
        "W - moves West\n"
        )
    elif move in ("status", "health", "points", "score"):
        player.print_status()
    elif move == "inventory":
        player.print_inventory()
    elif move == "break":
        exit()
    elif "use" in move:
        return parse_use_move(move, board, player)
    elif move in board_moves:
        board.parse_move(move, player)

def parse_use_move(move, board, player):
    parts = move.split()
    if parts[0] != "use" or parts[1] not in (item.name for item in player.inventory):
        return False
    if len(parts) == 2:
        for item in player.inventory:
            if item.name == parts[1]:
                item.use(player)
    elif len(parts) == 4:
        if parts[2] != "on":
            return False
        for entity in board.entities:
            if parts[4] == entity.name:
                player.inventory.index(parts[1].use(entity))
    else:
        return false

def get_move():
    print("Enter 'help' for instructions.")
    move = input("Enter a move: ")
    return move

def main():
    board = GameBoard(5)
    player = Player(30, 0, [], board)
    potion = HealthItem("potion", "A potion that deals 10 damage.", -10)
    player.inventory.append(potion)
    board.introduce(player)
    player.print_status()
    while player.alive:
        move = get_move()
        parse_move(move, board, player)

main()