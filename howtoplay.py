import pygame
import sys
from sprite import Sprite

pygame.init()
pygame.font.init()

# -------------------- Fonts --------------------
FONT_PATH = "Assets/fonts/Pixel Game.otf"  # custom font
OPTIONS_FONT = pygame.font.Font(FONT_PATH, 128)
OPTIONS_MEDIUM_FONT = pygame.font.Font(FONT_PATH, 90)
OPTIONS_SMALL_FONT = pygame.font.Font(FONT_PATH, 64)

# -------------------- Colors & Buttons --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (60, 140, 220)
GRAY = (180, 180, 180)
DARK = (100, 100, 100)

# -------------------- Screen --------------------
WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("How to Play")
clock = pygame.time.Clock()

# -------------------- Sprites --------------------
howtoplay = Sprite("Assets/Sprites/howtoplay.png", 1000, 800)

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
        self.offset_x = (self.offset_x - self.speed) % tile_w
        for x in range(-tile_w, screen_w + tile_w, tile_w):
            for y in range(0, screen_h + tile_h, tile_h):
                surface.blit(self.tile, (x - self.offset_x, y))

BG_IMAGE = ScrollingBackground("Assets/background/background3.png", (450, 250), speed=0.3)

# -------------------- Outline Text Function --------------------
def render_text_outline(text, font, text_color, outline_color, outline_width=2):
    base = font.render(text, True, text_color)
    size = (base.get_width() + 2 * outline_width, base.get_height() + 2 * outline_width)
    surface = pygame.Surface(size, pygame.SRCALPHA)

    # Draw outline
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                surface.blit(font.render(text, True, outline_color), (dx + outline_width, dy + outline_width))
    # Draw main text
    surface.blit(base, (outline_width, outline_width))
    return surface

# -------------------- How To Play Menu --------------------
def howtoplay_menu():
    global screen

    while True:
        # ----- DRAW SCROLLING BACKGROUND -----
        BG_IMAGE.render(screen)

        WIDTH, HEIGHT = screen.get_width(), screen.get_height()

        # ----- TEXT -----
        back_text_surf = render_text_outline("ESC to return", OPTIONS_SMALL_FONT, WHITE, BLACK, outline_width=3)
        screen.blit(back_text_surf, back_text_surf.get_rect(center=(WIDTH // 2, HEIGHT - 150)))

        howtoplay_surf = howtoplay.get_sprite()
        screen.blit(howtoplay_surf, howtoplay_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))

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
