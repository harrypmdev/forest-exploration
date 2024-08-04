import random
import math
from entity import Entity
from effect import Effect

class Enemy(Entity):

    def __init__(self, health, name, board, max_damage, accuracy, attack_name):
        super().__init__(health, name, board)
        self.max_damage = max_damage
        self.accuracy = accuracy
        self.attack_name = attack_name
        board.in_battle = True
    
    def attack(self, target):
        if random.random() > self.accuracy:
            damage = math.ceil(self.max_damage * (random.random() * self.accuracy))
            attack = Effect(f"{self.attack_name} by {self.name}", -damage)
            print(f"{self.name.capitalize()} attacked and it hit!")
            print(f"{target.name.capitalize()} {attack.name} for {str(damage)} damage.")
            target.affect_health(attack, False)
        else:
            print(f"{self.name.capitalize()} attacked and it missed!")