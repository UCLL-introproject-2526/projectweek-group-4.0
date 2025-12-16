
import pygame, sys, random
from pygame.locals import *
from sprite import Sprite
from audio import Audio

pygame.init()
 
# Colours
BACKGROUND = (255, 255, 255)

FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')


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
# sailor_idle = Sprite("Assets/Sprites/Sailor.png", 50, 81)
# sailor_anim1 = Sprite("Assets/Sprites/Sailor1.png", 50, 81)
boat_sprite = Sprite("Assets/Sprites/Boat.png", 720, 290)
shark_sprite = Sprite("Assets/Sprites/Shark.png", 100, 162)
canonball_sprite=Sprite("Assets/Sprites/CanonBall.png",50,50)
canon_sprite=Sprite("Assets/Sprites/Canon.png",100,100)
shark_sprite.rotate_sprite()

anim = Animations()

audio = Audio(volume=1.0)

shart_y_spawn_pos = 600
shark_x_spawn_pos_list = [300, 600, 900]

active_sharks_list = []

active_cannonballs_list = []

last_time_shark_timer = 0
last_time_cannonball_timer = 0
shark_spawn_delay = 3000

current_lives = 3

# The main function that controls the game
def main():
    looping = True
    startpos = 600
    xpos = startpos
    movementAmount = 300
    # The main game loop
    while looping:
        # Get inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_a or event.key== K_LEFT or event.key== K_q:
                    if xpos > startpos - movementAmount:
                        xpos -= movementAmount
                        anim.start_drink_anim()
                if event.key == K_d or event.key== K_RIGHT:
                    if xpos < startpos + movementAmount:
                        xpos += movementAmount 
                        anim.start_drink_anim()

        draw_window(xpos)

def draw_window(xpos):
    global last_time_shark_timer 
    WINDOW.fill(BACKGROUND)

    # === ADD: Render background ===
    BACKGROUND_IMAGE.render(WINDOW)
    boat_pos = spawn_boat()
    anim.handle_animations()
    player_sprite = anim.get_player_img()
    WINDOW.blit(player_sprite, (xpos, 200))
    current_time = pygame.time.get_ticks()


    shark_spawner(boat_pos, current_time, xpos)
    pygame.display.update()
    fpsClock.tick(FPS)


def spawn_boat():
    boat_pos = WINDOW.blit(boat_sprite.get_sprite(), (300, 130))
    WINDOW.blit(canon_sprite.get_sprite(), (300, 225))
    WINDOW.blit(canon_sprite.get_sprite(), (600, 225))
    WINDOW.blit(canon_sprite.get_sprite(), (900, 225))

    boat_pos.y -= 100
    return boat_pos


def cannon_ball_spawner(sharkpos_list, current_time, xpos):
    global last_time_cannonball_timer 
    
    if current_time - last_time_cannonball_timer >= 900:
        shark = Shark(3, xpos , 200)
        active_cannonballs_list.append(shark)
        audio.Fire()
        last_time_cannonball_timer = current_time

    for cannonball in active_cannonballs_list:
        cannonball_pos = WINDOW.blit(canonball_sprite.get_sprite(), (cannonball.get_next_frame()[0], cannonball.get_next_frame()[1]))

        index = 0
        for sharkpos in sharkpos_list:
            if sharkpos.colliderect(cannonball_pos):
                active_cannonballs_list.remove(cannonball)
                sharkpos_list.pop(index)
                active_sharks_list.pop(index)
            index += 1



def shark_spawner(boat_pos, current_time, xpos):
    global last_time_shark_timer
    global shark_spawn_delay

    

    if current_time - last_time_shark_timer >= shark_spawn_delay:
        if shark_spawn_delay < 250:
            shark_spawn_delay = shark_spawn_delay
        elif shark_spawn_delay < 1000:
            shark_spawn_delay -= 10
        else:
            shark_spawn_delay -= 100

        shark = Shark(-1, shark_x_spawn_pos_list[random.randint(0, len(shark_x_spawn_pos_list) -1)], shart_y_spawn_pos)
        active_sharks_list.append(shark)
        last_time_shark_timer = current_time

    shark_pos_list = []

    global current_lives

    for shark in active_sharks_list:
        shark_pos = WINDOW.blit(anim.get_shark_img(), (shark.get_next_frame()[0], shark.get_next_frame()[1]))
        
        if boat_pos.colliderect(shark_pos):
            current_lives -= 1
            active_sharks_list.remove(shark)
            if current_lives <= 0:
                pygame.quit()
                sys.exit() 

        shark_pos_list.append(shark_pos)


    cannon_ball_spawner(shark_pos_list, current_time, xpos)

def animate_sailor(xpos, currentSprite):
    print(currentSprite)
    WINDOW.blit(currentSprite.get_sprite(), (xpos, 200))


if __name__ == "__main__":
  main()


