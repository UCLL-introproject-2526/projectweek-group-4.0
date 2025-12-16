
import pygame
import sys
from app import main
from sprite import Sprite

pygame.init()

WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drunken Sailor")

BLACK = (0, 0, 0)
BACKGROUND = (220, 220, 220)

MENU_FONT = pygame.font.Font(None, 40)

logo_sprite = Sprite("Assets/Sprites/oficial_logo_inv.png", 600, 400)
logo_image = logo_sprite.get_sprite()
logo_rect = logo_image.get_rect(center=(WIDTH // 2, HEIGHT // 3))

board_start_game_sprite = Sprite("Assets/Sprites/board_start_game.png", 200, 50)
board_start_game_image = board_start_game_sprite.get_sprite()

logo_sprite = Sprite(
    "Assets/Sprites/oficial_logo_inv.png",
    600,   # width
    400    # height
)
logo_image = logo_sprite.get_sprite()

board_start_game_sprite = Sprite(
    "Assets/Sprites/board_start_game.png",
    450,
    100
)
board_start_game_image = board_start_game_sprite.get_sprite()

board_options_sprite = Sprite(
    "Assets/Sprites/options.png",
    450,
    100
)
board_options_image = board_options_sprite.get_sprite()

board_quit_sprite = Sprite(
    "Assets/Sprites/quit.png",
    450,
    100
)
board_quit_image = board_quit_sprite.get_sprite()
# Text surfaces
logo_rect = logo_image.get_rect(center=(WIDTH // 2, HEIGHT // 3))
#start_text = MENU_FONT.render("Press ENTER to Start", True, BLACK)
#quit_text = MENU_FONT.render("Press ESC to Quit", True, BLACK)

# Text positions
#title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
BUTTON_Y_START = HEIGHT // 2 + 150
BUTTON_SPACING = 125

start_rect = board_start_game_image.get_rect(
    center=(WIDTH // 2, BUTTON_Y_START)
)

options_rect = board_options_image.get_rect(
    center=(WIDTH // 2, BUTTON_Y_START + BUTTON_SPACING)
)

quit_rect = board_quit_image.get_rect(
    center=(WIDTH // 2, BUTTON_Y_START + BUTTON_SPACING * 2)
)




clock = pygame.time.Clock()

class Background:
    def __init__(self, path: str, tile_size: tuple[int, int]):
        self._path = path
        self._tile_size = tile_size
        self._tile = self._load_tile()

    def _load_tile(self) -> pygame.Surface:
        try:
            img = pygame.image.load(self._path).convert_alpha()
            img = pygame.transform.smoothscale(img, self._tile_size)
            return img
        except Exception:
            surf = pygame.Surface(self._tile_size)
            surf.fill(BACKGROUND)
            return surf

    def render(self, surface: pygame.Surface):
        tile_w, tile_h = self._tile.get_size()
        screen_w, screen_h = surface.get_size()
        for x in range(0, screen_w, tile_w):
            for y in range(0, screen_h, tile_h):
                surface.blit(self._tile, (x, y))

BACKGROUND_IMAGE = Background("Assets/background/background3.png", (450, 250))

HOVER_SCALE = 1.08
HOVER_TIME = 0.7  # seconds

buttons = {
    "start": {
        "image": board_start_game_image,
        "rect": start_rect,
        "scale": 1.0,
    },
    "options": {
        "image": board_options_image,
        "rect": options_rect,
        "scale": 1.0,
    },
    "quit": {
        "image": board_quit_image,
        "rect": quit_rect,
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

def main_menu():
    while True:
        dt = clock.tick(60) / 100  # delta time in seconds

        BACKGROUND_IMAGE.render(screen)
        screen.blit(logo_image, logo_rect)

        draw_hover_button(screen, buttons["start"], dt)
        draw_hover_button(screen, buttons["options"], dt)
        draw_hover_button(screen, buttons["quit"], dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if buttons["start"]["rect"].collidepoint(event.pos):
                    return
                elif buttons["options"]["rect"].collidepoint(event.pos):
                    print("Options clicked")
                elif buttons["quit"]["rect"].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

main_menu()
main()