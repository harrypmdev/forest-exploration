from collections.abc import Callable, Awaitable
import random
import emoji
from effect import Effect
from entity import Entity
from game_error import GameError

def get_emojis(*args):
    """
    Returns a list of the emojis from the strings passed to the function
    """
    emoji_list = []
    for arg in args:
        emoji_list.append(emoji.emojize(arg))
    return emoji_list

def border(func: Callable) -> Callable:
    def wrapper(*args):
        print('═' * 80)
        return_val = func(*args)
        print('═' * 80 + "\n")
        return return_val
    return wrapper 

def print_help() -> bool:
    """ Prints the game's valid moves. Always returns False. """
    print(
        "\nValid moves:\n"
        "inventory - lists your current inventory\n"
        "status - outputs your health and score\n"
        "status of (creature name) - outputs the status of a creature\n"
        "look - gives a description of the area\n"
        "punch (creature name) - performs a weak attack on a creature\n"
        "flee - run from battle in a random direction\n"
        "map - outputs the map\n"
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
    """ Prints the game tutorial. Always returns False. """
    print(
        "\nTutorial:\n"
        "Travel around the map using the go command (go north, go east etc.)\n"
        "to accumulate points and find the amulet of power! You get points\n"
        "by defeating enemies, healing sick animals and finding special items.\n"
        "When you enter an area with a hostile creature, you enter battle. In\n"
        "battle, you will be attacked every turn until the enemy is defeated.\n"
        "You can use items on the enemy (sword, poison etc.), attempt to flee,\n"
        "or simply 'punch' the enemy if you have no items to use. Good luck!\n"
    )
    return False