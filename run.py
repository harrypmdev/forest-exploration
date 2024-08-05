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
    print("Enter 'help' for valid move list.")
    return input("Enter a move: ")

def main():
    board = GameBoard(5)
    player = Player(30, board, 0, [])
    potion = HealthItem("health potion", "A potion that heals 10 health.", 10)
    throwing_star = HealthItem("throwing star", "A weapon that deals 5 damage.", -7, target_item=True)
    beginner_sword = HealthItem("sword", "A sword that will last for a short while.", -4, 5, True)
    katana = HealthItem("katana", "A strong and sturdy weapon.", -20, 100, True)
    player.inventory.append(potion)
    player.inventory.append(beginner_sword)
    board.introduce(player)
    player.print_status(False)
    board.look(False)
    while player.alive:
        move = get_move()
        try:
            if parse_move(move.lower(), board, player):
                board.end_turn(player)
        except GameError as e:
            print(str(e))
        #except Exception:
            #print("\nNot a valid move! Try again.\n")

main()