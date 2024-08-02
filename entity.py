class Entity:
    """
    An abstract class to be inherited by Player, Enemy and any other entities.
    """

    def __init__(self, health, name, board):
        self.name = name
        self.health = health
        self.alive = True
        board.entities.append(self)

    def affect_health(self, effect):
        self.health = max(0, self.health + effect.value)
        if self.health == 0:
            self.die(effect)
            return
        target_text = "on yourself" if self.name == "player" else f"on {self.name}"
        effect_text = "restoring" if effect.value >= 0 else "dealing"
        print(f"\n{effect.name.capitalize()} ${target_text} ${effect_text} {effect.value} health.\n")
    
    def die(self, effect):
        print(f'\n{self.name.capitalize()} died! It ran out of health when {effect.name} causing {abs(effect.value)} damage!\n')
        self.alive = False
    
    def print_status(self):
        print(f"\n{self.name.capitalize()} has {self.health} health.\n")