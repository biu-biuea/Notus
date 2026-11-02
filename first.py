import pygame
import sys
import math

pygame.init()
pygame.mouse.set_visible(False) # new, to hide mouse


# change this when you get the resolution of ur screen (NOW CHANGED)
# resolution matches Hosyond 7" DSI screen
W, H = 800, 480
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN | pygame.SCALED) # new, resolution change, application wouldnt fit screen
pygame.display.set_caption("notus")
clock = pygame.time.Clock()

# the palette them im using for now, prob will change it -  i want more of a cream color tbh

CREAM       = (249, 246, 240)
WARM_WHITE  = (255, 253, 248)
STONE       = (214, 208, 198)
TAUPE       = (174, 165, 152)
DARK_TAUPE  = (110, 100,  88)
CHARCOAL    = ( 54,  48,  42)
BLUSH       = (224, 196, 183)
SAGE        = (172, 189, 168)
DUSTY_BLUE  = (168, 183, 201)
PIXEL_GRID  = (230, 225, 216)   # this makes subtle dot grid colour

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
# ── helper drawing functions ───────────────────────────────────────────────────
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

# ill put just my hand drawn pixel logo over here???
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

# -
# screen splash
# -
class SplashScreen:
    def __init__(self):
        self.timer = 0
        self.duration = 180   # frames at 60fps = 3 seconds (looked this up)
        self.done = False

    def update(self):
        self.timer += 1
        if self.timer >= self.duration:
            self.done = True

    def draw(self, surface):
        surface.fill(CREAM)
        draw_pixel_grid(surface)

        # fade-in alpha
        alpha = min(255, int(255 * (self.timer / 60)))

        # logo block
        logo_x = W//2 - 52
        logo_y = H//2 - 80
        draw_pixel_logo(surface, logo_x, logo_y, scale=5,
                        color=(*DARK_TAUPE, alpha))

        # app name
        title_surf = font_title.render("notus", True, CHARCOAL)
        title_surf.set_alpha(alpha)
        surface.blit(title_surf, (W//2 - title_surf.get_width()//2, H//2 + 40))

        # tagline
        tag_surf = font_sub.render("your pocket calculator companion", True, TAUPE)
        tag_surf.set_alpha(alpha)
        surface.blit(tag_surf, (W//2 - tag_surf.get_width()//2, H//2 + 100))

        # loading dots
        if self.timer > 90:
            dots = "." * ((self.timer // 20) % 4)
            dot_surf = font_sub.render(dots, True, STONE)
            surface.blit(dot_surf, (W//2 - 10, H//2 + 140))


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
        # Card positions
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

        # ── back button ──
        draw_rounded_rect(surface, STONE, (10,10,90,36), radius=8)
        draw_text_centered(surface, "← back", font_tiny, CHARCOAL, 55, 28)

        # ── display panel ──
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

        # ── buttons ──
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


# main loop

def main():
    splash     = SplashScreen()
    home       = HomeScreen()
    calculator = CalculatorScreen()
    screens    = {
        "formulas": PlaceholderScreen("Formulas", SAGE),
        "notepad":  PlaceholderScreen("Notepad",  DUSTY_BLUE),
        "grapher":  PlaceholderScreen("Grapher",  STONE),
    }

    state = "splash"   # splash → home → calculator/formulas/notepad/grapher

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if state == "splash":
                pass   # splash auto-advances

            elif state == "home":
                home.handle_event(event)
                if home.selected:
                    state = home.selected
                    home.selected = None

            elif state == "calculator":
                result = calculator.handle_event(event)
                if result == "home":
                    state = "home"

            elif state in screens:
                result = screens[state].handle_event(event)
                if result == "home":
                    state = "home"

        # update later (?)
        if state == "splash":
            splash.update()
            if splash.done:
                state = "home"

        # draw
        if state == "splash":
            splash.draw(screen)
        elif state == "home":
            home.draw(screen)
        elif state == "calculator":
            calculator.draw(screen)
        elif state in screens:
            screens[state].draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()