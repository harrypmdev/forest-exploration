class Entity:
    """
    A class for game entities, inherited by Player and Enemy.
    """

    def __init__(self, health, name, board):
        self.name = name
        self.health = health
        self.alive = True
        board.entities.append(self)

    def affect_health(self, effect, output_message = True):
        if not self.alive:
            print(f"\n{self.name.capitalize()} is dead, so nothing happens.\n")
            return
        self.health = max(0, self.health + effect.value)
        if self.health == 0:
            self.die(effect)
            return
        if not output_message:
            return
        target_text = "on yourself" if self.name == "player" else f"on {self.name}"
        effect_text = f"restoring {effect.value} health" if effect.value >= 0 else f"dealing {effect.value} damage"
        print(f"\n{effect.name.capitalize()} {target_text} {effect_text}!\n")
    
    def die(self, effect):
        print(f'\n{self.name.capitalize()} died! It ran out of health when {effect.name} causing {abs(effect.value)} damage!\n')
        self.alive = False
    
    def print_status(self):
        if self.health == 0:
            print(f"\n{self.name.capitalize()} is dead.\n")
        else:
            print(f"\n{self.name.capitalize()} has {self.health} health.\n")