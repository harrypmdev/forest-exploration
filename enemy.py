import random
import math
from entity import Entity
from effect import Effect
from item import Item, HealthItem, Amulet, GenerateItems

class Enemy(Entity):

    def __init__(self, health, name, game_state, max_damage, accuracy, attack_name):
        super().__init__(health, name, game_state, hostile=True)
        self.max_damage = max_damage
        self.accuracy = accuracy
        self.attack_name = attack_name
        self.loot = GenerateItems.generate((HealthItem,))

    def get_attack(self) -> Effect:
        damage = math.ceil(self.max_damage * (random.random() * self.accuracy))
        attack = Effect(f"{self.attack_name} by {self.name}", -damage)
        return attack
        
    def search(self) -> list[Item]:
        self.searched = True
        return self.loot