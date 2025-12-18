import pygame
import sys
import audio

pygame.font.init()

# Fonts en kleuren
font_large = pygame.font.Font(None, 80)
font_small = pygame.font.Font(None, 40)
TEXT_COLOR = (255, 255, 255)
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 80
BUTTON_SPACING = 50

def show_game_over_screen(screen, current_score, high_score, init_game):
    """
    Toont game over scherm met:
    - Restart knop (afbeelding)
    - Quit knop (afbeelding)
    - Scores
    """
    restart_img = pygame.image.load("Assets/Sprites/Restart.png").convert_alpha()
    restart_img = pygame.transform.scale(restart_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    quit_img = pygame.image.load("Assets/Sprites/quit.png").convert_alpha()
    quit_img = pygame.transform.scale(quit_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    audio_instance = audio.Audio()
    audio_instance.Death()

    screen_width, screen_height = screen.get_size()
    running = True

    restart_rect = restart_img.get_rect(center=(screen_width//2, screen_height//2))
    quit_rect = quit_img.get_rect(center=(screen_width//2, screen_height//2 + BUTTON_HEIGHT + BUTTON_SPACING//2))

    clock = pygame.time.Clock()

    while running:
        screen.fill((0, 0, 128))

        # Tekst: GAME OVER
        game_over_text = font_large.render("GAME OVER", True, TEXT_COLOR)
        screen.blit(game_over_text, (screen_width//2 - game_over_text.get_width()//2, 100))

        # Tekst: Scores
        current_score_text = font_small.render(f"Score: {current_score}", True, TEXT_COLOR)
        high_score_text = font_small.render(f"High Score: {high_score}", True, TEXT_COLOR)
        screen.blit(current_score_text, (screen_width//2 - current_score_text.get_width()//2, 250))
        screen.blit(high_score_text, (screen_width//2 - high_score_text.get_width()//2, 300))

        mouse_pos = pygame.mouse.get_pos()

        # Restart knop hover
        if restart_rect.collidepoint(mouse_pos):
            highlight = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 50))
            screen.blit(restart_img, restart_rect)
            screen.blit(highlight, restart_rect)
        else:
            screen.blit(restart_img, restart_rect)

        # Quit knop hover
        if quit_rect.collidepoint(mouse_pos):
            highlight = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 50))
            screen.blit(quit_img, quit_rect)
            screen.blit(highlight, quit_rect)
        else:
            screen.blit(quit_img, quit_rect)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect.collidepoint(event.pos):
                    audio_instance.StopMusic()
                    audio_instance.PlayMusic()
                    init_game()
                    return "restart"
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)
