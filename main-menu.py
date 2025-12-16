
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
start_rect = board_start_game_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

quit_text = MENU_FONT.render("Press ESC to Quit", True, BLACK)
quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

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

def main_menu():
    while True:
        BACKGROUND_IMAGE.render(screen)
        screen.blit(logo_image, logo_rect)
        screen.blit(board_start_game_image, start_rect)
        screen.blit(quit_text, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_rect.collidepoint(event.pos):
                    main()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
   main_menu()