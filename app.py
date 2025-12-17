import pygame, sys, random
from pygame.locals import *
from sprite import Sprite
import highscore as hs

pygame.init()

BACKGROUND = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("My Game!")

FONT = pygame.font.SysFont("arial", 32)
BIG_FONT = pygame.font.SysFont("arial", 64)
CLOCK = pygame.time.Clock()

class Animations:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.drink_timer = 0
        self.shark_timer = 0
        self.idle_timer = 0
        self.idle_index = 0
        self.shark_index = 0
        self.player_idle = True

        self.idle = [
            Sprite("Assets/Sprites/player_idle_1.png", 50, 81),
            Sprite("Assets/Sprites/player_idle_2.png", 50, 81),
        ]
        self.drink = [
            Sprite("Assets/Sprites/player_drinking_1.png", 50, 81),
            Sprite("Assets/Sprites/player_drinking_2.png", 50, 81),
        ]

        self.sharks = [
            Sprite(f"Assets/Sprites/shark_swim_{i}.png", 100, 162)
            for i in range(1, 7)
        ]
        for s in self.sharks:
            s.rotate_sprite()

        self.player_img = self.idle[0]
        self.shark_img = self.sharks[0]

    def start_drink_anim(self):
        self.player_idle = False
        self.drink_timer = 0.55

    def update(self):
        if self.idle_timer <= 0 and self.player_idle:
            self.idle_index ^= 1
            self.player_img = self.idle[self.idle_index]
            self.idle_timer = 0.5

        if self.drink_timer <= 0:
            self.player_idle = True
        elif self.drink_timer > 0.3:
            self.player_img = self.drink[0]
        else:
            self.player_img = self.drink[1]

        if self.shark_timer <= 0:
            self.shark_img = self.sharks[self.shark_index]
            self.shark_index = (self.shark_index + 1) % len(self.sharks)
            self.shark_timer = 0.1

        dt = self.clock.tick(60) / 1000
        self.drink_timer = max(0, self.drink_timer - dt)
        self.idle_timer = max(0, self.idle_timer - dt)
        self.shark_timer = max(0, self.shark_timer - dt)

<<<<<<< HEAD
class Shark:
    def __init__(self, speed, x, y):
        self.speed = speed
        self.x = x
        self.y = y
=======
class ObjectInstanceData:
    def __init__(self, ypos_increment, xpos, ypos):
        self.ypos_increment = ypos_increment
        self.__xpos = xpos
        self.__ypos = ypos
>>>>>>> a3deccad8d56d6eafb179ed17c09103a28650379

    def move(self):
        self.y += self.speed
        return self.x, self.y

class Background:
    def __init__(self, path, size):
        self.tile = pygame.transform.smoothscale(
            pygame.image.load(path).convert_alpha(), size
        )

    def draw(self, surface):
        w, h = self.tile.get_size()
        sw, sh = surface.get_size()
        for x in range(0, sw, w):
            for y in range(0, sh, h):
                surface.blit(self.tile, (x, y))

background = Background("Assets/background/background3.png", (450, 250))

boat_sprite = Sprite("Assets/Sprites/Boat.png", 720, 290)
canon_sprite = Sprite("Assets/Sprites/Canon.png", 100, 100)
canonball_sprite = Sprite("Assets/Sprites/CanonBall.png", 50, 50)

anim = Animations()

shark_x_positions = [300, 600, 900]
active_sharks = []
active_cannonballs = []

last_shark_time = 0
last_ball_time = 0
spawn_delay =3000

