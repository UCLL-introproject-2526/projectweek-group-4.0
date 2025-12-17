from sprite import Sprite

class Upgrade:

    def __init__(self, gold_cost, cannon_sprite, time_between_cannonfire):
        self.__gold_cost = gold_cost
        self.__cannon_sprite = cannon_sprite
        self.__time_between_cannonfire = time_between_cannonfire


    def get_upgrade_gold_cost(self):
        return self.__gold_cost
    
    def get_upgrade_cannon_sprite(self):
        return self.__cannon_sprite
    
    def get_time_between_cannonfire(self):
        return self.__time_between_cannonfire


class UpgradeSystem:
     
    def __init__(self):
        self.__gold_amount = 0
        self.__cannon1 = Sprite("Assets/Sprites/Canon.png",100,100)
        self.__cannon2 = Sprite("Assets/Sprites/Cannon2.png",100,100)
        self.__cannon3 = Sprite("Assets/Sprites/Cannon3.png",100,100)
        self.__cannon4 = Sprite("Assets/Sprites/Cannon4.png",100,100)


        self.__upgrades = [Upgrade(500, self.__cannon2, 750), Upgrade(1000, self.__cannon3, 500), 
                    Upgrade(1500, self.__cannon4, 300), Upgrade(2000, self.__cannon4, 150)]
        
        self.__current_cannon_sprite = self.__cannon1

        self.__current_upgrade_index = 0

        self.__current_time_between_cannonfire = 900

    def get_current_cannon_spirte(self):
        return self.__current_cannon_sprite
    
    def get_time_between_cannonfire(self):
        return self.__current_time_between_cannonfire
    
    def get_current_gold_amount(self):
        return self.__gold_amount

    def add_gold(self, gold_amount):
        self.__gold_amount += gold_amount

    def upgrade(self, anim):

        if self.__current_upgrade_index >= len(self.__upgrades):
            return

        current_upgrade = self.__upgrades[self.__current_upgrade_index]

        print(self.__current_upgrade_index)
        if self.__gold_amount >= current_upgrade.get_upgrade_gold_cost():
            self.__current_cannon_sprite = current_upgrade.get_upgrade_cannon_sprite()
            self.__gold_amount -= current_upgrade.get_upgrade_gold_cost()
            self.__current_upgrade_index += 1
            self.__current_time_between_cannonfire = current_upgrade.get_time_between_cannonfire()
            anim.upgrade_particle_anim()

    

