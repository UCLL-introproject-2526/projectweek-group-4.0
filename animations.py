import pygame
from pygame.locals import *
from sprite import Sprite
from audio import Audio

class Animations:
    
    def __init__(self):

        self.__clock = pygame.time.Clock()

        self.__drinktimer = 0
        self.__sharktimer = 0
        self.__idletimer = 0
        self.__idle_sprite = 0
        self.__shark_sprite = 0
        self.__player_idle = True

        self.__idle1 = Sprite("Assets/Sprites/player_idle_1.png", 50, 81)
        self.__idle2 = Sprite("Assets/Sprites/player_idle_2.png", 50, 81)
        self.__drinking1 = Sprite("Assets/Sprites/player_drinking_1.png", 50, 81)
        self.__drinking2 = Sprite("Assets/Sprites/player_drinking_2.png", 50, 81)

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


        self.__shark_sprites_list = [self.shark1, self.shark2, self.shark3, self.shark4, self.shark5, self.shark6]


        self.__player_image = self.__idle1
        self.__shark_image = self.shark1

    def start_drink_anim(self):
        audio = Audio()
        audio.Drink()
        self.__player_idle = False
        self.__drinktimer = 0.55


    def handle_animations(self):

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

        self.__dt = self.__clock.tick(60.0) / 1000.0
        self.__drinktimer -= self.__dt
        self.__sharktimer -= self.__dt
        self.__idletimer -= self.__dt
        self.__drinktimer = max(0, self.__drinktimer)
        self.__drinktimer = max(0, self.__drinktimer)
        self.__sharktimer = max(0, self.__sharktimer)
        self.__idletimer = max(0, self.__idletimer)

    def get_player_img(self):
        return self.__player_image.get_sprite()
    
    def get_shark_img(self):
        return self.__shark_image.get_sprite()
