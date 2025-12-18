import pygame
import sys

pygame.font.init()

# Fonts en kleuren
font_small = pygame.font.Font(None, 40)
TEXT_COLOR = (255, 255, 255)
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 80
BUTTON_SPACING = 50

def show_pause_screen(screen, restartgame, audio):
    """
    Toont pauze scherm met:
    - Resume knop (afbeelding)
    - Restart knop (afbeelding)
    - Quit knop (afbeelding)
    """
    resume_img = pygame.image.load("Assets/Sprites/Resume.png").convert_alpha()
    resume_img = pygame.transform.scale(resume_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    restart_img = pygame.image.load("Assets/Sprites/Restart.png").convert_alpha()
    restart_img = pygame.transform.scale(restart_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    quit_img = pygame.image.load("Assets/Sprites/quit.png").convert_alpha()
    quit_img = pygame.transform.scale(quit_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    screen_width, screen_height = screen.get_size()
    running = True

    # Knoppen rects
    resume_rect = resume_img.get_rect(center=(screen_width//2, screen_height//2 - BUTTON_HEIGHT - BUTTON_SPACING//2))
    restart_rect = restart_img.get_rect(center=(screen_width//2, screen_height//2))
    quit_rect = quit_img.get_rect(center=(screen_width//2, screen_height//2 + BUTTON_HEIGHT + BUTTON_SPACING//2))

    clock = pygame.time.Clock()

    while running:
        screen.fill((0, 0, 128))

        # Tekst: PAUSED
        pause_text = pygame.font.Font(None, 80).render("PAUSED", True, TEXT_COLOR)
        screen.blit(pause_text, (screen_width//2 - pause_text.get_width()//2, 150))

        mouse_pos = pygame.mouse.get_pos()

        # Resume knop hover
        if resume_rect.collidepoint(mouse_pos):
            highlight = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 50))
            screen.blit(resume_img, resume_rect)
            screen.blit(highlight, resume_rect)
        else:
            screen.blit(resume_img, resume_rect)

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_rect.collidepoint(event.pos):
                    return "resume"
                elif restart_rect.collidepoint(event.pos):
                    audio.StopMusic()
                    restartgame()
                    return "restart"
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"

        pygame.display.flip()
        clock.tick(60)
