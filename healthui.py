from sprite import Sprite

class HealthUI:
    def __init__(self):
        self.__heart_sprite = Sprite("Assets/Sprites/Heart.png", 50, 50)
        self.__black_heart_sprite = Sprite("Assets/Sprites/BlackHeart.png", 50, 50)


    def draw_hearts(self, window, current_lives):
        x_pos = 500

        for i in range(current_lives):
            window.blit(self.__heart_sprite.get_sprite(), (x_pos, 15))
            x_pos += 100

        for i in range(3 - current_lives):
            window.blit(self.__black_heart_sprite.get_sprite(), (x_pos, 15))
            x_pos += 100