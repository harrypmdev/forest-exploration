"""A script to trigger and run the Forest Exploration game."""

from utility import print_tutorial, get_move, yes_no_query
from leaderboard import Save, save_game
from game_board import GameBoard
from player import Player
from game_error import GameError
from game_state import GameState
from parser import Parser
from item import HealthItem
from effect import Effect


def get_introduction(player: Player, game_board: GameBoard) -> str:
    """
    Return a game introductory message.

    Arguments:
    player: Player -- the player for which the message should
    be written, as created by the initialize_game function.
    board: GameBoard -- the board for which the message should
    be written, as created by the initialize_game function.

    Returns a string.
    """
    return (
        "═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══\n"
        "Welcome to Forest Exploration!\n"
        f"Your game board has {game_board.size}x{game_board.size} dimensions.\n"
        f"Your player starts with {player.health} health.\n"
        "═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══"
    )

def end_turn(player: Player, board: GameBoard) -> None:
    """End the turn, making all living enemies attack the player.

    Arguments:
    player: Player -- the player for this game, as created
    by the initialize_game function
    board: GameBoard -- the board for this game, as created
    by the initialize_game function
    """
    for entity in board.current_location.entities:
        if entity.hostile and entity.alive and player.alive:
            if entity.attack_chance():
                attack: Effect = entity.get_attack()
                player.apply_effect(attack)
                if not player.alive:
                    break
                print(f"{entity.name.capitalize()} attacked and it hit!")
                print(f"Player {attack.name} for {str(abs(attack.value))} damage.\n")
            else:
                print(f"{entity.name.capitalize()} attacked and it missed!\n")


def initialize_game() -> tuple[Player, GameBoard, GameState]:
    """Initialize a new game.

    Returns a tuple with 3 elements:
        1: Player -- the player for this game.
        2: GameBoard -- the board for this game.
        3: GameState -- the game state for this game.
    """
    game_state = GameState()
    board = GameBoard(5, game_state)
    potion = HealthItem("potion", "A potion that heals 10 health.", 10)
    sword = HealthItem(
        "sword", "A sword that will last for a short while.", -4, 5, True
    )
    player: Player = Player(30, [potion, sword])
    return player, board, game_state


def game_loop(player: Player, board: GameBoard, game_state: GameState) -> None:
    """Run the game loop, asking the player for
    their move for as long as the game continues.

    Arguments:
    player: Player -- the player for this game, as created
    by the initialize_game function
    board: GameBoard -- the board for this game, as created
    by the initialize_game function
    game_state: GameState -- the game state for this game, as
    created by the initialize_game function
    """
    parser = Parser(player, board, game_state)
    while player.alive and not game_state.game_won:
        move = get_move()
        try:
            if parser.parse_move(move):
                end_turn(player, board)
        except GameError as e:
            print(str(e))


def main():
    """Run the Forest Exploration game."""
    player, board, game_state = initialize_game()
    print("\nGreetings player!")
    if yes_no_query("Is it your first time playing?"):
        print_tutorial()
        input("Press any key to continue.\n")
    print(get_introduction(player, board))
    print("\nYou are in the center of a large forest.")
    print(board.current_location.get_description())
    game_loop(player, board, game_state)
    if game_state.game_won:
        save_score = yes_no_query(
            "Well done on finishing the game. " "Save score to leaderboard?"
        )
        if save_score:
            all_records = game_state.records
            all_records["health"] = player.health
            save_game(all_records)
    if yes_no_query("Play again?"):
        main()
    else:
        print("\nThanks for playing. Goodbye!")
        exit()


main()
