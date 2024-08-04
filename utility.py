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

def parse_move(move, board, player):
    board_moves = ("n", "e", "s", "w", "map", "look", "flee")
    if move == "help":
        print("\nValid moves:\n"
        "inventory - lists your current inventory\n"
        "status - outputs your current status\n"
        "status of (creature name) - outputs the status of a creature\n"
        "look - gives a description of the area\n"
        "punch (creature name) - attacks a creature\n"
        "flee - run from battle in a random direction\n"
        "map - outputs the map\n"
        "describe (item name) - gives the description of an inventory item\n"
        "use (item name) - uses an item\n"
        "use (item name) on (target) - uses an item on a target\n"
        "N - moves North\n"
        "E - moves East\n"
        "S - moves South\n"
        "W - moves West\n"
        )
        return True
    elif "tutorial" in move:
        print("\nTutorial:\n"
        "Travel around the map using N, E, S and W commands to accumulate points\n"
        "and find the amulet of power! You get points by defeating enemies, healing\n"
        "sick animals and finding special items. When you enter an area with a hostile\n"
        "creature, you enter battle. In battle, you will be attacked every turn until\n"
        "the enemy is defeated. You can use items on the enemy, attempt to flee, or simply\n"
        "'punch' the enemy if you have no items to use. Good luck!\n")
    elif "status" in move:
        return parse_status_move(move, board, player)
    elif move == "inventory":
        player.print_inventory()
    elif move == "break":
        exit()
    elif "punch" in move:
        return parse_punch_move(move, board, player)
    elif "use" in move:
        return parse_use_move(move, board, player)
    elif "describe" in move:
        return parse_describe_move(move, player)
    elif move in board_moves:
        return board.parse_move(move, player)
    else:
        raise Exception

def parse_punch_move(move, board, player):
    entity_name = move[6:]
    for entity in board.get_current_area_entities():
        if entity.name == entity_name:
            damage = -random.randrange(1, 3)
            entity.affect_health(Effect("you punched it", damage), False)
            if entity.alive:
                print(f"\nYou punched {entity.name} dealing {str(abs(damage))} damage.\n")
            return True
        raise GameError(f"\nNo entity called {entity_name} in area.\n")  

def parse_status_move(move, board, player):
    if " of " in move:
        entity_name = move.split(" of ",1)[1]
        for entity in board.get_current_area_entities():
            if entity.name == entity_name:
                entity.print_status()
                return False
        raise GameError(f"\nNo entity called {entity_name} in area.\n")
    else:
        player.print_status()
        return False

def parse_use_move(move, board, player):
    parts = []
    parts.append(move[:3])
    parts.append(move[3:])
    parts = [part.strip() for part in parts]
    item_name = find_item_name(player, parts[1])
    if parts[0] != "use" and not item_name:
        return False
    target = player
    if item_name != parts[1] and " on " in parts[1][len(item_name):]:
        enemy_name = parts[1].split(" on ",1)[1]
        for entity in board.get_current_area_entities():
            if entity.name == enemy_name:
                target = entity
        if target == player:
            raise GameError(f"\nNo entity called {enemy_name} in the area.\n")
    item_used = False
    for item in player.inventory:
        if item.name == item_name:
            if item.target_item and target == player:
                raise GameError(f"\nThis item must be targeted at a creature.\n")
            else:
                item.use(player, target)
                item_used = True
    if not item_used:
        raise GameError(f"\nNo item in inventory called {parts[1]}.\n")
    return True

def parse_describe_move(move, player):
    parts = []
    parts.append(move[:8])
    parts.append(move[8:])
    parts = [part.strip() for part in parts]
    if parts[0] != "describe" or parts[1] not in (item.name for item in player.inventory):
        return False
    for item in player.inventory:
        if item.name == parts[1]:
            print("\n" + item.description + "\n")
            return True
    
def find_item_name(player: Player, item_name: str) -> str:
    for inventory_item in player.inventory:
        if inventory_item.name == item_name:
            return item_name
    if len(item_name) > 0:
        return find_item_name(player, item_name[:-1])
    return ""