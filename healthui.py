from sprite import Sprite

class HealthUI:
    def __init__(self):
        self.__heart_sprite = Sprite("Assets/Sprites/Heart.png", 50, 50)
        self.__black_heart_sprite = Sprite("Assets/Sprites/BlackHeart.png", 50, 50)
        self.__boat_sprite1 = Sprite("Assets/Sprites/Boat.png", 720, 290)
        self.__boat_sprite2 = Sprite("Assets/Sprites/Boat1.png", 720, 290)
        self.__boat_sprite3 = Sprite("Assets/Sprites/Boat2.png", 720, 290)


        self.__boat_sprites_list = [self.__boat_sprite1, self.__boat_sprite2, self.__boat_sprite3]

        self.__current_boat_sprite = self.__boat_sprite1



    def draw_hearts(self, window, current_lives):
        x_pos = 500

        index = 2
        for i in range(current_lives):
            window.blit(self.__heart_sprite.get_sprite(), (x_pos, 15))
            self.__current_boat_sprite = self.__boat_sprites_list[index]
            index -= 1
            x_pos += 100

        for i in range(3 - current_lives):
            window.blit(self.__black_heart_sprite.get_sprite(), (x_pos, 15))
            x_pos += 100

    def get_current_boat_sprite(self):
        return self.__current_boat_sprite.get_sprite()