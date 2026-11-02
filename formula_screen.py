import pygame
from settings import W, H, CREAM, STONE, CHARCOAL, DARK_TAUPE, TAUPE, SAGE, WARM_WHITE, BLUSH
from fonts import font_title, font_sub, font_menu, font_menu_sm, font_tiny, font_btn
from helpers import draw_pixel_grid, draw_rounded_rect, draw_text_centered, draw_text

# screen: formula reference sheet

# formula data organized by category
FORMULA_DATA = [
    {
        "category": "Algebra",
        "color": BLUSH,
        "formulas": [
            ("Quadratic Formula", "x = (-b +/- sqrt(b^2 - 4ac)) / 2a"),
            ("Slope", "m = (y2 - y1) / (x2 - x1)"),
            ("Slope-Intercept", "y = mx + b"),
            ("Point-Slope", "y - y1 = m(x - x1)"),
            ("Distance", "d = sqrt((x2-x1)^2 + (y2-y1)^2)"),
            ("Midpoint", "M = ((x1+x2)/2, (y1+y2)/2)"),
            ("Difference of Squares", "a^2 - b^2 = (a+b)(a-b)"),
            ("Binomial Square", "(a+b)^2 = a^2 + 2ab + b^2"),
        ],
    },
    {
        "category": "Geometry",
        "color": SAGE,
        "formulas": [
            ("Area of Circle", "A = pi * r^2"),
            ("Circumference", "C = 2 * pi * r"),
            ("Area of Triangle", "A = (1/2) * b * h"),
            ("Area of Rectangle", "A = l * w"),
            ("Pythagorean Theorem", "a^2 + b^2 = c^2"),
            ("Volume of Sphere", "V = (4/3) * pi * r^3"),
            ("Surface Area Sphere", "SA = 4 * pi * r^2"),
            ("Volume of Cylinder", "V = pi * r^2 * h"),
        ],
    },
    {
        "category": "Trigonometry",
        "color": STONE,
        "formulas": [
            ("Sine", "sin(t) = opposite / hypotenuse"),
            ("Cosine", "cos(t) = adjacent / hypotenuse"),
            ("Tangent", "tan(t) = opposite / adjacent"),
            ("Pythagorean Identity", "sin^2(t) + cos^2(t) = 1"),
            ("Double Angle Sin", "sin(2t) = 2 sin(t) cos(t)"),
            ("Double Angle Cos", "cos(2t) = cos^2(t) - sin^2(t)"),
            ("Law of Sines", "a/sin(A) = b/sin(B) = c/sin(C)"),
            ("Law of Cosines", "c^2 = a^2 + b^2 - 2ab cos(C)"),
        ],
    },
    {
        "category": "Calculus Basics",
        "color": BLUSH,
        "formulas": [
            ("Power Rule", "d/dx [x^n] = n * x^(n-1)"),
            ("Product Rule", "d/dx [fg] = f'g + fg'"),
            ("Quotient Rule", "d/dx [f/g] = (f'g - fg') / g^2"),
            ("Chain Rule", "d/dx [f(g(x))] = f'(g(x)) * g'(x)"),
            ("Basic Integral", "integral x^n dx = x^(n+1)/(n+1) + C"),
            ("Derivative of sin", "d/dx [sin(x)] = cos(x)"),
            ("Derivative of cos", "d/dx [cos(x)] = -sin(x)"),
            ("Derivative of e^x", "d/dx [e^x] = e^x"),
        ],
    },
]


