import pygame
import sys

pygame.init()
pygame.font.init()

# -------------------- Fonts --------------------
FONT_PATH = "Assets/fonts/Pixel Game.otf"  # custom font uit options.py
font_title = pygame.font.Font(FONT_PATH, 100)
font_score = pygame.font.Font(FONT_PATH, 50)

# -------------------- Colors & Buttons --------------------
TEXT_COLOR = (255, 0, 0)
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 80
BUTTON_SPACING = 40

HOVER_SCALE = 1.1
HOVER_TIME = 0.1  # seconden

# -------------------- SCROLLING BACKGROUND --------------------
class ScrollingBackground:
    def __init__(self, path, tile_size=(450, 250), speed=20):
        self.speed = speed  # pixels per seconde
        self.tile_size = tile_size
        self.offset_x = 0

        try:
            img = pygame.image.load(path).convert_alpha()
            self.tile = pygame.transform.smoothscale(img, tile_size)
            self.tile_width, self.tile_height = self.tile.get_size()
        except Exception:
            self.tile = pygame.Surface(tile_size)
            self.tile.fill((220, 220, 220))
            self.tile_width, self.tile_height = self.tile.get_size()

    def render(self, surface, dt):
        screen_w, screen_h = surface.get_size()
        self.offset_x = (self.offset_x + self.speed * dt) % self.tile_width
        for x in range(-self.tile_width, screen_w + self.tile_width, self.tile_width):
            for y in range(0, screen_h + self.tile_height, self.tile_height):
                surface.blit(self.tile, (x - self.offset_x, y))

# -------------------- Game Over Scherm --------------------
def show_game_over_screen(screen, current_score, high_score, init_game):
    screen_width, screen_height = screen.get_size()
    clock = pygame.time.Clock()
    running = True

    # Achtergrond
    BG = ScrollingBackground("Assets/background/background3.png", speed=20)  # trage achtergrond

    # Knoppen
    restart_img = pygame.image.load("Assets/Sprites/Restart2.png").convert_alpha()
    restart_img = pygame.transform.scale(restart_img, (BUTTON_WIDTH, BUTTON_HEIGHT))
    quit_img = pygame.image.load("Assets/Sprites/quit.png").convert_alpha()
    quit_img = pygame.transform.scale(quit_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    restart_button = {
        "image": restart_img,
        "rect": restart_img.get_rect(center=(screen_width//2, screen_height//2 + 50)),
        "scale": 1.0
    }
    quit_button = {
        "image": quit_img,
        "rect": quit_img.get_rect(center=(screen_width//2, screen_height//2 + 50 + BUTTON_HEIGHT + BUTTON_SPACING)),
        "scale": 1.0
    }

    # Hover animatie
    def draw_hover_button(button, dt):
        target_scale = HOVER_SCALE if button["rect"].collidepoint(pygame.mouse.get_pos()) else 1.0
        scale_speed = (HOVER_SCALE - 1.0) / HOVER_TIME

        if button["scale"] < target_scale:
            button["scale"] = min(button["scale"] + scale_speed * dt, target_scale)
        elif button["scale"] > target_scale:
            button["scale"] = max(button["scale"] - scale_speed * dt, target_scale)

        image = button["image"]
        w, h = image.get_size()
        scaled_image = pygame.transform.smoothscale(image, (int(w * button["scale"]), int(h * button["scale"])))
        rect = scaled_image.get_rect(center=button["rect"].center)
        screen.blit(scaled_image, rect)

    while running:
        dt = clock.tick(60) / 1000  # delta tijd in seconden

        # Achtergrond renderen
        BG.render(screen, dt)

        # Titel en scores
        title_text = font_title.render("GAME OVER", True, TEXT_COLOR)
        score_text = font_score.render(f"Score: {current_score}", True, TEXT_COLOR)
        high_score_text = font_score.render(f"High Score: {high_score}", True, TEXT_COLOR)

        screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, screen_height//4 - 50))
        screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, screen_height//2 - 100))
        screen.blit(high_score_text, (screen_width//2 - high_score_text.get_width()//2, screen_height//2 - 50))

        # Knoppen tekenen met hover
        draw_hover_button(restart_button, dt)
        draw_hover_button(quit_button, dt)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button["rect"].collidepoint(event.pos):
                    init_game()
                    return "restart"
                elif quit_button["rect"].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
