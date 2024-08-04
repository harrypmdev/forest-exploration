from entity import Entity

class Player(Entity):
    """
    A class to represent the player.
    """

    def __init__(self, health, board, score, inventory, ):
        super().__init__(health, "player", board)
        self.score = score
        self.inventory = inventory
    
    def die(self, effect):
        print('═' * 80)
        print(f'You died! You ran out of health when {effect.name} causing {abs(effect.value)} damage!\n')
        print('═' * 80)
        self.alive = False
    
    def print_status(self, line_break = True):
        line_break = "\n" if line_break else ""
        print(f"\nYou have {self.health} health. Your score is {self.score}.{line_break}")
    
    def print_inventory(self):
        if not self.inventory:
            print("\nYour inventory is empty.\n")
            return
        print("\nYour inventory:")
        for item in self.inventory:
            print(f"{item.name}")
        print("")