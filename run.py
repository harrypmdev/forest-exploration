import math
import os
import random
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

def introduce(player: Player, game_board: GameBoard) -> None:
    """ Print a game introductory message. 
    
    Arguments:
    player: Player -- the player for which the message should 
    be printed, as created by the initialize_game function
    board: GameBoard -- the board for which the message should 
    be printed, as created by the initialize_game function
    """
    print("═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══\n"
            "Welcome to Forest Exploration!\n"
            f"Your game board has {game_board.size}x{game_board.size} dimensions.\n"
            f"Your player starts with {player.health} health.\n"
            "═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══")

def get_move() -> str:
    """ Receive the user's raw input for their game move.
    Prints a message reminding them of the 'help' command before each input.

    Returns a string, the user's input.
    """
    print("Enter 'help' for valid move list.")
    return input("Enter a move: \n")

def yes_no_query(question: str) -> bool:
    """ Ask the user a yes or no question and validate input.
    Repeats question until valid answer is entered.

    Returns a bool - True if yes, False if no.
    """
    answer = input(question)
    if answer.lower() not in ("yes", "no"):
        print("\nPlease enter 'yes' or 'no'.")
        return yes_no_query(question)
    return answer.lower() == "yes"

def save_game(game_state: GameState):
    pass

def end_turn(player: Player, board: GameBoard) -> None:
    """ End the turn, making all living enemies attack the player. 

    Arguments:
    player: Player -- the player for this game, as created 
    by the initialize_game function
    board: GameBoard -- the board for this game, as created
    by the initialize game function
    """
    for entity in board.current_location.entities:
        if entity.hostile and entity.alive and player.alive:
            if random.random() < entity.accuracy:
                attack = entity.get_attack()
                player.affect_health(attack)
                print(f"{entity.name.capitalize()} attacked and it hit!")
                print(f"Player {attack.name} for {str(abs(attack.value))} damage.\n")
            else:
                print(f"{entity.name.capitalize()} attacked and it missed!\n")

def initialize_game() -> tuple[Player, GameBoard, GameState]:
    """ Initialize a new game.

    Returns a tuple with 3 elements:
        1: Player -- the player for this game.
        2: GameBoard -- the board for this game.
        3: GameState -- the game state for this game.
    """
    game_state = GameState()
    board = GameBoard(5, game_state)
    player = Player(30, board, game_state, [])
    player.inventory.append(HealthItem("potion", "A potion that heals 10 health.", 10))
    player.inventory.append(HealthItem("sword", "A sword that will last for a short while.", -4, 5, True))
    return player, board, game_state

def game_loop(player: Player, board: GameBoard, game_state: GameState) -> None:
    """ Run the game loop, asking the player for 
    their move for as long as the game continues.

    Arguments:
    player: Player -- the player for this game, as created 
    by the initialize_game function
    board: GameBoard -- the board for this game, as created
    by the initialize game function
    game_state: GameState -- the game state for this game, as
    created by the initialize game function
    """
    parser = Parser(player, board, game_state)
    while player.alive:
        move = get_move()
        try:
            if parser.parse_move(move):
                if game_state.game_won:
                    break
                end_turn(player, board)
        except GameError as e:
            print(str(e))

def main():
    """ Run the Forest Exploration game. """
    player, board, game_state = initialize_game()
    if yes_no_query("Is it your first time playing?: \n"):
        print_tutorial()
        input("Press any key to continue.\n")
    introduce(player, board)
    print("\nYou are in the center of a large forest.")
    board.look(False)
    game_loop(player, board, game_state)
    if game_state.game_won and yes_no_query("Well done on finishing the game. Save score to leaderboard? (Yes/No): \n"):
        save_game(game_state)
    print("")
    if yes_no_query("Play again?: \n"):
        main()
    else:
        print("\nThanks for playing. Goodbye!")
        exit()

main()