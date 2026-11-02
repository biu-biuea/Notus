# Project - [notus!]

This repository is for the semester project. For each milestone, you should update the corresponding
section with information about your project status. Do not complete README sections for future milestones or
the final submission when we still have not gotten to an earlier milestone. This is likely to cause
confusion for peer code reviewers. Doing so may result in the loss of points, up to and including
an award of 0 points as determined by the instructor.

## Milestone 1

notus is a (supposed to be on hardware) desktop-based math productivity application (?) built using python and pygame. the goal of the project is to create a visually clean, intuitive, and aesthetically minimal math companion that combines calculator functionality with study tools such as notes, formulas, and graphing features.

for milestone 1, the focus was on building the core structure of the application, designing the user interface system, and implementing a fully functional calculator screen along with navigable placeholder screens for additional features.

the design aesthetic follows a soft, warm neutral palette with subtle pixel grid backgrounds and rounded ui elements. the project uses a modular screen-based architecture with separate states for splash, home, calculator, and additional feature placeholders.
### Current Progress



### Challenges

one of the primary challenges during this milestone was organizing the project architecture. initially, all components were written in a single file (because i wasnt thinking and osmething wasnt working)

### Future Directions

add the rest of the modules AND add a drawing pad compatibility



## Milestone 2


for this milestone i added a formula reference screen to replace the placeholder. formula_screen.py has 4 categories (algebra, geometry, trig, and calculus basics) with 8 formulas each that you can scroll through. each category shows up as a card on the main formula page and you tap into it to see the formulas. i also got the hardware side set up with the raspberry pi 5 and the touchscreen connected. theres currently a small import issue where main.py cant find formula_screen, probably something with how the files are organized that i need to debug. next steps are getting the drawing/grapher screen working and making sure everything runs clean on the pi.


### Current Progress

- calculator screen: working
- formula reference screen: code is done, fixing import issue
- notepad screen: still placeholder
- grapher screen: still placeholder
- hardware: raspberry pi 5 + touchscreen connected and displaying

### Challenges

ran into an import error when connecting formula_screen to main.py. also had some trouble figuring out the best way to organize the formula data so it would be easy to scroll through without lagging on the pi. time management was rough this milestone honestly.
### Future Directions

planning to build out the notepad screen next so users can write quick notes while studying. after that the grapher where you can type in an equation and see it plotted. also want to add a way to save favorite formulas and maybe a simple unit converter. long term goal is making this a full portable study tool that runs completely on the pi without needing wifi.


## Final Submission

### Overview

