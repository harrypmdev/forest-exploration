"""
A module containing general purpose functions for use by the other modules in
the Forest Exploration game.

Functions:
get_move -- receive the user's raw input for their game move.
yes_no_query -- ask the user a yes or no question and validate input.
get_emojis -- return the relevant emojis for areas on the map.
border -- decorate a callable with a two line border above and
          below its output.
print_help -- print the game's valid moves.
print_tutorial -- print the game tutorial.
print_key -- print the map key.
"""

from collections.abc import Callable

import emoji


def get_move() -> str:
    """Receive the user's raw input for their game move.
    Prints a message reminding them of the 'help' command before each input.

    Returns a string, the user's input.
    """
    print("Enter 'help' for valid move list.")
    return input("Enter a move: \n")


def yes_no_query(question: str) -> bool:
    """Ask the user a yes or no question and validate input.
    Repeats question until valid answer is entered.

    Arguments:
    question: str -- The question that should be asked.

    Returns a bool - True if yes, False if no.
    """
    answer = input(f"{question} (Yes/No): \n")
    if answer.lower() not in ("yes", "no"):
        print("\nPlease enter 'yes' or 'no'.")
        return yes_no_query(question)
    return answer.lower() == "yes"


def get_emojis(*args: str) -> list[str]:
    """
    Return the relevant emojis for areas on the map.

    Arguments:
    *args: str -- variable number of string arguments which denote the emojis
                  that should be returned. Valid inputs include: "tree",
                  "player", "battle", "visited".

    Raises ValueError if passed a string which does not correspond to
    a map location.

    Returns a list of strings.
    """
    key = {
        "tree": ":evergreen_tree:",
        "player": ":diamond_with_a_dot:",
        "battle": ":collision:",
        "visited": ":radio_button:",
    }
    emoji_list = []
    for arg in args:
        if arg not in key.keys():
            raise ValueError("Invalid map emoji name.")
        emoji_string = key[arg]
        emoji_list.append(emoji.emojize(emoji_string))
    return emoji_list


def border(func: Callable) -> Callable:
    """
    Decorate a callable with a two line border above and below its output.

    Arguments:
    func: Callable -- the callable to which the border should be added

    Returns a callable, the callable that was passed to the function
    but with the borders added.
    """

    def wrapper(*args):
        print("═" * 80)
        return_val = func(*args)
        print("═" * 80 + "\n")
        return return_val

    return wrapper


def print_help() -> bool:
    """Print the game's valid moves. Always returns False."""
    print(
        "\nValid moves:\n"
        "inventory - lists your current inventory\n"
        "status - outputs your health and score\n"
        "status of (creature name) - outputs the status of a creature\n"
        "look - gives a description of the area\n"
        "punch (creature name) - performs a weak attack on a creature\n"
        "flee - run from battle in a random direction\n"
        "map - outputs the map\n"
        "key - outputs the map key\n"
        "describe (item name) - gives the description of an inventory item\n"
        "use (item name) - uses an item\n"
        "use (item name) on (target) - uses an item on a target\n"
        "take (item name) - picks up an item from the ground\n"
        "drop (item name) - drops an item from the inventory onto the ground\n"
        "search (enemy name) - searches a defeated enemy for items\n"
        "go (North/East/South/West) - moves you on the map\n"
        "quit - quits the game\n"
    )
    return False


def print_tutorial() -> bool:
    """Print the game tutorial. Always returns False."""
    print(
        "\nTutorial:\n"
        "Travel around the map using the go command (go north, go east etc.)\n"
        "to accumulate points and find the amulet of power! You get points\n"
        "by defeating enemies and healing sick animals by using items on them.\n"
        "If you can find and use the amulet of power you have won the game!.\n"
        "When you enter an area with a hostile creature, you enter battle. In\n"
        "battle, you will be attacked every turn until the enemy is defeated.\n"
        "You can use items on the enemy (sword, poison etc.), attempt to flee,\n"
        "or simply 'punch' the enemy if you have no items to use. Good luck!\n"
    )
    return False


def print_key() -> bool:
    """Print the map key. Always returns False."""
    tree, player, battle, visited = get_emojis("tree", "player", "battle", "visited")
    print(
        "\nMap Key:\n"
        f"{tree} -- Unexplored forest.\n"
        f"{player} -- Your current location.\n"
        f"{battle} -- An unresolved battle you fled from.\n"
        f"{visited} -- A visited location with no living hostiles.\n"
    )
    return False
