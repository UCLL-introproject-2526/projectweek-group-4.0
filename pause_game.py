import pygame
import sys

pygame.font.init()

# Fonts en kleuren
font_small = pygame.font.Font(None, 40)
TEXT_COLOR = (0, 0, 0)
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 80
BUTTON_SPACING = 50
OPTIONS_FONT = pygame.font.Font("Assets/fonts/Pixel Game.otf", 128)

def show_pause_screen(screen, restartgame, audio):
    """
    Toont pauze scherm met:
    - Resume knop
    - Restart knop
    - Quit knop (gaat terug naar main menu)
    """

    resume_img = pygame.image.load("Assets/Sprites/Resume.png").convert_alpha()
    resume_img = pygame.transform.scale(resume_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    restart_img = pygame.image.load("Assets/Sprites/Restart2.png").convert_alpha()
    restart_img = pygame.transform.scale(restart_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    quit_img = pygame.image.load("Assets/Sprites/quit.png").convert_alpha()
    quit_img = pygame.transform.scale(quit_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    screen_width, screen_height = screen.get_size()

    # Knoppen rects
    resume_rect = resume_img.get_rect(
        center=(screen_width // 2, screen_height // 2 - BUTTON_HEIGHT - BUTTON_SPACING // 2)
    )
    restart_rect = restart_img.get_rect(
        center=(screen_width // 2, screen_height // 2)
    )
    quit_rect = quit_img.get_rect(
        center=(screen_width // 2, screen_height // 2 + BUTTON_HEIGHT + BUTTON_SPACING // 2)
    )

    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 128))

        # ----- TEXT -----
        pause_text = OPTIONS_FONT.render("PAUSED", True, TEXT_COLOR)
        screen.blit(
            pause_text,
            (screen_width // 2 - pause_text.get_width() // 2, 150)
        )

        mouse_pos = pygame.mouse.get_pos()

        # ----- RESUME BUTTON -----
        screen.blit(resume_img, resume_rect)
        if resume_rect.collidepoint(mouse_pos):
            highlight = pygame.Surface(resume_rect.size, pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 50))
            screen.blit(highlight, resume_rect)

        # ----- RESTART BUTTON -----
        screen.blit(restart_img, restart_rect)
        if restart_rect.collidepoint(mouse_pos):
            highlight = pygame.Surface(restart_rect.size, pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 50))
            screen.blit(highlight, restart_rect)

        # ----- QUIT BUTTON -----
        screen.blit(quit_img, quit_rect)
        if quit_rect.collidepoint(mouse_pos):
            highlight = pygame.Surface(quit_rect.size, pygame.SRCALPHA)
            highlight.fill((255, 255, 255, 50))
            screen.blit(highlight, quit_rect)

        # ----- EVENTS -----
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
                    audio.StopMusic()
                    return "menu"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"

        pygame.display.flip()
        clock.tick(60)
