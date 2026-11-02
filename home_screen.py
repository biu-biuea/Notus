import pygame
from settings import (W, H, CREAM, WARM_WHITE, STONE, TAUPE, DARK_TAUPE,
                      CHARCOAL, BLUSH, SAGE, DUSTY_BLUE)
from fonts import font_title, font_sub, font_menu, font_menu_sm, font_tiny
from helpers import draw_pixel_grid, draw_rounded_rect, draw_text_centered


# screen: HOME MENU ~~~~

MENU_ITEMS = [
    {
        "label": "Calculator",
        "icon":  ["XXXXX", "X   X", "XXXXX", "X   X", "XXXXX"],
        "desc":  "Scientific calculator",
        "color": BLUSH,
        "screen": "calculator",
    },
    {
        "label": "Formulas",
        "icon":  [" XXX ", "X   X", " XXX ", "X   X", " XXX "],
        "desc":  "Formula reference",
        "color": SAGE,
        "screen": "formulas",
    },
    {
        "label": "Notepad",
        "icon":  ["XXXXX", "X    ", "XXXX ", "X    ", "XXXXX"],
        "desc":  "Digital notes",
        "color": DUSTY_BLUE,
        "screen": "notepad",
    },
    {
        "label": "Grapher",
        "icon":  ["    X", "   X ", "  X  ", " X   ", "X    "],
        "desc":  "Plot equations",
        "color": STONE,
        "screen": "grapher",
    },
]

class HomeScreen:
    def __init__(self):
        self.hovered = None
        self.selected = None
        # card positions
        card_w, card_h = 210, 240
        start_x = (W - (4 * card_w + 3 * 20)) // 2
        self.cards = []
        for i, item in enumerate(MENU_ITEMS):
            rx = start_x + i * (card_w + 20)
            ry = H//2 - card_h//2 + 30
            self.cards.append(pygame.Rect(rx, ry, card_w, card_h))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = None
            for i, r in enumerate(self.cards):
                if r.collidepoint(event.pos):
                    self.hovered = i
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, r in enumerate(self.cards):
                if r.collidepoint(event.pos):
                    self.selected = MENU_ITEMS[i]["screen"]

    def draw(self, surface):
        surface.fill(CREAM)
        draw_pixel_grid(surface)

        # the header
        draw_text_centered(surface, "notus", font_title, CHARCOAL, W//2, 60)
        draw_text_centered(surface, "choose a mode", font_sub, TAUPE, W//2, 100)

        # decorative line
        pygame.draw.line(surface, STONE, (W//2-120, 118), (W//2+120, 118), 2)

        for i, (item, rect) in enumerate(zip(MENU_ITEMS, self.cards)):
            hov = (self.hovered == i)
            card_color = WARM_WHITE if not hov else item["color"]
            shadow_rect = rect.move(4, 4)
            draw_rounded_rect(surface, STONE, shadow_rect, radius=16)
            draw_rounded_rect(surface, card_color, rect, radius=16,
                              border=2, border_color=STONE)

            # pixel icon
            ico = item["icon"]
            ico_scale = 7
            ico_w = len(ico[0]) * ico_scale
            ico_h = len(ico) * ico_scale
            ox = rect.centerx - ico_w//2
            oy = rect.y + 30
            for ri, row in enumerate(ico):
                for ci, ch in enumerate(row):
                    if ch == 'X':
                        pygame.draw.rect(surface, DARK_TAUPE,
                            (ox + ci*ico_scale, oy + ri*ico_scale,
                             ico_scale-2, ico_scale-2))

            # label
            draw_text_centered(surface, item["label"], font_menu, CHARCOAL,
                               rect.centerx, rect.y + 30 + ico_h + 30)
            draw_text_centered(surface, item["desc"], font_menu_sm, TAUPE,
                               rect.centerx, rect.y + 30 + ico_h + 60)

        # ftooter
        draw_text_centered(surface, "tap a card to begin", font_tiny, STONE, W//2, H-20)