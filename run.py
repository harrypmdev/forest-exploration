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

def introduce(self, player: Player, game_board: GameBoard) -> None:
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
            "Enter 'tutorial' if it is your first time playing.\n"
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

def end_turn(self, player: Player, board: Gameboard) -> None:
    """ End the turn, making all living enemies attack the player. 

    Arguments:
    player: Player -- the player for this game, as created 
    by the initialize_game function
    board: GameBoard -- the board for this game, as created
    by the initialize game function
    """
    for entity in board.current_location.entities:
        if type(entity) == Enemy and entity.alive and player.alive:
            player.affect_health(entity.get_attack())

def initialize_game() -> tuple[Player, GameBoard, GameState]:
    """ Initialize a new game.

    Returns a tuple with 3 elements:
        1: Player -- the player for this game.
        2: GameBoard -- the board for this game.
        3: GameState -- the game state for this game.
    """
    item_field = generate_items()
    game_state = GameState()
    board = GameBoard(5, game_state, item_field)
    player = Player(30, board, 0, [])
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
    parser = Parser(player, board)
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
    introduce(player, game_board)
    player.print_status(False)
    print("You are in the center of a large forest.")
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