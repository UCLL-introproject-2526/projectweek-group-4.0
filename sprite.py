import pygame


class Sprite:

    def __init__(self, file_path, x_scale, y_scale):
        self.file_path = file_path
        self.player_img = pygame.image.load(file_path).convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (x_scale, y_scale))

    def get_sprite(self):
        return self.player_img
    
    def rotate_sprite(self):
        self.player_img = pygame.transform.rotate(self.player_img, 180)