class FormulaScreen:
    def __init__(self):
        self.scroll_y = 0
        self.max_scroll = 0
        self.hovered_back = False
        self.selected_category = None  # None = show categories, int = show that category

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.selected_category is not None:
                self.selected_category = None
                self.scroll_y = 0
                return None
            return "home"

        if event.type == pygame.MOUSEBUTTONDOWN:
            # back button
            if pygame.Rect(10, 10, 90, 36).collidepoint(event.pos):
                if self.selected_category is not None:
                    self.selected_category = None
                    self.scroll_y = 0
                    return None
                return "home"

            # category card clicks (when viewing categories)
            if self.selected_category is None:
                for i, cat in enumerate(FORMULA_DATA):
                    row = i // 2
                    col = i % 2
                    card_w = (W - 60) // 2
                    card_h = 100
                    x = 20 + col * (card_w + 20)
                    y = 120 + row * (card_h + 16)
                    rect = pygame.Rect(x, y, card_w, card_h)
                    if rect.collidepoint(event.pos):
                        self.selected_category = i
                        self.scroll_y = 0
                        return None

        # scrolling in formula detail view
        if event.type == pygame.MOUSEWHEEL and self.selected_category is not None:
            self.scroll_y -= event.y * 30
            if self.scroll_y < 0:
                self.scroll_y = 0
            if self.scroll_y > self.max_scroll:
                self.scroll_y = self.max_scroll

        return None

    def draw(self, surface):
        surface.fill(CREAM)
        draw_pixel_grid(surface)

        # back button
        draw_rounded_rect(surface, STONE, (10, 10, 90, 36), radius=8)
        draw_text_centered(surface, "< back", font_tiny, CHARCOAL, 55, 28)

        if self.selected_category is None:
            self._draw_category_menu(surface)
        else:
            self._draw_formula_list(surface)

    def _draw_category_menu(self, surface):
        # header
        draw_text_centered(surface, "Formula Reference", font_title, CHARCOAL, W // 2, 60)
        draw_text_centered(surface, "choose a category", font_sub, TAUPE, W // 2, 90)

        # decorative line
        pygame.draw.line(surface, STONE, (W // 2 - 120, 110), (W // 2 + 120, 110), 2)

        # category cards in a 2x2 grid
        for i, cat in enumerate(FORMULA_DATA):
            row = i // 2
            col = i % 2
            card_w = (W - 60) // 2
            card_h = 100
            x = 20 + col * (card_w + 20)
            y = 120 + row * (card_h + 16)

            rect = pygame.Rect(x, y, card_w, card_h)

            # shadow
            shadow_rect = rect.move(3, 3)
            draw_rounded_rect(surface, STONE, shadow_rect, radius=12)

            # card
            draw_rounded_rect(surface, cat["color"], rect, radius=12, border=2, border_color=STONE)

            # category name
            draw_text_centered(surface, cat["category"], font_menu, CHARCOAL,
                               rect.centerx, rect.centery - 12)

            # formula count
            count_text = str(len(cat["formulas"])) + " formulas"
            draw_text_centered(surface, count_text, font_menu_sm, DARK_TAUPE,
                               rect.centerx, rect.centery + 16)

        # footer
        draw_text_centered(surface, "tap a category to browse", font_tiny, TAUPE, W // 2, H - 20)

    def _draw_formula_list(self, surface):
        cat = FORMULA_DATA[self.selected_category]

        # header
        draw_text_centered(surface, cat["category"], font_title, CHARCOAL, W // 2, 60)

        line_ct = len(cat["formulas"])
        count_text = str(line_ct) + " formulas"
        draw_text_centered(surface, count_text, font_sub, TAUPE, W // 2, 90)

        # decorative line
        pygame.draw.line(surface, STONE, (W // 2 - 120, 108), (W // 2 + 120, 108), 2)

        # formula cards
        card_h = 70
        pad = 10
        start_y = 120
        visible_top = start_y
        visible_bottom = H - 10

        total_content_h = len(cat["formulas"]) * (card_h + pad)
        visible_h = visible_bottom - visible_top
        self.max_scroll = max(0, total_content_h - visible_h)

        # clip region so cards dont draw over header
        clip_rect = pygame.Rect(0, visible_top, W, visible_h)
        surface.set_clip(clip_rect)

        for i, (name, formula) in enumerate(cat["formulas"]):
            y = start_y + i * (card_h + pad) - self.scroll_y

            # skip if offscreen
            if y + card_h < visible_top or y > visible_bottom:
                continue

            card_rect = pygame.Rect(20, y, W - 40, card_h)

            # shadow
            shadow = card_rect.move(2, 2)
            draw_rounded_rect(surface, STONE, shadow, radius=10)

            # card background
            draw_rounded_rect(surface, WARM_WHITE, card_rect, radius=10,
                              border=1, border_color=STONE)

            # colored accent bar on left
            accent = pygame.Rect(card_rect.x, card_rect.y, 6, card_h)
            draw_rounded_rect(surface, cat["color"], accent, radius=3)

            # formula name
            draw_text(surface, name, font_menu_sm, CHARCOAL, card_rect.x + 16, card_rect.y + 10)

            # formula text
            draw_text(surface, formula, font_btn, DARK_TAUPE, card_rect.x + 16, card_rect.y + 38)

        # reset clip
        surface.set_clip(None)

        # scroll indicator if needed
        if self.max_scroll > 0:
            scroll_pct = self.scroll_y / self.max_scroll if self.max_scroll > 0 else 0
            bar_h = max(30, int(visible_h * (visible_h / total_content_h)))
            bar_y = visible_top + int((visible_h - bar_h) * scroll_pct)
            bar_rect = pygame.Rect(W - 8, bar_y, 4, bar_h)
            draw_rounded_rect(surface, TAUPE, bar_rect, radius=2)