import pygame
from settings import W, H, CREAM, STONE, CHARCOAL, DARK_TAUPE, TAUPE
from fonts import font_title, font_sub, font_menu_sm, font_tiny
from helpers import draw_pixel_grid, draw_rounded_rect, draw_text_centered

 # place holder for formulas, note pad, grapher
class PlaceholderScreen:    # make a new file for this and the rest of the classes because i cant find anything w all these lines
    def __init__(self, title, color):
        self.title = title
        self.color = color

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "home"
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(10,10,90,36).collidepoint(event.pos):
                return "home"
        return None

    def draw(self, surface):
        surface.fill(CREAM)
        draw_pixel_grid(surface)
        draw_rounded_rect(surface, STONE, (10,10,90,36), radius=8)
        draw_text_centered(surface, "← back", font_tiny, CHARCOAL, 55, 28)

        # big card
        card = pygame.Rect(W//2-280, H//2-160, 560, 320)
        draw_rounded_rect(surface, self.color, card, radius=20,
                          border=2, border_color=STONE)
        draw_text_centered(surface, self.title, font_title, CHARCOAL,
                           W//2, H//2 - 60)
        draw_text_centered(surface, "coming soon  ✦", font_sub, DARK_TAUPE,
                           W//2, H//2 + 10)
        draw_text_centered(surface, "this section is under construction",
                           font_menu_sm, TAUPE, W//2, H//2 + 50)