import pygame


class Sprite:

    def __init__(self, file_path):
        self.file_path = file_path
        self.player_img = pygame.image.load("Assets/Sprites/Sailor.png").convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (100, 162))

    def get_sprite(self):
        return self.player_img