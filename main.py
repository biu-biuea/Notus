import pygame
import sys
from settings import screen, clock, SAGE, DUSTY_BLUE, STONE
from splash_screen import SplashScreen
from home_screen import HomeScreen
from calculator_screen import CalculatorScreen
from placeholder_screen import PlaceholderScreen
from formula_screen import FormulaScreen
from buttons import HardwareButtons


# main loop

def main():

    splash    = SplashScreen()
    home      = HomeScreen()
    calculator = CalculatorScreen()
    hw = HardwareButtons()  # just added.
    screens    = {
        "formulas": FormulaScreen(),
        "notepad":  PlaceholderScreen("Notepad",  DUSTY_BLUE),
        "grapher":  PlaceholderScreen("Grapher",  STONE),
    }

    state = "splash"  # splash to home to calculator/formulas/notepad/grapher

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if state == "splash":
                pass  # splash auto advances

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

        # hardware button input
        for name in hw.poll():
            if name == 'home':
                state = "home"
            elif name == 'back':
                if state != "home" and state != "splash":
                    state = "home"
            elif name == 'forward':
                modules = ["calculator", "formulas", "notepad", "grapher"]
                if state in modules:
                    i = modules.index(state)
                    state = modules[(i + 1) % len(modules)]
                elif state == "home":
                    state = "calculator"
            elif name == 'select':
                if state == "home":
                    state = "calculator"

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