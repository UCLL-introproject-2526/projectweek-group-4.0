import pygame
import sys
from app import main

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
TITLE_FONT = pygame.font.Font(None, 80)
MENU_FONT = pygame.font.Font(None, 40)

# Text surfaces
title_text = TITLE_FONT.render("DRUNKEN SAILOR", True, BLACK)
start_text = MENU_FONT.render("Press ENTER to Start", True, BLACK)
quit_text = MENU_FONT.render("Press ESC to Quit", True, BLACK)

# Text positions
title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

# Clock
clock = pygame.time.Clock()

def main_menu():
    while True:
        screen.fill(WHITE)

        # Draw text
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()  # replace with game loop later
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

# Run menu
main_menu()
