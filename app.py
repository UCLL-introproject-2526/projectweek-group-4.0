
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
    """Loads and tiles a seamless background image."""
    def __init__(self, path: str, tile_size: tuple[int, int]):
        self._path = path
        self._tile_size = tile_size
        self._tile = self._load_tile()

    def _load_tile(self) -> pygame.Surface:
        try:
            img = pygame.image.load(self._path).convert_alpha()
            img = pygame.transform.smoothscale(img, self._tile_size)
            return img
        except Exception as e:
            print(f"[WARN] Could not load background ({self._path}): {e}")
            surf = pygame.Surface(self._tile_size)
            surf.fill(BACKGROUND)
            return surf

    def render(self, surface: pygame.Surface):
        tile_w, tile_h = self._tile.get_size()
        screen_w, screen_h = surface.get_size()

        for x in range(0, screen_w, tile_w):
            for y in range(0, screen_h, tile_h):
                surface.blit(self._tile, (x, y))

# === ADD: Create background instance ===
BACKGROUND_IMAGE = Background(
    path="Assets/background/background3.png",
    tile_size=(450, 250)  # smaller = more repeats
)

# Sprites
sailor_idle = Sprite("Assets/Sprites/Sailor.png", 50, 81)
sailor_anim1 = Sprite("Assets/Sprites/Sailor1.png", 50, 81)
boat_sprite = Sprite("Assets/Sprites/Boat.png", 100, 162)
shark_sprite = Sprite("Assets/Sprites/Shark.png", 100, 162)
shark_sprite.rotate_sprite()

plater_sprites = [sailor_idle, sailor_anim1]

shart_y_spawn_pos = 600
shark_x_spawn_pos_list = [300, 600, 900]

active_sharks_list = []

last_time = 0
shark_spawn_delay = 3000

# The main function that controls the game
def main():
    looping = True
    startpos = 600
    xpos = startpos
    movementAmount = 300

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
    global last_time 
    WINDOW.fill(BACKGROUND)

    # === ADD: Render background ===
    BACKGROUND_IMAGE.render(WINDOW)

    player_pos = WINDOW.blit(sailor_idle.get_sprite(), (xpos, 200))
    currentanim_index += 1
    if currentanim_index >= len(plater_sprites):
        currentanim_index = 0
    animate_sailor(xpos, plater_sprites[currentanim_index])
    shark_spawner(player_pos)
    pygame.display.update()
    fpsClock.tick(FPS)


def shark_spawner(player_pos):
    current_time = pygame.time.get_ticks()
    global last_time
    global shark_spawn_delay

    

    if current_time - last_time >= shark_spawn_delay:
        if shark_spawn_delay < 250:
            shark_spawn_delay = shark_spawn_delay
        elif shark_spawn_delay < 1000:
            shark_spawn_delay -= 10
        else:
            shark_spawn_delay -= 100

        
        shark = Shark(-1, shark_x_spawn_pos_list[random.randint(0, len(shark_x_spawn_pos_list) -1)], shart_y_spawn_pos)
        active_sharks_list.append(shark)
        last_time = current_time

    for shark in active_sharks_list:
        shark_pos = WINDOW.blit(shark_sprite.get_sprite(), (shark.get_next_frame()[0], shark.get_next_frame()[1]))
       
        if player_pos.colliderect(shark_pos):
             pygame.quit()
             sys.exit()

def animate_sailor(xpos, currentSprite):
    print(currentSprite)
    WINDOW.blit(currentSprite.get_sprite(), (xpos, 200))


if __name__ == "__main__":
  main()


