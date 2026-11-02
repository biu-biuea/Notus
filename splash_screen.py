import pygame
from settings import W, H, CREAM, DARK_TAUPE, CHARCOAL, TAUPE, STONE
from fonts import font_title, font_sub
from helpers import draw_pixel_grid, draw_pixel_logo

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

        # fade in alpha
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