<<<<<<< HEAD
def draw_score():
    txt = FONT.render(
        f"Score: {hs.get_current()}  High: {hs.get_high()}",
        True,
        BLACK,
=======

shart_y_spawn_pos = 800
shark_x_spawn_pos_list = [300, 600, 900]

active_sharks_list = []

active_cannonballs_list = []

last_time_shark_timer = 0
last_time_cannonball_timer = 0
shark_spawn_delay = 3000

current_lives = 3


fire_canon = False
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
    # ===== SCORE DISPLAY =====
    score_text = score_font.render(
        f"Score: {score_manager.current_score}", True, (0, 0, 0)
>>>>>>> a3deccad8d56d6eafb179ed17c09103a28650379
    )
    WINDOW.blit(txt, (20, 20))

def spawn_boat():
    boat = WINDOW.blit(boat_sprite.get_sprite(), (300, 130))
    for x in shark_x_positions:
        WINDOW.blit(canon_sprite.get_sprite(), (x, 225))
    boat.y -= 100
    return boat

def game_over_screen():
    while True:
        WINDOW.fill((20, 20, 20))

        title = BIG_FONT.render("GAME OVER", True, (200, 30, 30))
        score = FONT.render(f"Score: {hs.get_current()}", True, (255, 255, 255))
        high = FONT.render(f"High Score: {hs.get_high()}", True, (255, 255, 255))
        total = FONT.render(f"Total Points: {hs.get_total()}", True, (255, 255, 255))
        hint = FONT.render("ENTER = Restart | ESC = Quit", True, (180, 180, 180))

<<<<<<< HEAD
        y = 250
        for surf in (title, score, high, total, hint):
            WINDOW.blit(surf, (WINDOW_WIDTH // 2 - surf.get_width() // 2, y))
            y += 70
=======
def cannon_ball_spawner(sharkpos_list, current_time, xpos):
    global fire_canon
    global last_time_cannonball_timer 

    
    if current_time - last_time_cannonball_timer >= 900 and fire_canon == True:
        fire_canon = False
        cannon_ball = ObjectInstanceData(3, xpos + 25 , 255)
        active_cannonballs_list.append(cannon_ball)
        audio.Fire()
        last_time_cannonball_timer = current_time
>>>>>>> a3deccad8d56d6eafb179ed17c09103a28650379

        pygame.display.update()

<<<<<<< HEAD
        for event in pygame.event.get():
            if event.type == QUIT:
=======
        index = 0
        for sharkpos in sharkpos_list:
            if sharkpos.colliderect(cannonball_pos):
                active_cannonballs_list.remove(cannonball)
                sharkpos_list.pop(index)
                active_sharks_list.pop(index)

                score_manager.add_score(100)
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

        shark = ObjectInstanceData(-1, shark_x_spawn_pos_list[random.randint(0, len(shark_x_spawn_pos_list) -1)], shart_y_spawn_pos)
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
                score_manager.save_score()
>>>>>>> a3deccad8d56d6eafb179ed17c09103a28650379
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    hs.reset_current()
                    active_sharks.clear()
                    active_cannonballs.clear()
                    return

                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    global last_shark_time, last_ball_time, spawn_delay
    hs.reset_current()

    xpos = 600
    startpos = 600
    move = 300

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key in (K_a, K_LEFT, K_q) and xpos > startpos - move:
                    xpos -= move
                    anim.start_drink_anim()
                if event.key in (K_d, K_RIGHT) and xpos < startpos + move:
                    xpos += move
                    anim.start_drink_anim()

        WINDOW.fill(BACKGROUND)
        background.draw(WINDOW)

        boat = spawn_boat()
        anim.update()
        WINDOW.blit(anim.player_img.get_sprite(), (xpos, 200))

        now = pygame.time.get_ticks()

        if now - last_shark_time > spawn_delay:
            spawn_delay = max(150, spawn_delay - 120)
            active_sharks.append(
                Shark(-1, random.choice(shark_x_positions), 600)
            )
            last_shark_time = now

        shark_rects = []
        for shark in active_sharks[:]:
            rect = WINDOW.blit(anim.shark_img.get_sprite(), shark.move())
            shark_rects.append(rect)
            if boat.colliderect(rect):

                # ---- NEW HIGH SCORE SYSTEM ----
                hs.update_high_score()   # check if new high score
                hs.end_round()           # save score to file
                # -------------------------------

                game_over_screen()
                spawn_delay = 3000

        if now - last_ball_time > 900:
            active_cannonballs.append(Shark(3, xpos, 200))
            last_ball_time = now

        for ball in active_cannonballs[:]:
            ball_rect = WINDOW.blit(canonball_sprite.get_sprite(), ball.move())
            for i, srect in enumerate(shark_rects):
                if ball_rect.colliderect(srect):
                    hs.add_kill()
                    active_sharks.pop(i)
                    active_cannonballs.remove(ball)
                    break

        draw_score()
        pygame.display.update()
        CLOCK.tick(FPS)

if __name__ == "__main__":
    main()
