import pygame
import sys
from app import main
from sprite import Sprite

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drunken Sailor")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
TITLE_FONT = pygame.font.Font(None, 80)
MENU_FONT = pygame.font.Font(None, 40)

logo_sprite = Sprite(
    "Assets/Sprites/oficial_logo_inv.png",
    600,   # width
    400    # height
)
logo_image = logo_sprite.get_sprite()

board_start_game_sprite = Sprite(
    "Assets/Sprites/board_start_game.png",
    200,
    50
)
board_start_game_image = board_start_game_sprite.get_sprite()
# Text surfaces
logo_rect = logo_image.get_rect(center=(WIDTH // 2, HEIGHT // 3))
#start_text = MENU_FONT.render("Press ENTER to Start", True, BLACK)
quit_text = MENU_FONT.render("Press ESC to Quit", True, BLACK)

# Text positions
#title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
start_rect = board_start_game_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

# Clock
clock = pygame.time.Clock()
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

def main_menu():
    while True:
        BACKGROUND_IMAGE.render(screen)

        # Draw text
        screen.blit(logo_image, logo_rect)
        screen.blit(board_start_game_image, start_rect)
        screen.blit(quit_text, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # replace with game loop later
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)



# Run menu
main_menu()
main()