notus is a portable study tool that combines a calculator, formula reference, notepad, and graphing module into one handheld device. it runs on a raspberry pi 5 with a 7-inch dsi touchscreen and four physical buttons wired through gpio. the program is written in python using pygame for the graphics and gpiozero for reading the buttons. the goal of notus was to make a study tool that wasn't a phone (too distracting) or a calculator (too limited), but something purpose-built for studying. the current version has a working calculator, working formulas module, and placeholder screens for notepad and grapher while those are still in development.
[full project portfolio on google sites](https://sites.google.com/view/leahdixon/notus)
### Tutorial

when you turn on the pi, notus launches automatically. you don't have to open a terminal or run anything yourself. the splash screen shows for about three seconds, then the home menu appears with four module cards: calculator, formulas, notepad, and grapher.

there are two ways to use notus. you can tap the touchscreen to open a module by tapping its card. or you can use the four physical buttons on the breadboard. the buttons are mapped like this: home goes back to the main menu from anywhere, back exits the current module, forward cycles to the next module in order, and select opens the calculator from the home menu. so if you're inside the formulas module and you press home, you go back to the main menu. if you press forward from the calculator, you go to formulas. simple navigation either way.

once inside a module, you interact with it using the touchscreen. the calculator handles digits, addition, subtraction, multiplication, division, decimals, percent, sign flip, and clear. the formulas module shows a categorized reference of common math formulas you can scroll through. the notepad and grapher modules are still in development and currently show "coming soon" screens with the planned features listed.

### Installation Instructions

notus is built to run on a raspberry pi 5 with raspberry pi os bookworm. the hardware setup is a hosyond 7-inch dsi touchscreen connected to the pi over the dsi cable, plus four tactile buttons wired to gpio pins 17, 27, 22, and 23 with a shared ground.
required python packages:
- pygame
- gpiozero
- lgpio (the gpio backend used on pi 5)

to install:
to launch manually:

the program runs at 800x480 fullscreen, scaled automatically from a 1024x600 internal canvas using pygame's scaled display flag.

**auto-start on boot:** notus is set up to launch automatically when the pi boots. this is done with a `.desktop` file in `~/.config/autostart/` that tells the pi to run `python3 /home/biuea/desktop/notus/main.py` when the desktop loads. the file (`notus.desktop`) is included in this repo. to enable auto-start on a fresh pi, copy that file into `~/.config/autostart/` and reboot. that way notus behaves like a real product: turn on the device, the app opens, no terminal needed.

### Citation, Sources, and References
Complete this section to include citations for assets and resources that you used for your project. For example, you could
write this section like in the following example:


[UI-Pack Sci-FI from kenney.nl](https://kenney.nl/assets/ui-pack-sci-fi)

[Digital Audio Pack from kenny.nl](https://kenney.nl/assets/digital-audio)

I created by own ASCII art using the [asciiflow web application](https://asciiflow.com/#/ ) and generative AI.


> [!note]
> Any assets and resources you use need to be verifiable that they are licenced for you to use. If you made your
own assets or used generative AI, you must indicate that you did so. Include a link to any assets that you
downloaded and used. 

> [!important]
> Leaving the "Citation, Sources, and References" section unedited will count as not having completed it.


the following resources were used during this project:

- [pygame documentation](https://www.pygame.org/docs/) for the graphics, event handling, and display scaling
- [gpiozero documentation](https://gpiozero.readthedocs.io/) for the gpio button setup and edge-detection logic
- [raspberry pi 5 gpio pinout reference at pinout.xyz](https://pinout.xyz/) for identifying which pins to use for power, ground, and signal
- [hosyond 7-inch dsi touchscreen documentation](https://www.amazon.com/Hosyond-7inch-DSI-Touchscreen-Raspberry/dp/B0C7HHV2NM) for the screen wiring and specs
- [raspberry pi os bookworm release notes](https://www.raspberrypi.com/news/bookworm-the-new-version-of-raspberry-pi-os/) for understanding why rpi.gpio doesn't work on the pi 5 and gpiozero is the recommended replacement
- pinterest references for the visual style (cream colors, pixel-grid aesthetic, soft palette)

generative ai was used during this project. i used [claude](https://claude.ai/) by anthropic in a few specific ways. first, for navigating the terminal: when i ran into commands or syntax i couldn't figure out from the manual or documentation, i used claude to help me understand what to type and why. second, for testing the buttons: when i wired up my first button and the others, i used claude to help me write small test scripts to confirm each button was working before integrating them into the main program. third, for generating an image: i used ai to generate a visual reference of what i wanted my main menu to look like aesthetically, but i did not use ai-generated graphics in the final program. all the visuals in notus are drawn programmatically by me using pygame. all the code is my own, written or adapted by me, and all hardware wiring was done by me using product manuals and the gpio pinout reference.

- [breadboard tutorial from raspberry pi official magazine](https://magazine.raspberrypi.com/articles/breadboard-tutorial) for understanding how breadboards work and how to wire jumper cables between the pi gpio and the breadboard
- [how to safely connect a breadboard to raspberry pi (youtube)](https://www.youtube.com/watch?v=KwKiiWYQies) for a visual walkthrough of gpio header connections and male-to-female jumper wire usage
- [how to create a simple calculator using python (youtube)](https://www.youtube.com/watch?v=5_CAo_C523g) for understanding the basic logic of arithmetic operations and operator handling that i adapted into my calculator screen module
- [programiz simple calculator in python](https://www.programiz.com/python-programming/examples/calculator) for the basic logic of arithmetic operations and operator handling that i adapted into my calculator screen module

no third-party assets like fonts, sounds, sprites, or image packs were used. all visuals are drawn programmatically using pygame.


