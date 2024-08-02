import emoji

def get_emojis(*args):
    """
    Returns a list of the emojis from the strings passed to the function
    """
    emoji_list = []
    for arg in args:
        emoji_list.append(emoji.emojize(arg))
    return emoji_list

def parse_move(move, board, player):
    board_moves = ("N", "E," "S", "S", "map")
    if move == "help":
        print("\nValid moves:\n"
        "inventory - prints your current inventory\n"
        "status - prints your current status\n"
        "map - prints the map\n"
        "describe (item name) - gives the description of an inventory item\n"
        "use (item name) - uses an item\n"
        "use (item name) on (target) - uses an item on a target\n"
        "N - moves North\n"
        "E - moves East\n"
        "S - moves South\n"
        "W - moves West\n"
        )
        return True
    elif move in ("status", "health", "points", "score"):
        player.print_status()
        return True
    elif move == "inventory":
        player.print_inventory()
        return True
    elif move == "break":
        exit()
    elif "use" in move:
        return parse_use_move(move, board, player)
    elif "describe" in move:
        return parse_describe_move(move, player)
    elif move in board_moves:
        return board.parse_move(move, player)
    else:
        return False

def parse_use_move(move, board, player):
    parts = move.split()
    if parts[0] != "use" or parts[1] not in (item.name for item in player.inventory):
        return False
    if len(parts) == 2:
        for item in player.inventory:
            if item.name == parts[1]:
                item.use(player)
    elif len(parts) == 4:
        if parts[2] != "on":
            return False
        for entity in board.entities:
            if parts[4] == entity.name:
                player.inventory.index(parts[1].use(entity))
    else:
        return false

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