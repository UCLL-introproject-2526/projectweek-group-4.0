
import pygame, sys, random
from pygame.locals import *
from sprite import Sprite
pygame.init()
 
# Colours
BACKGROUND = (255, 255, 255)

FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')

class Shark:
    def __init__(self, ypos_increment, xpos, ypos):
        self.ypos_increment = ypos_increment
        self.__xpos = xpos
        self.__ypos = ypos

    def get_next_frame(self):
        self.__ypos += self.ypos_increment
        return (self.__xpos, self.__ypos)

# === ADD: Background class ===
class Background:
    """Loads and renders a static background image."""
    def __init__(self, path: str, target_size: tuple[int, int]):
        self._path = path
        self._target_size = target_size
        self._image = self._create_image()

    def _create_image(self) -> pygame.Surface:
        try:
            img = pygame.image.load(self._path).convert_alpha()
            img = pygame.transform.smoothscale(img, self._target_size)
            return img
        except Exception as e:
            print(f"[WARN] Could not load background ({self._path}): {e}")
            surf = pygame.Surface(self._target_size)
            surf.fill(BACKGROUND)
            return surf

    def render(self, surface: pygame.Surface):
        surface.blit(self._image, (0, 0))

# === ADD: Create background instance ===
BACKGROUND_IMAGE = Background(
    path="image.png",  # Change this to your actual image path
    target_size=(WINDOW_WIDTH, WINDOW_HEIGHT)
)

# Sprites
sailor_idle = Sprite("Assets/Sprites/Sailor.png")
sailor_anim1 = Sprite("Assets/Sprites/Sailor1.png")
boat_sprite = Sprite("Assets/Sprites/Boat.png")
shark_sprite = Sprite("Assets/Sprites/Shark.png")

plater_sprites = [sailor_idle, sailor_anim1]

shart_y_spawn_pos = 600
shark_x_spawn_pos_list = [300, 600, 900]

active_sharks_list = []

last_time = 0
shark_spawn_delay = 6

# The main function that controls the game
def main():
    looping = True
    startpos = 550
    xpos = startpos
    movementAmount = 120

    currentanim_index = 0
    # The main game loop
    while looping:
        # Get inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_a:
                    if xpos > startpos - movementAmount:
                        xpos -= movementAmount
                if event.key == K_d:
                    if xpos < startpos + movementAmount:
                        xpos += movementAmount

        draw_window(xpos, currentanim_index)

def draw_window(xpos, currentanim_index):
    WINDOW.fill(BACKGROUND)

    # === ADD: Render background ===
    BACKGROUND_IMAGE.render(WINDOW)

    WINDOW.blit(sailor_idle.get_sprite(), (xpos, 200))
    currentanim_index += 1
    if currentanim_index >= len(plater_sprites):
        currentanim_index = 0
    animate_sailor(xpos, plater_sprites[currentanim_index])
    shark_spawner()
    pygame.display.update()
    fpsClock.tick(FPS)


def shark_spawner():
    current_time = pygame.time.get_ticks()
    global last_time
    if current_time - last_time >= shark_spawn_delay:
        last_time = current_time
        shark = Shark(-1, shark_x_spawn_pos_list[random.randint(0, len(shark_x_spawn_pos_list) -1)], shart_y_spawn_pos)
        active_sharks_list.append(shark)

    for shark in active_sharks_list:
        WINDOW.blit(shark_sprite.get_sprite(), (shark.get_next_frame()[0], shark.get_next_frame()[1]))


def animate_sailor(xpos, currentSprite):
    print(currentSprite)
    WINDOW.blit(currentSprite.get_sprite(), (xpos, 200))

main()


