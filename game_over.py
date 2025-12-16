
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def render_game_over(surface: pygame.Surface, message: str = "Game Over! De haai raakte de boot.") -> pygame.Rect:
    """
    Teken een grote game-over boodschap gecentreerd op het scherm.

    :param surface: Het pygame Surface (bv. je WINDOW) waar op getekend wordt.
    :param message: De te tonen tekst.
    :return: De pygame.Rect van de getekende tekst (handig voor verdere logica of testen).
    """
    width, height = surface.get_size()

    # Maak semitransparante overlay
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 200))  # licht wit, alpha=200
    surface.blit(overlay, (0, 0))

    # Fonts (val terug op default als None)
    title_font = pygame.font.Font(None, 100)
    info_font = pygame.font.Font(None, 40)

    # Hoofdtekst
    title_surf = title_font.render(message, True, BLACK)
    title_rect = title_surf.get_rect(center=(width // 2, height // 2 - 40))
    surface.blit(title_surf, title_rect)

    # Subtekst
    info_surf = info_font.render("Druk op ENTER om opnieuw te starten of ESC om te sluiten", True, BLACK)
    info_rect = info_surf.get_rect(center=(width // 2, height // 2 + 40))
    surface.blit(info_surf, info_rect)

    return title_rect

def wait_for_quit_or_restart() -> str:
    """
    Wacht op ENTER (restart) of ESC/QUIT (quit). Geeft 'restart' of 'quit' terug.
    Gebruik dit na render_game_over() in je main loop.
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'quit'
                if event.key == pygame.K_r:
                    return 'restart'
        
    
