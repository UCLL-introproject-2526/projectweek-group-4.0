
import pygame, sys, random
from pygame.locals import *
from sprite import Sprite
from audio import Audio
from scores import ScoreManager
from upgrades import UpgradeSystem
from animations import Animations

pygame.init()

# Colours
BACKGROUND = (255, 255, 255)

FPS = 60
fpsClock = pygame.time.Clock()
#WINDOW_WIDTH = 1200
#WINDOW_HEIGHT = 1000

#WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
GAME_WIDTH = 1200
GAME_HEIGHT = 800

WINDOW = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
GAME_SURFACE = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('My Game!')
score_font = pygame.font.Font(None, 36)

class ObjectInstanceData:
    def __init__(self, ypos_increment, xpos, ypos):
        self.ypos_increment = ypos_increment
        self.__xpos = xpos
        self.__ypos = ypos

    def get_next_frame(self):
        self.__ypos += self.ypos_increment
        return (self.__xpos, self.__ypos)
    
class Enemy:
    def __init__(self, objectinstnace, anim_function, health_amount):
        self.__object_instance = objectinstnace
        self.__anim_function = anim_function
        self.__health_amount = health_amount

    def get_anim(self):
        return self.__anim_function()
    
    def get_next_frame(self):
        return self.__object_instance.get_next_frame()
    
    def check_alive(self):
        self.__health_amount -= 1
        print(self.__health_amount)
        if self.__health_amount <= 0:
            return False
        
        return True

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

score_manager = ScoreManager()

upgrade_system = UpgradeSystem()


shart_y_spawn_pos = 800
shark_x_spawn_pos_list = [300, 600, 900]

active_sharks_list = []

active_orca_list = []

active_cannonballs_list = []

shark_speed = 1

last_time_shark_timer = 0
last_time_cannonball_timer = 0
shark_spawn_delay = 2100

current_lives = 3


fire_canon = False

def scale_surface_to_screen(surface, screen):
    sw, sh = surface.get_size()
    ww, wh = screen.get_size()

    scale = min(ww / sw, wh / sh)

    new_w = int(sw * scale)
    new_h = int(sh * scale)

    scaled_surface = pygame.transform.smoothscale(surface, (new_w, new_h))

    offset_x = (ww - new_w) // 2
    offset_y = (wh - new_h) // 2

    return scaled_surface, offset_x, offset_y
# The main function that controls the game
def main():
    score_manager.reset_score()
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
                if event.key == K_SPACE:
                    global fire_canon
                    fire_canon = True
                    anim.__firetimer = 0
                if event.key == K_u or event.key == K_v:
                    upgrade_system.upgrade(anim, audio)

        draw_window(xpos)

def draw_window(xpos):
    global last_time_shark_timer 
    GAME_SURFACE.fill(BACKGROUND)

    # === ADD: Render background ===
    BACKGROUND_IMAGE.render(GAME_SURFACE)
    boat_pos = spawn_boat()
    anim.handle_animations()
    
    player_sprite = anim.get_player_img()
    GAME_SURFACE.blit(player_sprite, (xpos, 135))
    GAME_SURFACE.blit(anim.get_parrot_img(), (boat_pos.x + 150, 105))
    current_time = pygame.time.get_ticks()


    shark_spawner(boat_pos, current_time, xpos)
    # ===== UI =====
    game_ui()
    # =========================
     # ---- CENTER GAME SURFACE ----
    window_w, window_h = WINDOW.get_size()
    offset_x = (window_w - GAME_WIDTH) // 2
    offset_y = (window_h - GAME_HEIGHT) // 2

    WINDOW.fill((0, 0, 0))

    scaled_game, ox, oy = scale_surface_to_screen(GAME_SURFACE, WINDOW)
    WINDOW.blit(scaled_game, (ox, oy))

    pygame.display.update()
    fpsClock.tick(FPS)

def game_ui():
    score_text = score_font.render(
    f"Score: {score_manager.current_score}", True, (0, 0, 0)
    )
    high_score_text = score_font.render(
        f"High Score: {score_manager.high_score}", True, (0, 0, 0)
    )

    coin_text = score_font.render(
        f"Coins: {upgrade_system.get_current_gold_amount()}", True, (0, 0, 0)
    )

    GAME_SURFACE.blit(score_text, (20, 20))
    GAME_SURFACE.blit(high_score_text, (20, 60))
    GAME_SURFACE.blit(coin_text, (1000,100))

