import pygame
from settings import *

# fonts~
# ill try to use pygames default font as a fallback but try system mono for pixel feel

def load_font(size, bold=False):
    for name in ["Courier New", "Courier", "monospace"]:
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
            return f
        except:
            pass
    return pygame.font.Font(None, size)
font_title   = load_font(52, bold=True)
font_sub     = load_font(20)
font_menu    = load_font(26, bold=True)
font_menu_sm = load_font(17)
font_calc_lg = load_font(42, bold=True)   # calc display
font_calc_sm = load_font(28)
font_btn     = load_font(22, bold=True)
font_tiny    = load_font(14)