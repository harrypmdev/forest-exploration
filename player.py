from entity import Entity
from utility import *

class Player(Entity):
    """
    A class to represent the player.
    """

    def __init__(self, health, board, score, inventory, ):
        super().__init__(health, "player", board)
        self.score = score
        self.inventory = inventory
    
    @border
    def die(self, effect):
        print(f'You died! Player {effect.name} causing {abs(effect.value)} damage and ran out of health!\n')
        self.alive = False

    @border
    def win(self):
        moves = self.board.records["total moves"]
        kills = self.board.records["kills"]
        print(f"You win! You finished the game with a score total of {self.score} and {self.health} health.")
        print(f"You moved a total of {moves} times. You killed {kills} creatures.")
    
    def print_status(self, line_break: bool = True) -> bool:
        """ Prints the player's 'status' (health and score). Always returns False. """
        line_break = "\n" if line_break else ""
        print(f"\nYou have {self.health} health. Your score is {self.score}.{line_break}")
        return False
    
    def print_inventory(self) -> bool:
        " Prints the player's inventory. Always returns False."
        if not self.inventory:
            print("\nYour inventory is empty.\n")
            return False
        print("\nYour inventory:")
        item_names = []
        for item in self.inventory:
            item_names.append(item.name)
        for item_name in sorted(item_names):
            print(f"{item_name}")
        print("")
        return False