import pygame
import sys
from sprite import Sprite

pygame.init()

WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Options")

clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 48)
SMALL_FONT = pygame.font.Font(None, 32)

OPTIONS_FONT = pygame.font.Font("Assets/fonts/Pixel Game.otf", 128)
OPTIONS_MEDIUM_FONT = pygame.font.Font("Assets/fonts/Pixel Game.otf", 90)
OPTIONS_SMALL_FONT = pygame.font.Font("Assets/fonts/Pixel Game.otf", 64)

mute_sprite = Sprite(
    "Assets/Sprites/mute2.png",
    450,   # width
    100    # height
)
mute_image = mute_sprite.get_sprite()

fullscreen_sprite = Sprite(
    "Assets/Sprites/fullscreen2.png",
    450,   # width
    100    # height
)
fullscreen_image = fullscreen_sprite.get_sprite()

window_sprite = Sprite(
    "Assets/Sprites/window2.png",
    450,   # width
    100    # height
)
window_image = window_sprite.get_sprite()

BUTTON_Y_START = HEIGHT // 2 + 150
BUTTON_SPACING = 125

mute_rect = mute_image.get_rect(
    center=(WIDTH // 2, BUTTON_Y_START)
)

fullscreen_rect = fullscreen_image.get_rect(
    center=(WIDTH // 2, BUTTON_Y_START + BUTTON_SPACING)
)

window_rect = window_image.get_rect(
    center=(WIDTH // 2, BUTTON_Y_START + BUTTON_SPACING)
)

howtoplay = Sprite(
    "Assets/Sprites/howtoplay.png",
    1000,
    800
)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (60, 140, 220)
GRAY = (180, 180, 180)
DARK = (100, 100, 100)

# -------------------- SCROLLING BACKGROUND --------------------
class ScrollingBackground:
    def __init__(self, path, tile_size, speed=1.0):
        self.tile_size = tile_size
        self.speed = speed
        self.offset_x = 0

        try:
            img = pygame.image.load(path).convert_alpha()
            self.tile = pygame.transform.smoothscale(img, tile_size)
        except Exception:
            self.tile = pygame.Surface(tile_size)
            self.tile.fill((220, 220, 220))

    def render(self, surface):
        tile_w, tile_h = self.tile_size
        screen_w, screen_h = surface.get_size()

        # Scroll right to left
        self.offset_x = (self.offset_x - self.speed) % tile_w

        for x in range(-tile_w, screen_w + tile_w, tile_w):
            for y in range(0, screen_h + tile_h, tile_h):
                surface.blit(self.tile, (x - self.offset_x, y))

# Load background (replace with your tileable image path)
BG_IMAGE = ScrollingBackground("Assets/background/background3.png", (450, 250), speed=0.3)

HOVER_SCALE = 1.08
HOVER_TIME = 0.7  # seconds

buttons = {
    "mute": {
        "image": mute_image,
        "rect": mute_rect,
        "scale": 1.0,
    },
    "fullscreen": {
        "image": fullscreen_image,
        "rect": fullscreen_rect,
        "scale": 1.0,
    },
    "window": {
        "image": window_image,
        "rect": window_rect,
        "scale": 1.0,
    }
}

def draw_hover_button(screen, button, dt):
    target_scale = HOVER_SCALE if button["rect"].collidepoint(pygame.mouse.get_pos()) else 1.0

    # Smooth interpolation
    scale_speed = (HOVER_SCALE - 1.0) / HOVER_TIME
    if button["scale"] < target_scale:
        button["scale"] = min(button["scale"] + scale_speed * dt, target_scale)
    elif button["scale"] > target_scale:
        button["scale"] = max(button["scale"] - scale_speed * dt, target_scale)

    image = button["image"]
    w, h = image.get_size()
    scaled_image = pygame.transform.smoothscale(
        image,
        (int(w * button["scale"]), int(h * button["scale"]))
    )

    rect = scaled_image.get_rect(center=button["rect"].center)
    screen.blit(scaled_image, rect)


def howtoplay_menu():
    global screen

    while True:
        # ----- DRAW SCROLLING BACKGROUND -----
        BG_IMAGE.render(screen)

        WIDTH, HEIGHT = screen.get_width(), screen.get_height()

        # ----- UPDATE BUTTON POSITIONS -----
        BUTTON_Y_START = HEIGHT // 2 + 150
        BUTTON_SPACING = 125

        # ----- TEXT -----
        back_text = OPTIONS_SMALL_FONT.render("ESC to return", True, BLACK)
        screen.blit(back_text, back_text.get_rect(center=(WIDTH // 2, HEIGHT - 150)))


        screen.blit(howtoplay.get_sprite(), howtoplay.get_sprite().get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))

        # ----- EVENTS -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.flip()
        clock.tick(60)
