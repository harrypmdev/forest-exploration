import math
import os
from game_board import GameBoard
from player import Player
from enemy import Enemy
from entity import Entity
from effect import Effect
from game_error import GameError
from game_state import GameState
from parser import Parser
from item import *
from utility import *

def generate_items(self) -> dict:
    """ 
    Generate the list of items the can be spawned in this game. 
    Returns a dictionary of items and their generation probability.
    """
    items = {}
    items[HealthItem("potion", "A potion that heals 10 health.", 10)] = 0.05
    items[HealthItem("berries", "A tasty food. Heals 3 health.", 3)] = 0.05
    items[HealthItem("tomahawk", "A one-time use weapon that deals 7 damage.", -7, target_item=True)] = 0.1
    items[HealthItem("sword", "A sword that will last for a short while.", -4, 5, True)] = 0.05
    items[HealthItem("katana", "A super deadly sword that deals 10 damage.", -10, 7, True)] = 0.05
    items[HealthItem("axe", "A weak but durable weapon. Deals 3 damage.", -3, 15, True)] = 0.05
    items[Amulet("amulet", "Could it be... the amulet of power? There's only one way to find out.")] = 0
    return items

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
    item_field = generate_items()
    game_state = GameState()
    board = GameBoard(5, game_state)
    player = Player(30, board, 0, [])
    potion = HealthItem("potion", "A potion that heals 10 health.", 10)
    beginner_sword = HealthItem("sword", "A sword that will last for a short while.", -4, 5, True)
    player.inventory.append(potion)
    player.inventory.append(beginner_sword)
    board.introduce(player)
    player.print_status(False)
    print("You are in the center of a large forest.")
    board.look(False)
    parser = Parser(player)
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
    if player.won and yes_no_query("Well done on finishing the game. Save score to leaderboard? (Yes/No): \n"):
        save_game(player)
    print("")
    if yes_no_query("Play again?: \n"):
        main()
    else:
        print("\nThanks for playing. Goodbye!")
        exit()

main()