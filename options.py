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
GRAY = (180, 180, 180)

def options_menu(audio):
    volume = audio.volume
    dragging = False

    # Slider setup
    slider_x = 350
    slider_y = 400
    slider_width = 500
    slider_height = 10

    knob_width = 20
    knob_height = 30

    while True:
        screen.fill((220, 220, 220))

        # ---- TEXT ----
        title = FONT.render("OPTIONS", True, BLACK)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        vol_text = FONT.render(f"Volume: {int(volume * 100)}%", True, BLACK)
        screen.blit(vol_text, vol_text.get_rect(center=(WIDTH // 2, 250)))

        hint = SMALL_FONT.render("LEFT / RIGHT or Drag Slider", True, BLACK)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 300)))

        back_text = SMALL_FONT.render("ESC to return", True, BLACK)
        screen.blit(back_text, back_text.get_rect(center=(WIDTH // 2, 800)))

        # ---- SLIDER ----
        slider_bg = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
        knob_x = slider_x + int(volume * slider_width) - knob_width // 2
        slider_knob = pygame.Rect(knob_x, slider_y - 10, knob_width, knob_height)

        pygame.draw.rect(screen, GRAY, slider_bg)
        pygame.draw.rect(screen, BLUE, slider_knob)

        # ---- EVENTS ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_RIGHT:
                    volume = min(1.0, volume + 0.05)
                    audio.set_master_volume(volume)

                if event.key == pygame.K_LEFT:
                    volume = max(0.0, volume - 0.05)
                    audio.set_master_volume(volume)

            # Mouse controls
            if event.type == pygame.MOUSEBUTTONDOWN:
                if slider_knob.collidepoint(event.pos):
                    dragging = True

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                mouse_x = event.pos[0]
                volume = (mouse_x - slider_x) / slider_width
                volume = max(0.0, min(1.0, volume))
                audio.set_master_volume(volume)

        pygame.display.flip()
        clock.tick(60)

