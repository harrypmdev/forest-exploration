import emoji
import math
import os

class gameBoard:

    def __init__(self, size):
        tree, player = get_emojis(":evergreen_tree:", ":diamond_with_a_dot:")
        self.size = size
        self.board = [[tree for x in range(size)] for y in range(size)]
        self.visited = []
        middle = (math.floor(size/2))
        self.current_location = (middle, middle)
        self.board[middle][middle] = player
        self.visited.append((middle, middle))

    def print(self):
        print("\n")
        for row in self.board:
            print(" ".join(row))
    
    def introduce(self, player):
        print("═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══\n"
              "Welcome to Forest Exploration!\n"
              f"Your game board has {self.size}x{self.size} dimensions.\n"
              f"Your player starts with {player.health} health.\n"
              "Enter N, E, S or W to travel North, East, South and West.\n"
              "═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══")

    def add_to_visited(self,x, y):
        self.visited.append((x, y)) 
        self.board[x][y] = get_emojis(":radio_button:")[0]

    def parse_move(self, move):
        if move == "help":
            print("\nValid moves:\n"
            "inventory - prints your current inventory\n"
            "status - prints your current status\n"
            "map - prints the map\n"
            "N - moves North\n"
            "E - moves East\n"
            "S - moves South\n"
            "W - moves West\n"
            )
        elif move == "map":
            self.print()

class Player:

    def __init__(self, health, score, inventory):
        self.health = health
        self.score = score
        self.inventory = inventory
        self.alive = True

    def affect_health(self, effect):
        self.health = max(0, self.health + effect.value)
        if self.health == 0:
            self.die(effect)
    
    def die(self, effect):
        print('═' * 80)
        print(f'You died! You ran out of health when {effect.name} causing {abs(effect.value)} damage!\n')
        print('═' * 80)
        self.alive = False
    
    def print_status(self):
        print(f"\nYou have {self.health} health. Your score is {self.score}.\n")
    
    def get_move(self):
        print("Enter 'help' for instructions.\n")
        move = input("Enter a move: ")
        return move

class Effect:

    def __init__(self, name, value):
        self.name = name
        self.value = value

def get_emojis(*args):
    """
    Returns a list of the emojis from the strings passed to the function
    """
    emoji_list = []
    for arg in args:
        emoji_list.append(emoji.emojize(arg))
    return emoji_list

def main():
    board = gameBoard(5)
    player = Player(30, 0, [])
    board.introduce(player)
    while player.alive:
        player.print_status()
        move = player.get_move()
        board.parse_move(move)
        while move == "help":
            board.parse_move(move)
            move = player.get_move()
        if move == "break":
            break
main()