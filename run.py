"""A script to trigger and run the Forest Exploration game."""

from utility import print_tutorial, get_move, yes_no_query, quit_game
from leaderboard import save_game, print_leaderboard
from game_board import GameBoard
from player import Player
from errors import GameError, LeaderboardError
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


def initialize_game(board_size: int) -> tuple[Player, GameBoard, GameState]:
    """Initialize a new game.

    Arguments:
    board_size: int -- the dimension size of the board (3 is a 3x3 board.)

    Returns a tuple with 3 elements:
        1: Player -- the player for this game.
        2: GameBoard -- the board for this game.
        3: GameState -- the game state for this game.
    """
    game_state = GameState()
    board = GameBoard(board_size, game_state)
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


def get_size() -> int:
    """
    Ask the user for the board size they wish to play on and validate input.
    Returns int of 3, 5 or 9 for small, medium and large inputs respectively.
    """
    size = ""
    while size.lower() not in ("small", "medium", "large"):
        size = input(
            "\n(small/medium/large)"
            "\nPlease enter the board size you would like to play:\n"
        )
        if size.lower() not in ("small", "medium", "large"):
            print("\nSize must be 'small', 'medium', or 'large'.")
    sizes = {"small": 3, "medium": 5, "large": 9}
    size_num = sizes[size.lower()]
    print(f"\n{size.capitalize()} chosen, a board size of {size_num}x{size_num}.\n")
    return size_num


def end_game(won: bool, records: dict) -> None:
    """
    Peform end of game procedures. Offer to save game to leaderboard if player
    won the game. If did not win, print advisory message.
    Print the leaderboard.
    Ask the user if they wish to play again. If yes, restart game, otherwise
    print exit message and exit program.

    Arguments:
    won: bool -- whether or not the user won the game (True if so, False if not).
    records: dict -- A dictionary of information about a game. Must include
                        keys: 'size', 'score', 'total moves', 'kills', 'health'.
    """
    if won:
        query = "Well done on finishing the game. Save score to leaderboard?"
        save_score = yes_no_query(query)
        if save_score:
            try:
                save_game(records)
            except LeaderboardError as e:
                print(str(e))
    else:
        print(
            "Only winners get to save their score to the leaderboard.\n"
            "Find and use the amulet to save your score!"
        )
    try:
        print_leaderboard()
    except LeaderboardError as e:
        print(str(e))
    if yes_no_query("Play again?"):
        main()
    else:
        quit_game()


def main() -> None:
    """Run the Forest Exploration game."""
    print("\nGreetings player!")
    if yes_no_query("Is it your first time playing?"):
        print_tutorial()
        input("Press any key to continue.")
    board_size = get_size()
    player, board, game_state = initialize_game(board_size)
    print(get_introduction(player, board))
    print("\nYou are in the center of a large forest.")
    print(board.current_location.get_description())
    game_loop(player, board, game_state)
    all_records = game_state.records
    all_records["health"] = player.health
    all_records["size"] = board_size
    end_game(game_state.game_won, all_records)


main()
