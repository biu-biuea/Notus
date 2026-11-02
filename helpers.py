import pygame
from settings import W, H, PIXEL_GRID, DARK_TAUPE

# ─ helper drawing functions
def draw_pixel_grid(surface, color=PIXEL_GRID, spacing=24):
    """subtle dotgrid background  the pinterest (the notion vibe is kinda what im going for."""
    for x in range(0, W, spacing):
        for y in range(0, H, spacing):
            pygame.draw.circle(surface, color, (x, y), 1)

def draw_rounded_rect(surface, color, rect, radius=12, border=0, border_color=None):
    r = pygame.Rect(rect)
    pygame.draw.rect(surface, color, r, border_radius=radius)
    if border and border_color:
        pygame.draw.rect(surface, border_color, r, border, border_radius=radius)

def draw_text_centered(surface, text, font, color, cx, cy):
    s = font.render(text, True, color)
    surface.blit(s, (cx - s.get_width()//2, cy - s.get_height()//2))

def draw_text(surface, text, font, color, x, y):
    s = font.render(text, True, color)
    surface.blit(s, (x, y))

# ill put just my pixel logo over here???
LOGO_PIXELS = [
    "   ",
    "  ",
    " ",
    " ",
    "  ",
    "  ",
]
def draw_pixel_logo(surface, ox, oy, scale=4, color=DARK_TAUPE):
    for row_i, row in enumerate(LOGO_PIXELS):
        for col_i, ch in enumerate(row):
            if ch == 'X':
                pygame.draw.rect(surface, color,
                    (ox + col_i*scale, oy + row_i*scale, scale-1, scale-1))