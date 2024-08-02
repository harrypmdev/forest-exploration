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
    
    def print_inventory(self):
        if not self.inventory:
            print("\nYour inventory is empty.\n")
            return
        print("Your inventory:")
        for item in self.inventory:
            print(f"\n{item}")
        print("\n")
    
    def get_move(self):
        print("Enter 'help' for instructions.\n")
        move = input("Enter a move: ")
        return move