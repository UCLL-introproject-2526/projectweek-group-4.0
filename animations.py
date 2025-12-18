import pygame
from pygame.locals import *
from sprite import Sprite
from audio import Audio
from upgrades import UpgradeSystem


class Animations:

    def __init__(self):

        self.__clock = pygame.time.Clock()

        self.__drinktimer = 0
        self.__sharktimer = 0
        self.__orcatimer = 0
        self.__parrottimer = 0
        self.__idletimer = 0
        self.__firetimer = 0
        self.__particletimer = 0
        self.__idle_sprite = 0
        self.__shark_sprite = 0
        self.__orca_sprite = 0
        self.__parrot_sprite = 0
        self.__player_idle = True

        self.__idle1 = Sprite("Assets/Sprites/player_idle_1.png", 50, 81)
        self.__idle2 = Sprite("Assets/Sprites/player_idle_2.png", 50, 81)
        self.__drinking1 = Sprite("Assets/Sprites/player_drinking_1.png", 50, 81)
        self.__drinking2 = Sprite("Assets/Sprites/player_drinking_2.png", 50, 81)

        self.__cannon_fire1 = Sprite("Assets/Sprites/cannon_smoke_1.png", 100, 100)
        self.__cannon_fire2 = Sprite("Assets/Sprites/cannon_smoke_2.png", 100, 100)
        self.__cannon_fire3 = Sprite("Assets/Sprites/cannon_smoke_3.png", 100, 100)
        self.__cannon_idle = Sprite("Assets/Sprites/canon.png", 100, 100)
        self.__no_smoke = Sprite("Assets/Sprites/no_smoke.png", 100, 100)

        self.__upgrade_particle_1 = Sprite("Assets/Sprites/upgrade_particle_1.png", 200, 200)
        self.__upgrade_particle_2 = Sprite("Assets/Sprites/upgrade_particle_2.png", 200, 200)
        self.__upgrade_particle_3 = Sprite("Assets/Sprites/upgrade_particle_3.png", 200, 200)
        self.__upgrade_particle_4 = Sprite("Assets/Sprites/upgrade_particle_4.png", 200, 200)

        self.__upgrade_message_sprite = Sprite("Assets/Sprites/upgrade_popup.png",100,100)

        self.shark1 = Sprite("Assets/Sprites/shark_swim_1.png", 100, 162)
        self.shark1.rotate_sprite()
        self.shark2 = Sprite("Assets/Sprites/shark_swim_2.png", 100, 162)
        self.shark2.rotate_sprite()
        self.shark3 = Sprite("Assets/Sprites/shark_swim_3.png", 100, 162)
        self.shark3.rotate_sprite()
        self.shark4 = Sprite("Assets/Sprites/shark_swim_4.png", 100, 162)
        self.shark4.rotate_sprite()
        self.shark5 = Sprite("Assets/Sprites/shark_swim_5.png", 100, 162)
        self.shark5.rotate_sprite()
        self.shark6 = Sprite("Assets/Sprites/shark_swim_6.png", 100, 162)
        self.shark6.rotate_sprite()

        self.orca1 = Sprite("Assets/Sprites/orca_1.png", 100, 100)
        self.orca1.rotate_sprite()
        self.orca2 = Sprite("Assets/Sprites/orca_2.png", 100, 100)
        self.orca2.rotate_sprite()
        self.orca3 = Sprite("Assets/Sprites/orca_3.png", 100, 100)
        self.orca3.rotate_sprite()
        self.orca4 = Sprite("Assets/Sprites/orca_4.png", 100, 100)
        self.orca4.rotate_sprite()
        self.orca5 = Sprite("Assets/Sprites/orca_5.png", 100, 100)
        self.orca5.rotate_sprite()
        self.orca6 = Sprite("Assets/Sprites/orca_6.png", 100, 100)
        self.orca6.rotate_sprite()
        self.orca7 = Sprite("Assets/Sprites/orca_7.png", 100, 100)
        self.orca7.rotate_sprite()
        self.orca8 = Sprite("Assets/Sprites/orca_8.png", 100, 100)
        self.orca8.rotate_sprite()

        self.parrot1 = Sprite("Assets/Sprites/parrot_1.png", 80, 80)
        self.parrot2 = Sprite("Assets/Sprites/parrot_2.png", 80, 80)
        self.parrot3 = Sprite("Assets/Sprites/parrot_3.png", 80, 80)
        self.parrot4 = Sprite("Assets/Sprites/parrot_4.png", 80, 80)  
        self.parrot5 = Sprite("Assets/Sprites/parrot_5.png", 80, 80)
        self.parrot6 = Sprite("Assets/Sprites/parrot_6.png", 80, 80)
        self.parrot7 = Sprite("Assets/Sprites/parrot_7.png", 80, 80)
        self.parrot8 = Sprite("Assets/Sprites/parrot_8.png", 80, 80)
        self.parrot9 = Sprite("Assets/Sprites/parrot_9.png", 80, 80)
        self.parrot10 = Sprite("Assets/Sprites/parrot_10.png", 80, 80)
        self.parrot11 = Sprite("Assets/Sprites/parrot_11.png", 80, 80)
        self.parrot12 = Sprite("Assets/Sprites/parrot_12.png", 80, 80)

        self.__parrot_sprites_list = [self.parrot1, self.parrot2, self.parrot3, self.parrot4, self.parrot5, self.parrot6, self.parrot7, self.parrot8, self.parrot9, self.parrot10, self.parrot11, self.parrot12]

        self.__orca_sprites_list = [self.orca1, self.orca2, self.orca3, self.orca4, self.orca5, self.orca6, self.orca7, self.orca8]
        self.__shark_sprites_list = [self.shark1, self.shark2, self.shark3, self.shark4, self.shark5, self.shark6]

        self.__player_image = self.__idle1
        self.__shark_image = self.shark1
        self.__orca_image = self.orca1
        self.__parrot_image = self.parrot1
        self.__cannon_image = self.__cannon_idle
        self.__upgrade_particle_image = self.__no_smoke

        self.__show_upgrade_message = False
        self.__popup_timer = 0

    def start_drink_anim(self):
        audio = Audio()
        audio.Drink()
        self.__player_idle = False
        self.__drinktimer = 0.55

    def cannon_fire_anim(self):
        self.__firetimer = 0.3

    def upgrade_particle_anim(self):
        self.__particletimer = 0.4

    def handle_animations(self, current_gold_amount):
        #IDLE ANIMATION
        if self.__idletimer <= 0 and self.__player_idle:
            self.__idletimer = 0.5 #seconds
            if self.__idle_sprite == 0:
                self.__idle_sprite = 1
                self.__player_image = self.__idle1
            elif self.__idle_sprite == 1:
                self.__player_image = self.__idle2
                self.__idle_sprite = 0

        #DRINKING ANIMATION
        if self.__drinktimer <= 0:
            self.__player_idle = True
        elif self.__drinktimer >= 0.4:
            self.__player_image = self.__drinking1
        elif self.__drinktimer >= 0.25 and self.__drinktimer < 0.4:
             self.__player_image = self.__drinking2

        #SHARK ANIMATION
        if self.__sharktimer <= 0:
            if self.__shark_sprite >= len(self.__shark_sprites_list):
                self.__shark_sprite = 0
            self.__shark_image = self.__shark_sprites_list[self.__shark_sprite]
            self.__shark_sprite += 1
            self.__sharktimer = 0.1 #seconds

        #ORCA ANIMATION
        if self.__orcatimer <= 0:
            if self.__orca_sprite >= len(self.__orca_sprites_list):
                self.__orca_sprite = 0
            self.__orca_image = self.__orca_sprites_list[self.__orca_sprite]
            self.__orca_sprite += 1
            self.__orcatimer = 0.1 #seconds

        #CANNON FIRE ANIMATION
        if self.__firetimer > 0.2:
            self.__cannon_image = self.__cannon_fire1
        elif self.__firetimer > 0.1 and self.__firetimer <= 0.2:
            self.__cannon_image = self.__cannon_fire2
        elif self.__firetimer > 0 and self.__firetimer <= 0.1:
            self.__cannon_image = self.__cannon_fire3
        elif self.__firetimer <= 0:
            self.__cannon_image = self.__no_smoke
        
        #UPGRADE PARTICLE ANIMATION
        if self.__particletimer > 0.3:
            self.__upgrade_particle_image = self.__upgrade_particle_1
        elif self.__particletimer > 0.2 and self.__particletimer <= 0.3:
            self.__upgrade_particle_image = self.__upgrade_particle_2
        elif self.__particletimer > 0.1 and self.__particletimer <= 0.2:
            self.__upgrade_particle_image = self.__upgrade_particle_3
        elif self.__particletimer > 0 and self.__particletimer <= 0.1:
            self.__upgrade_particle_image = self.__upgrade_particle_4
        elif self.__particletimer <= 0:
            self.__upgrade_particle_image = self.__no_smoke

        #PARROT ANIMATION
        if self.__parrottimer <= 0:
            if self.__parrot_sprite >= len(self.__parrot_sprites_list):
                self.__parrot_sprite = 0
            self.__parrot_image = self.__parrot_sprites_list[self.__parrot_sprite]
            self.__parrot_sprite += 1
            self.__parrottimer = 0.2 #seconds

        #UPGRADE POPUP TIMER
        
        if self.__popup_timer <= 0:
            self.__show_upgrade_message = False
        else:
            self.__show_upgrade_message = True

        self.__dt = self.__clock.tick(60.0) / 1000.0
        self.__drinktimer -= self.__dt
        self.__sharktimer -= self.__dt
        self.__parrottimer -= self.__dt
        self.__orcatimer -= self.__dt
        self.__idletimer -= self.__dt
        self.__firetimer -= self.__dt
        self.__popup_timer -= self.__dt
        self.__particletimer -= self.__dt
        self.__drinktimer = max(0, self.__drinktimer)
        self.__orcatimer = max(0, self.__orcatimer)
        self.__parrottimer = max(0, self.__parrottimer)
        self.__sharktimer = max(0, self.__sharktimer)
        self.__idletimer = max(0, self.__idletimer)
        self.__firetimer = max(0, self.__firetimer)
        self.__particletimer = max(0, self.__particletimer)
        self.__popup_timer = max(0, self.__popup_timer)

    def get_player_img(self):
        return self.__player_image.get_sprite()

    def get_shark_img(self):
        return self.__shark_image.get_sprite()
    
    def get_orca_img(self):
        return self.__orca_image.get_sprite()
    
    def get_smoke_img(self):
        return self.__cannon_image.get_sprite()

    def get_parrot_img(self):
        return self.__parrot_image.get_sprite()

    def get_cannon_img(self):
        return self.__cannon_idle.get_sprite()

    def get_upgrade_particle_img(self):
        return self.__upgrade_particle_image.get_sprite()    
    
    def get_upgrade_popup(self):
        if self.__show_upgrade_message:
            return self.__upgrade_message_sprite.get_sprite()
        else:
            return pygame.Surface((0,0))

    def upgrade_message(self):
        self.__show_upgrade_message = True
        self.__popup_timer = 4.0
