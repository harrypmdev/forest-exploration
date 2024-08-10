import random
import math
from entity import Entity
from effect import Effect
from item import Item, HealthItem, Amulet

class Enemy(Entity):

    def __init__(self, health, name, game_state, max_damage, accuracy, attack_name):
        super().__init__(health, name, game_state, hostile=True)
        self.max_damage = max_damage
        self.accuracy = accuracy
        self.attack_name = attack_name
        self.loot = self.generate_loot()

    def generate_loot(self):
        loot = []
        for item_args in HealthItem.ITEMS:
            item_name = item_args[0]
            if random.random() < self.game_state.item_probabilites[item_name]:
                loot.append(HealthItem(*item_args))
        return loot
        
    def get_attack(self) -> Effect:
        damage = math.ceil(self.max_damage * (random.random() * self.accuracy))
        attack = Effect(f"{self.attack_name} by {self.name}", -damage)
        return attack
        
    def search(self) -> list[Item]:
        self.searched = True
        return self.loot