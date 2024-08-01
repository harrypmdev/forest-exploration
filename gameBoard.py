import utility
import math

class gameBoard:

    def __init__(self, size):
        tree, player = utility.get_emojis(":evergreen_tree:", ":diamond_with_a_dot:")
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
        print("\n")
    
    def introduce(self, player):
        print("═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══\n"
              "Welcome to Forest Exploration!\n"
              f"Your game board has {self.size}x{self.size} dimensions.\n"
              f"Your player starts with {player.health} health.\n"
              "Enter N, E, S or W to travel North, East, South and West.\n"
              "═══━━━━━━━━━────────────────── • ──────────────────━━━━━━━━━═══")

    def add_to_visited(self,x, y):
        self.visited.append((x, y)) 
        self.board[x][y] = utility.get_emojis(":radio_button:")[0]

    def parse_move(self, move, player):
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
        elif move == "status":
            player.print_status()
        elif move == "inventory":
            player.print_inventory()
        elif move == "break":
            exit()
