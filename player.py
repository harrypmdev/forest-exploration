from entity import Entity
from utility import border

class Player(Entity):
    """
    A class to represent the player.
    """

    def __init__(self, health, inventory):
        super().__init__(health, "player")
        self.inventory = inventory
    
    @border
    def _die(self, effect):
        print(f"You died! Player {effect.name} causing"
        f"\n{abs(effect.value)} damage and ran out of health!")
        self.alive = False
    
    def print_status(self, score: int) -> bool:
        """ Prints the player's 'status' (health and score). Always returns False. """
        print(f"\nYou have {self.health} health. "
                f"Your score is {str(score)}\n")
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