
class Player:
    """
    A class to represent the player.
    """

    def __init__(self, health, score, inventory, board):
        self.name = "player"
        self.health = health
        self.score = score
        self.inventory = inventory
        self.alive = True
        board.entities.append(self)

    def affect_health(self, effect):
        self.health = max(0, self.health + effect.value)
        if self.health == 0:
            self.die(effect)
        elif effect.value >= 0:
            print(f"\n{effect.name.capitalize()} and restored {effect.value} health.\n")
        else:
            print(f"\n{effect.name.capitalize()} and received {abs(effect.value)} damage.\n")
    
    def die(self, effect):
        print('═' * 80)
        print(f'You died! You ran out of health when {effect.name} causing {abs(effect.value)} damage!\n')
        print('═' * 80)
        self.alive = False
    
    def print_status(self):
        print(f"\nYou have {self.health} health. Your score is {self.score}.\n")
    
    def print_inventory(self):
        if not self.inventory:
            print("\nYour inventory is empty.\n")
            return
        print("\nYour inventory:")
        for item in self.inventory:
            print(f"{item.name}\n")
    
    def get_move(self):
        print("Enter 'help' for instructions.")
        move = input("Enter a move: ")
        return move