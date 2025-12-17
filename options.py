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
BLUE = (50, 120, 200)

def options_menu(audio):
    volume = audio.volume

    while True:
        screen.fill((220, 220, 220))

        # ---- TEXT ----
        title = FONT.render("OPTIONS", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH//2, 100)))

        vol_text = FONT.render(f"Volume: {int(volume * 100)}%", True, BLACK)
        screen.blit(vol_text, vol_text.get_rect(center=(WIDTH//2, 250)))

        hint = SMALL_FONT.render("LEFT / RIGHT to change volume", True, BLACK)
        screen.blit(hint, hint.get_rect(center=(WIDTH//2, 300)))

        back_text = SMALL_FONT.render("ESC to return", True, BLACK)
        screen.blit(back_text, back_text.get_rect(center=(WIDTH//2, 800)))

        # ---- SIMPLE SLIDER ----
        slider_bg = pygame.Rect(350, 400, 500, 10)
        slider_knob = pygame.Rect(350 + int(volume * 500) - 10, 390, 20, 30)

        pygame.draw.rect(screen, BLACK, slider_bg)
        pygame.draw.rect(screen, BLUE, slider_knob)

        # ---- EVENTS ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # go back

                if event.key == pygame.K_RIGHT:
                    volume = min(1.0, volume + 0.05)
                    audio.set_master_volume(volume)

                if event.key == pygame.K_LEFT:
                    volume = max(0.0, volume - 0.05)
                    audio.set_master_volume(volume)

        pygame.display.flip()
        clock.tick(60)
