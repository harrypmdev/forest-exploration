import math
import os
from game_board import GameBoard
from player import Player
from enemy import Enemy
from entity import Entity
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
    throwing_star = HealthItem("throwing star", "A weapon that deals 5 damage.", -5)
    bomb = HealthItem("bomb", "An explosive weapon that causes 15 damage.", -15)
    player.inventory.append(potion)
    player.inventory.append(throwing_star)
    player.inventory.append(bomb)
    board.introduce(player)
    player.print_status()
    while player.alive:
        move = get_move()
        try:
            parse_move(move.lower(), board, player)
        except GameError as e:
            print(str(e))
        except Exception:
            print("\nNot a valid move! Try again.\n")

main()