def spawn_boat():
    screen_width = GAME_WIDTH
    boat_pos = GAME_SURFACE.blit(
        boat_sprite.get_sprite(),
        (screen_width * 0.25, 65)
    )
    cannon_sprite = upgrade_system.get_current_cannon_spirte().get_sprite()
    GAME_SURFACE.blit(cannon_sprite, (boat_pos.x, 160))
    GAME_SURFACE.blit(cannon_sprite, (boat_pos.x + 300, 160))
    GAME_SURFACE.blit(cannon_sprite, (boat_pos.x + 600, 160))

    boat_pos.y -= 100
    return boat_pos


def cannon_ball_spawner(sharkpos_list, current_time, xpos):
    global fire_canon
    global last_time_cannonball_timer 

    smoke_animation(xpos , 155)
    particle_animation()

    if current_time - last_time_cannonball_timer >= upgrade_system.get_time_between_cannonfire() and fire_canon == True:
        fire_canon = False
        cannon_ball = ObjectInstanceData(5, xpos + 25 , 255)
        active_cannonballs_list.append(cannon_ball)
        audio.Fire()
        last_time_cannonball_timer = current_time

        anim.cannon_fire_anim()

    for cannonball in active_cannonballs_list:
        cannonball_pos = GAME_SURFACE.blit(canonball_sprite.get_sprite(), (cannonball.get_next_frame()[0], cannonball.get_next_frame()[1]))

        index = 0
        for sharkpos in sharkpos_list:
            if sharkpos.colliderect(cannonball_pos):
                active_cannonballs_list.remove(cannonball)
                if not active_sharks_list[index].check_alive():
                    sharkpos_list.pop(index)
                    active_sharks_list.pop(index)

                    score_manager.add_score(100)
                    upgrade_system.add_gold(50)
            index += 1

def smoke_animation(x, y):
    GAME_SURFACE.blit(anim.get_smoke_img(), (x, y))

def particle_animation():
    GAME_SURFACE.blit(anim.get_upgrade_particle_img(), (250, 115))
    GAME_SURFACE.blit(anim.get_upgrade_particle_img(), (550, 115))
    GAME_SURFACE.blit(anim.get_upgrade_particle_img(), (850, 115))

def shark_spawner(boat_pos, current_time, xpos):
    global last_time_shark_timer
    global shark_spawn_delay
    global shark_speed
    

    if current_time - last_time_shark_timer >= shark_spawn_delay:
        if shark_spawn_delay < 180:
            shark_spawn_delay = shark_spawn_delay
        elif shark_spawn_delay < 1000:
            shark_spawn_delay -= 10
            #shark_speed + 0.5
        elif shark_spawn_delay < 1600:
            shark_speed += 0.02
            shark_spawn_delay -= 25
        else:
            shark_spawn_delay -= 90
            shark_speed += 0.05


        random_chance = random.randint(0, 1000)

        if(random_chance > 130):
            shark = Enemy(ObjectInstanceData(-shark_speed, shark_x_spawn_pos_list[random.randint(0, len(shark_x_spawn_pos_list) -1)], 
                                         shart_y_spawn_pos), anim.get_shark_img, 1)
        else:
            shark = Enemy(ObjectInstanceData(-shark_speed, shark_x_spawn_pos_list[random.randint(0, len(shark_x_spawn_pos_list) -1)], 
                                         shart_y_spawn_pos), anim.get_orca_img, 2)
        active_sharks_list.append(shark)
        last_time_shark_timer = current_time

    shark_pos_list = []

    global current_lives

    for shark in active_sharks_list:
        shark_pos = GAME_SURFACE.blit(shark.get_anim(), (shark.get_next_frame()[0], shark.get_next_frame()[1]))
        
        if boat_pos.colliderect(shark_pos):
            current_lives -= 1
            active_sharks_list.remove(shark)
            if current_lives <= 0:
                score_manager.save_score()
                pygame.quit()
                sys.exit() 

        shark_pos_list.append(shark_pos)


    cannon_ball_spawner(shark_pos_list, current_time, xpos)

def animate_sailor(xpos, currentSprite):
    print(currentSprite)
    GAME_SURFACE.blit(currentSprite.get_sprite(), (xpos, 200))

def upgrade_popup():
    GAME_SURFACE.blit(upgrade_message_sprite.get_sprite(), (500, 300))

if __name__ == "__main__":
    main()