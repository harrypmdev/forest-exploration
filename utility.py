import random
import emoji
from effect import Effect
from entity import Entity
from player import Player
from game_error import GameError

def get_emojis(*args):
    """
    Returns a list of the emojis from the strings passed to the function
    """
    emoji_list = []
    for arg in args:
        emoji_list.append(emoji.emojize(arg))
    return emoji_list

def print_help() -> bool:
    """ Prints the game's valid moves. Always returns False. """
    print("\nValid moves:\n"
    "inventory - lists your current inventory\n"
    "status - outputs your health and score\n"
    "status of (creature name) - outputs the status of a creature\n"
    "look - gives a description of the area\n"
    "punch (creature name) - attacks a creature\n"
    "flee - run from battle in a random direction\n"
    "map - outputs the map\n"
    "describe (item name) - gives the description of an inventory item\n"
    "use (item name) - uses an item\n"
    "use (item name) on (target) - uses an item on a target\n"
    "search (enemy name) - search a defeated enemy for items\n"
    "go (North/East/South/West) - move on the map\n"
    "quit - quit the game\n"
    )
    return False

def print_tutorial() -> bool:
    """ Prints the game tutorial. Always returns False. """
    print("\nTutorial:\n"
    "Travel around the map using N, E, S and W commands to accumulate points\n"
    "and find the amulet of power! You get points by defeating enemies, healing\n"
    "sick animals and finding special items. When you enter an area with a hostile\n"
    "creature, you enter battle. In battle, you will be attacked every turn until\n"
    "the enemy is defeated. You can use items on the enemy, attempt to flee, or simply\n"
    "'punch' the enemy if you have no items to use. Good luck!\n")
    return False
    
def find_item_name(player: Player, item_name: str) -> str:
    for inventory_item in player.inventory:
        if inventory_item.name == item_name:
            return item_name
    if len(item_name) > 0:
        return find_item_name(player, item_name[:-1])
    return ""