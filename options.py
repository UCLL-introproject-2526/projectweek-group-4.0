import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Options")

clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 48)
SMALL_FONT = pygame.font.Font(None, 32)

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

    # Button dimensions
    button_width, button_height = 300, 60
    mute_offset_y = 470
    screen_offset_y = 560

    while True:
        # ----- DRAW SCROLLING BACKGROUND -----
        BG_IMAGE.render(screen)

        WIDTH, HEIGHT = screen.get_width(), screen.get_height()

        # ----- TEXT -----
        title = FONT.render("OPTIONS", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        vol_label = FONT.render(f"Volume: {int(volume * 100)}%", True, BLACK)
        screen.blit(vol_label, vol_label.get_rect(center=(WIDTH // 2, 250)))

        hint = SMALL_FONT.render("LEFT / RIGHT or Drag Slider", True, BLACK)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 290)))

        back_text = SMALL_FONT.render("ESC to return", True, BLACK)
        screen.blit(back_text, back_text.get_rect(center=(WIDTH // 2, HEIGHT - 150)))

        # ----- SLIDER -----
        slider_x = (WIDTH - slider_width) // 2
        slider_y = slider_offset_y
        slider_bg = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
        knob_x = slider_x + int(volume * slider_width) - knob_w // 2
        slider_knob = pygame.Rect(knob_x, slider_y - 10, knob_w, knob_h)

        pygame.draw.rect(screen, GRAY, slider_bg)
        pygame.draw.rect(screen, BLUE, slider_knob)

        # ----- BUTTONS -----
        mute_btn = pygame.Rect((WIDTH - button_width)//2, mute_offset_y, button_width, button_height)
        screen_btn = pygame.Rect((WIDTH - button_width)//2, screen_offset_y, button_width, button_height)

        mute_text = "UNMUTE" if audio.muted else "MUTE"
        screen_text = "WINDOWED" if fullscreen else "FULLSCREEN"

        pygame.draw.rect(screen, DARK, mute_btn, border_radius=8)
        pygame.draw.rect(screen, DARK, screen_btn, border_radius=8)

        screen.blit(FONT.render(mute_text, True, WHITE),
                    FONT.render(mute_text, True, WHITE).get_rect(center=mute_btn.center))
        screen.blit(FONT.render(screen_text, True, WHITE),
                    FONT.render(screen_text, True, WHITE).get_rect(center=screen_btn.center))

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
                if mute_btn.collidepoint(event.pos):
                    audio.toggle_mute()
                if screen_btn.collidepoint(event.pos):
                    fullscreen = not fullscreen
                    if fullscreen:
                        info = pygame.display.Info()
                        screen = pygame.display.set_mode(
                        (info.current_w, info.current_h),
                        pygame.FULLSCREEN
                        )
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                volume = (event.pos[0] - slider_x) / slider_width
                volume = max(0.0, min(1.0, volume))
                audio.set_master_volume(volume)

        pygame.display.flip()
        clock.tick(60)
