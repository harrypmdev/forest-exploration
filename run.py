import math
import os
from game_board import GameBoard
from player import Player
from enemy import Enemy
from entity import Entity
from effect import Effect
from game_error import GameError
from parser import Parser
from item import *
from utility import *

def get_move():
    print("Enter 'help' for valid move list.")
    return input("Enter a move: \n")

def yes_no_query(question: str) -> bool:
    answer = input(question)
    if answer.lower() not in ("yes", "no"):
        print("\nPlease enter 'yes' or 'no'.")
        return yes_no_query(question)
    return answer.lower() == "yes"

def save_game(player):
    pass

def main():
    board = GameBoard(5)
    player = Player(30, board, 0, [])
    potion = HealthItem("potion", "A potion that heals 10 health.", 10)
    beginner_sword = HealthItem("sword", "A sword that will last for a short while.", -4, 5, True)
    player.inventory.append(potion)
    player.inventory.append(beginner_sword)
    board.introduce(player)
    player.print_status(False)
    print("You are in the center of a large forest.")
    board.look(False)
    parser = Parser(player, board)
    while player.alive:
        move = get_move()
        try:
            if parser.parse_move(move):
                if player.won:
                    break
                board.end_turn(player)
        except GameError as e:
            print(str(e))
        #except Exception:
            #print("\nNot a valid move! Try again.\n")
    if player.won and yes_no_query("\nWell done on finishing the game. Save score to leaderboard? (Yes/No): \n"):
        save_game(player)
    if yes_no_query("\nPlay again?: \n"):
        main()
    else:
        exit()

main()