import math
import os
from game_board import GameBoard
from player import Player
from enemy import Enemy
from effect import Effect
from game_error import GameError
from item import *
from utility import *

def get_move():
    print("Enter 'help' for instructions.")
    return input("Enter a move: ")

def main():
    board = GameBoard(5)
    player = Player(30, board, 0, [])
    potion = HealthItem("health potion", "A potion that heals 10 health.", 10)
    player.inventory.append(potion)
    board.introduce(player)
    player.print_status()
    while player.alive:
        move = get_move()
        try:
            parse_move(move, board, player)
        except GameError as e:
            print(str(e))
        except Exception:
            print("Not a valid move! Try again.")

main()