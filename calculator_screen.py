import pygame
from settings import (W, H, CREAM, WARM_WHITE, STONE, TAUPE, DARK_TAUPE,
                      CHARCOAL, BLUSH)
from fonts import font_sub, font_calc_lg, font_btn, font_tiny
from helpers import draw_pixel_grid, draw_rounded_rect, draw_text_centered, draw_text


# screem: calc

CALC_BUTTONS = [
    ["C",  "±",  "%",  "÷"],
    ["7",  "8",  "9",  "×"],
    ["4",  "5",  "6",  "−"],
    ["1",  "2",  "3",  "+"],
    ["0",  ".",  "⌫",  "="], # copied "⌫" and pasted that from some discord chat lol
]

class CalculatorScreen:
    def __init__(self):
        self.display_main = "0"
        self.display_sub  = ""
        self.current      = ""
        self.operator     = None
        self.first_val    = None
        self.just_evaled  = False
        self.hovered_btn  = None
        self._build_buttons()

    def _build_buttons(self):
        pad = 14
        sidebar_w = 340   # left panel = display + buttons
        btn_area_x = W - sidebar_w
        btn_w = (sidebar_w - pad*5) // 4
        btn_h = 58
        btn_area_y = H - (5 * (btn_h + pad)) - pad
        self.btn_rects = []
        for r, row in enumerate(CALC_BUTTONS):
            row_rects = []
            for c, label in enumerate(row):
                x = btn_area_x + pad + c*(btn_w+pad)
                y = btn_area_y + r*(btn_h+pad)
                row_rects.append(pygame.Rect(x, y, btn_w, btn_h))
            self.btn_rects.append(row_rects)

    def _btn_color(self, label, hov):
        if label == "=":
            return DARK_TAUPE if hov else CHARCOAL
        if label in ("÷","×","−","+"):
            return STONE if hov else TAUPE
        if label in ("C","±","%"):
            return BLUSH if hov else BLUSH
        return STONE if hov else WARM_WHITE

    def _btn_text_color(self, label):
        if label == "=":
            return CREAM
        if label in ("÷","×","−","+"):
            return CHARCOAL
        return CHARCOAL

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "home"
        if event.type == pygame.MOUSEMOTION:
            self.hovered_btn = None
            for r, row in enumerate(self.btn_rects):
                for c, rect in enumerate(row):
                    if rect.collidepoint(event.pos):
                        self.hovered_btn = (r, c)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for r, row in enumerate(self.btn_rects):
                for c, rect in enumerate(row):
                    if rect.collidepoint(event.pos):
                        self._press(CALC_BUTTONS[r][c])
        # back button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(10, 10, 90, 36).collidepoint(event.pos):
                return "home"
        return None

    def _press(self, label):
        if label == "C":
            self.display_main = "0"
            self.display_sub  = ""
            self.current      = ""
            self.operator     = None
            self.first_val    = None
            self.just_evaled  = False

        elif label == "⌫":
            if self.current:
                self.current = self.current[:-1]
                self.display_main = self.current if self.current else "0"

        elif label == "±":
            if self.current and self.current != "0":
                if self.current.startswith("-"):
                    self.current = self.current[1:]
                else:
                    self.current = "-" + self.current
                self.display_main = self.current

        elif label == "%":
            try:
                val = float(self.current)
                self.current = str(val / 100)
                self.display_main = self._fmt(float(self.current))
            except:
                pass

        elif label in ("÷","×","−","+"):
            try:
                self.first_val = float(self.current) if self.current else 0
            except:
                self.first_val = 0
            self.operator = label
            self.display_sub = f"{self._fmt(self.first_val)} {label}"
            self.current = ""
            self.just_evaled = False

        elif label == "=":
            try:
                second = float(self.current) if self.current else self.first_val
                ops = {"÷": lambda a,b: a/b if b!=0 else "Error",
                       "×": lambda a,b: a*b,
                       "−": lambda a,b: a-b,
                       "+": lambda a,b: a+b}
                if self.operator and self.first_val is not None:
                    result = ops[self.operator](self.first_val, second)
                    self.display_sub  = f"{self._fmt(self.first_val)} {self.operator} {self._fmt(second)} ="
                    if isinstance(result, str):
                        self.display_main = result
                        self.current = ""
                    else:
                        self.display_main = self._fmt(result)
                        self.current = str(result)
                    self.operator  = None
                    self.first_val = None
                    self.just_evaled = True
            except:
                self.display_main = "Error"

        elif label == ".":
            if "." not in self.current:
                self.current = (self.current or "0") + "."
                self.display_main = self.current

        else:  # digit
            if self.just_evaled:
                self.current = ""
                self.just_evaled = False
            self.current += label
            self.display_main = self._fmt(float(self.current)) if self.current.replace("-","").replace(".","").isdigit() else self.current

    def _fmt(self, val):
        if isinstance(val, float):
            if val == int(val) and abs(val) < 1e12:
                return str(int(val))
            return f"{val:.6g}"
        return str(val)

    def draw(self, surface):
        surface.fill(CREAM)
        draw_pixel_grid(surface)

        # ─back button ─
        draw_rounded_rect(surface, STONE, (10,10,90,36), radius=8)
        draw_text_centered(surface, "← back", font_tiny, CHARCOAL, 55, 28)

        # ─ display panel ─
        disp_rect = pygame.Rect(10, 56, W - 350, H - 70)
        draw_rounded_rect(surface, WARM_WHITE, disp_rect, radius=16,
                          border=2, border_color=STONE)
        # sub expression
        if self.display_sub:
            draw_text(surface, self.display_sub, font_sub, TAUPE,
                      disp_rect.x+20, disp_rect.y+20)
        # main number — right-aligned
        main_surf = font_calc_lg.render(str(self.display_main), True, CHARCOAL)
        mx = disp_rect.right - main_surf.get_width() - 20
        my = disp_rect.bottom - main_surf.get_height() - 20
        surface.blit(main_surf, (mx, my))

        # ─ buttons ─
        for r, row in enumerate(self.btn_rects):
            for c, rect in enumerate(row):
                label = CALC_BUTTONS[r][c]
                hov   = (self.hovered_btn == (r,c))
                col   = self._btn_color(label, hov)
                # shadow
                draw_rounded_rect(surface, STONE, rect.move(3,3), radius=10)
                draw_rounded_rect(surface, col, rect, radius=10,
                                  border=1, border_color=STONE)
                draw_text_centered(surface, label, font_btn,
                                   self._btn_text_color(label),
                                   rect.centerx, rect.centery)