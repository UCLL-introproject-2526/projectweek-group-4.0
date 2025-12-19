import pygame
import sys
from sprite import Sprite

pygame.init()

# -------------------- WINDOW --------------------
WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Options")

clock = pygame.time.Clock()

# -------------------- FONTS --------------------
FONT_PATH = "Assets/fonts/Pixel Game.otf"
OPTIONS_FONT = pygame.font.Font(FONT_PATH, 128)
OPTIONS_MEDIUM_FONT = pygame.font.Font(FONT_PATH, 90)
OPTIONS_SMALL_FONT = pygame.font.Font(FONT_PATH, 64)

# -------------------- COLORS --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (60, 140, 220)
GRAY = (180, 180, 180)

# -------------------- OUTLINED TEXT HELPER --------------------
def render_outlined_text(text, font, text_color, outline_color, outline_width=2):
    text_surf = font.render(text, True, text_color)
    w, h = text_surf.get_size()

    surf = pygame.Surface((w + outline_width * 2, h + outline_width * 2), pygame.SRCALPHA)

    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx != 0 or dy != 0:
                surf.blit(
                    font.render(text, True, outline_color),
                    (dx + outline_width, dy + outline_width)
                )

    surf.blit(text_surf, (outline_width, outline_width))
    return surf

# -------------------- SPRITES --------------------
mute_sprite = Sprite("Assets/Sprites/mute2.png", 450, 100)
fullscreen_sprite = Sprite("Assets/Sprites/fullscreen2.png", 450, 100)
window_sprite = Sprite("Assets/Sprites/window2.png", 450, 100)

mute_image = mute_sprite.get_sprite()
fullscreen_image = fullscreen_sprite.get_sprite()
window_image = window_sprite.get_sprite()

# -------------------- SCROLLING BACKGROUND --------------------
class ScrollingBackground:
    def __init__(self, path, tile_size, speed=0.3):
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

BG_IMAGE = ScrollingBackground("Assets/background/background3.png", (450, 250))

# -------------------- BUTTON SETUP --------------------
BUTTON_Y_START = HEIGHT // 2 + 150
BUTTON_SPACING = 125

mute_rect = mute_image.get_rect(center=(WIDTH // 2, BUTTON_Y_START))
fullscreen_rect = fullscreen_image.get_rect(center=(WIDTH // 2, BUTTON_Y_START + BUTTON_SPACING))
window_rect = window_image.get_rect(center=(WIDTH // 2, BUTTON_Y_START + BUTTON_SPACING))

HOVER_SCALE = 1.08
HOVER_TIME = 0.7

buttons = {
    "mute": {"image": mute_image, "rect": mute_rect, "scale": 1.0},
    "fullscreen": {"image": fullscreen_image, "rect": fullscreen_rect, "scale": 1.0},
    "window": {"image": window_image, "rect": window_rect, "scale": 1.0},
}

def draw_hover_button(screen, button, dt):
    target = HOVER_SCALE if button["rect"].collidepoint(pygame.mouse.get_pos()) else 1.0
    speed = (HOVER_SCALE - 1.0) / HOVER_TIME

    if button["scale"] < target:
        button["scale"] = min(button["scale"] + speed * dt, target)
    elif button["scale"] > target:
        button["scale"] = max(button["scale"] - speed * dt, target)

    img = button["image"]
    w, h = img.get_size()
    scaled = pygame.transform.smoothscale(img, (int(w * button["scale"]), int(h * button["scale"])))
    rect = scaled.get_rect(center=button["rect"].center)
    screen.blit(scaled, rect)

# -------------------- OPTIONS MENU --------------------
def options_menu(audio):
    global screen

    volume = audio.volume
    dragging = False
    fullscreen = False

    slider_width = 500
    slider_height = 10
    knob_w, knob_h = 20, 30
    slider_offset_y = 380

    while True:
        BG_IMAGE.render(screen)
        WIDTH, HEIGHT = screen.get_width(), screen.get_height()

        BUTTON_Y_START = HEIGHT // 2 + 150
        buttons["mute"]["rect"].center = (WIDTH // 2, BUTTON_Y_START)
        buttons["fullscreen"]["rect"].center = (WIDTH // 2, BUTTON_Y_START + BUTTON_SPACING)
        buttons["window"]["rect"].center = (WIDTH // 2, BUTTON_Y_START + BUTTON_SPACING)

        title = render_outlined_text("OPTIONS", OPTIONS_FONT, WHITE, BLACK, 4)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        vol_text = render_outlined_text(f"Volume: {int(volume * 100)}%", OPTIONS_MEDIUM_FONT, WHITE, BLACK, 3)
        screen.blit(vol_text, vol_text.get_rect(center=(WIDTH // 2, 250)))

        hint = render_outlined_text("LEFT / RIGHT or Drag Slider", OPTIONS_SMALL_FONT, WHITE, BLACK, 2)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 290)))

        esc = render_outlined_text("ESC to return", OPTIONS_SMALL_FONT, WHITE, BLACK, 2)
        screen.blit(esc, esc.get_rect(center=(WIDTH // 2, HEIGHT - 150)))

        slider_x = (WIDTH - slider_width) // 2
        slider_y = slider_offset_y
        slider_bg = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
        knob_x = slider_x + int(volume * slider_width) - knob_w // 2
        knob = pygame.Rect(knob_x, slider_y - 10, knob_w, knob_h)

        pygame.draw.rect(screen, GRAY, slider_bg)
        pygame.draw.rect(screen, BLUE, knob)

        active = "window" if fullscreen else "fullscreen"

        for key in buttons:
            if key == "mute" or key == active:
                draw_hover_button(screen, buttons[key], clock.get_time() / 1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RIGHT:
                    volume = min(1.0, volume + 0.05)
                    audio.set_master_volume(volume)
                if event.key == pygame.K_LEFT:
                    volume = max(0.0, volume - 0.05)
                    audio.set_master_volume(volume)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if knob.collidepoint(event.pos):
                    dragging = True
                if buttons["mute"]["rect"].collidepoint(event.pos):
                    audio.toggle_mute()
                if active == "fullscreen" and buttons["fullscreen"]["rect"].collidepoint(event.pos):
                    fullscreen = True
                    modes = pygame.display.list_modes()
                    screen = pygame.display.set_mode(modes[0], pygame.FULLSCREEN)
                elif active == "window" and buttons["window"]["rect"].collidepoint(event.pos):
                    fullscreen = False
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                volume = (event.pos[0] - slider_x) / slider_width
                volume = max(0.0, min(1.0, volume))
                audio.set_master_volume(volume)

        pygame.display.flip()
        clock.tick(60)
