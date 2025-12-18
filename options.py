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


def options_menu(audio):
    global screen

    volume = audio.volume
    dragging = False
    fullscreen = False

    # Slider dimensions
    slider_width = 500
    slider_height = 10
    knob_w, knob_h = 20, 30
    slider_offset_y = 380  # vertical offset from top

    while True:
        # ----- DRAW SCROLLING BACKGROUND -----
        BG_IMAGE.render(screen)

        WIDTH, HEIGHT = screen.get_width(), screen.get_height()

        # ----- UPDATE BUTTON POSITIONS -----
        BUTTON_Y_START = HEIGHT // 2 + 150
        BUTTON_SPACING = 125

        buttons["mute"]["rect"].center = (WIDTH // 2, BUTTON_Y_START)
        buttons["fullscreen"]["rect"].center = (WIDTH // 2, BUTTON_Y_START + BUTTON_SPACING)
        buttons["window"]["rect"].center = (WIDTH // 2, BUTTON_Y_START + BUTTON_SPACING)

        # ----- TEXT -----
        title = OPTIONS_FONT.render("OPTIONS", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        vol_label = OPTIONS_MEDIUM_FONT.render(f"Volume: {int(volume * 100)}%", True, BLACK)
        screen.blit(vol_label, vol_label.get_rect(center=(WIDTH // 2, 250)))

        hint = OPTIONS_SMALL_FONT.render("LEFT / RIGHT or Drag Slider", True, BLACK)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 290)))

        back_text = OPTIONS_SMALL_FONT.render("ESC to return", True, BLACK)
        screen.blit(back_text, back_text.get_rect(center=(WIDTH // 2, HEIGHT - 150)))

        # ----- SLIDER -----
        slider_x = (WIDTH - slider_width) // 2
        slider_y = slider_offset_y
        slider_bg = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
        knob_x = slider_x + int(volume * slider_width) - knob_w // 2
        slider_knob = pygame.Rect(knob_x, slider_y - 10, knob_w, knob_h)

        pygame.draw.rect(screen, GRAY, slider_bg)
        pygame.draw.rect(screen, BLUE, slider_knob)

        # Decide which screen toggle button to show
        active_button = "window" if fullscreen else "fullscreen"

        # Draw buttons
        for key in buttons:
            if key == "mute" or key == active_button:
                draw_hover_button(screen, buttons[key], clock.get_time() / 1000)

        # ----- EVENTS -----
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
                if slider_knob.collidepoint(event.pos):
                    dragging = True
                if buttons["mute"]["rect"].collidepoint(event.pos):
                    audio.toggle_mute()
                if active_button == "fullscreen" and buttons["fullscreen"]["rect"].collidepoint(event.pos):
                    fullscreen = True
                    modes = pygame.display.list_modes()
                    screen = pygame.display.set_mode((modes[0][0], modes[0][1]), pygame.FULLSCREEN)
                elif active_button == "window" and buttons["window"]["rect"].collidepoint(event.pos):
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
