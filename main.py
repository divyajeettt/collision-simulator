"""Collision Simulator

You can draw Balls on the screen within the given box. The Balls will move
according to the velocities given to them, collide and move accordingly.
The Walls on the edges are Walls of infinite mass.
Press CTRL to see the CONTROLS
Press 'L' to log the current state of all the Balls
"""

import pygame
import logging
import winsound
import generator
import collisions
import gravitation
import restitution

pygame.font.init()


# Constants
SIDE: int = 625
FPS:  int = 100
TIME: float = 1 / FPS

BORDER: int = 20
LOWER:  int = BORDER + generator.maxR
UPPER:  int = SIDE - LOWER

# Lower and Upper Limits of the screens (i.e. positions of the Walls)
LIMITS: generator.Point = (BORDER-7, SIDE-BORDER+10)

# List of Balls
BALLS: list[generator.Ball] = []

# Colors
BLACK: generator.Color = (  0,   0,   0)
WHITE: generator.Color = (255, 255, 255)
GRAY:  generator.Color = (127, 127, 127)
RED:   generator.Color = (200,   0,   0)

# Fonts
FONT1 = pygame.font.SysFont("SEGOEUISYMBOL", 45, "BOLD")
FONT2 = pygame.font.SysFont("GEORGIA", 35)
FONT3 = pygame.font.SysFont("GEORGIA", 27)
FONT4 = pygame.font.SysFont("CONSOLAS", 25)
FONT5 = pygame.font.SysFont("CONSOLAS", 20)
FONT6 = pygame.font.SysFont("CONSOLAS", 15)

# Controls of the Simulation
with open("controls.txt") as file:
    CONTROLS: list[str] = file.read().splitlines()

# Information about the Logger
LOG_FORMAT: str = "%(levelname)s: %(asctime)s - %(message)s"
logging.basicConfig(
    filename="collisions.log", level=logging.INFO, format=LOG_FORMAT
)
logger = logging.getLogger()

# Initialize the Window / Screen
WINDOW: pygame.Surface = pygame.display.set_mode((SIDE, SIDE))
pygame.display.set_caption("Collision Simulator")


def draw_screen(
        controls: bool, box: bool, gravity: bool, direction: str, paused: bool,
        planet: str|None, acc: float, ball: generator.Ball|None
    ) -> None:
        """draws the Walls on the screen and draws whether gravity is ON or OFF
        if controls is True, draw the controls on the screen
        if box is True, draw the box showing the area where Balls can be spawned
        if simulator is paused, display text - 'PAUSED'
        if ball is not None, display information about the selected ball"""

        WINDOW.fill(WHITE)
        pygame.draw.rect(WINDOW, BLACK, (0, 0, SIDE, SIDE), width=BORDER)

        if controls:
            heading = FONT1.render("CONTROLS", 1, BLACK)
            underline = FONT1.render("_"*12, 1, BLACK)
            WINDOW.blit(heading, ((SIDE-heading.get_width())//2, 10))
            WINDOW.blit(underline, ((SIDE-underline.get_width()) /2, 15))

            for i, line in enumerate(CONTROLS):
                font = FONT4 if ":" in line else FONT6
                WINDOW.blit(font.render(line, 1, BLACK), (30, 80+i*26))

            footing = FONT2.render("Press 'CTRL' to continue...", 1, BLACK)
            WINDOW.blit(footing, ((SIDE-footing.get_width()) // 2, 570))
            return

        draw_info(ball)

        if box:
            rect = (LOWER, LOWER, UPPER-LOWER, UPPER-LOWER)
            pygame.draw.rect(WINDOW, GRAY, rect, width=2)

        arrow = {"+y": "↓", "-y": "↑", "+x": "→", "-x": "←"}[direction]
        switch = "ON" if gravity else "OFF"
        bg = FONT1.render(f"GRAVITY {arrow}: {switch}", 1, GRAY)
        if planet is not None:
            text = FONT2.render(planet, 1, GRAY)
        else:
            text = FONT3.render(f"Current Value of g = {acc/FPS:.2f}", 1, GRAY)

        WINDOW.blit(bg, ((SIDE-bg.get_width())//2, (SIDE-bg.get_height())//2))
        WINDOW.blit(text, ((SIDE-text.get_width())//2, 255))

        if paused:
            WINDOW.blit(FONT2.render("PAUSED", 1, GRAY), (470, 575))


def draw_info(ball: generator.Ball|None = None) -> None:
    """draws information about the Ball selected on the screen"""

    if ball is None:
        return

    center: generator.Point = (210, 35)
    (sx, sy), (vx, vy) = ball.position, ball.velocity
    den, pos, vel = (450, 50), (25, 60), (25, 90)

    WINDOW.blit(FONT3.render("Selected Ball:", 1, BLACK), (25, 20))
    pygame.draw.circle(WINDOW, ball.color, center, 15)
    pygame.draw.circle(WINDOW, BLACK, center, 15, width=3)

    WINDOW.blit(FONT5.render(f"Radius: {ball.radius:.2f}", 1, GRAY), (270, 25))
    WINDOW.blit(FONT5.render(f"Mass: {ball.mass:.2f}", 1, GRAY), (450, 25))
    WINDOW.blit(FONT5.render(f"Density: {ball.density:.2f}", 1, GRAY), den)
    WINDOW.blit(FONT5.render(f"Position: ({sx:.2f}, {sy:.2f})", 1, GRAY), pos)
    WINDOW.blit(FONT5.render(f"Velocity: ({vx:.2f}, {vy:.2f})", 1, GRAY), vel)


def vary_density(density: float) -> None:
    """draws an iterating bar on the screen to represent density"""

    scale = (generator.maxD - density) * 10
    pygame.draw.rect(WINDOW, RED, (25, 400+scale, 40, 175-scale))
    pygame.draw.rect(WINDOW, BLACK, (25, 400+scale, 40, 175-scale), width=5)


def spawn_ball(
        center: generator.Point, radius: float, color: generator.Color
    ) -> None:
    """initializes a Ball at the given position with given iterating radius"""

    pygame.draw.circle(WINDOW, BLACK, center, radius+3, width=3)
    pygame.draw.circle(WINDOW, color, center, radius)
    pygame.draw.line(WINDOW, color, center, pygame.mouse.get_pos(), 2)


def draw_balls(density: float, vector: bool) -> None:
    """draw all current Balls on the screen, along with current density
    if vector is True, draw the velocity vector of the Ball"""

    WINDOW.blit(FONT5.render(f"Density: {density:.2f}", 1, GRAY), (25, 587))

    for ball in BALLS:
        if vector:
            end = ball.position + (vel := ball.velocity)
            normal = 2 * vel.normalize() if vel else vel
            pygame.draw.line(WINDOW, ball.color, ball.position, end, width=2)
            for i in range(5):
                pygame.draw.circle(WINDOW, ball.color, end-i*normal, i)

        pygame.draw.circle(WINDOW, BLACK, ball.position, ball.radius+3, width=3)
        pygame.draw.circle(WINDOW, ball.color, ball.position, ball.radius)


def main() -> None:
    """__main__ function"""

    clock = pygame.time.Clock()
    arrow_keys: dict[pygame.event.key, str] = {
        pygame.K_DOWN: "+y", pygame.K_UP: "-y",
        pygame.K_LEFT: "-x", pygame.K_RIGHT: "+x"
    }

    # Direction of Gravity
    direction = arrow_keys[pygame.K_DOWN]

    # Acceleration due to Gravity
    planet = "EARTH"
    acc: float = gravitation.g.get(planet) * FPS

    # Coefficient of Restitution
    e: float = restitution.E

    density: float = 1.0
    hold_radius = hold_density = vector = paused = controls = box = False
    gravity, selection = True, None

    logger.info(f"INITIALIZED Collision Simulator: {(FPS, e) = }")
    logger.warning(f"Gravity of {planet}: {direction = }")

    running = True
    while running:
        clock.tick(FPS)
        draw_screen(
            controls, box, gravity, direction, paused, planet, acc, selection
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("QUITING Collision Simulator")
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key in arrow_keys:
                    direction = arrow_keys[event.key]
                    log = f"Direction of Gravity: changed to {direction}"
                    logger.warning(log)

                elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                    controls = paused = not controls
                    hold_radius = hold_density = box = False
                    selection = None
                    log = f"{'Opened' if controls else 'Closed'} Controls"
                    logger.info(log)

                elif event.key == pygame.K_b:
                    if not (controls or hold_density) and selection is None:
                        box = not box

                elif event.key == pygame.K_c:
                    planet, acc = gravitation.main(FPS, acc, planet)
                    if planet is None:
                        log = f"Gravitational Acceleration (g) changed to {acc}"
                    else:
                        log = f"Gravity changed to Gravity of {planet}"
                    logger.warning(log)

                elif event.key == pygame.K_d:
                    generator.reset(generator.DENSITIES, generator.minD)
                    hold_density, box = True, False

                elif event.key == pygame.K_e:
                    e = restitution.main(e)
                    logger.warning(f"Coefficient of Restitution changed to {e}")

                elif event.key == pygame.K_g:
                    gravity = not gravity
                    log = f"Gravity: Switched {'ON' if gravity else 'OFF'}"
                    logger.warning(log)

                elif event.key == pygame.K_l:
                    if not BALLS:
                        logger.warning("The Screen is empty")
                    else:
                        logger.info(f"Current State of the BALLS: {BALLS}")

                elif event.key == pygame.K_p:
                    if not controls:
                        paused = not paused
                        hold_radius = hold_density = False
                        log = f"Simulator {'PAUSED' if paused else 'RESUMED'}"
                        logger.warning(log)

                elif event.key == pygame.K_r:
                    if BALLS:
                        BALLS.clear()
                        selection = None
                        logger.warning("Removed: ALL Balls")

                elif event.key == pygame.K_v:
                    vector = not vector

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    center = (x, y) = event.pos
                    selection = collisions.select(center, BALLS)
                    if selection is not None:
                        box = False
                        winsound.PlaySound("SystemExit", winsound.SND_ASYNC)
                        logger.info(f"Selected Ball at {center}: {selection}")
                        continue

                    if not paused:
                        generator.reset(generator.RADII, generator.minR)
                        if LOWER <= x <= UPPER and LOWER <= y <= UPPER:
                            hold_radius = True
                            color = generator.color()

                elif event.button == 3:
                    point = event.pos
                    if (ball := collisions.select(point, BALLS)) is not None:
                        selection = None if selection is ball else selection
                        BALLS.remove(ball)
                        logger.warning(f"Removed: {ball}")
                        winsound.PlaySound("SystemExit", winsound.SND_ASYNC)

                    elif hold_radius:
                        hold_radius = False
                        logger.warning(f"Cancelled Ball at: {point}")
                        winsound.PlaySound("SystemExit", winsound.SND_ASYNC)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if not hold_radius:
                    continue

                hold_radius = False
                center = pygame.math.Vector2(center)
                vel = center - pygame.math.Vector2(pygame.mouse.get_pos())
                BALLS.append(
                    ball := generator.Ball(color, radius, center, vel, density)
                )
                logger.info(f"Created: {ball}")

            elif event.type == pygame.KEYUP and event.key == pygame.K_d:
                if not hold_density:
                    continue
                hold_density = False

        if hold_radius:
            spawn_ball(center, (radius := next(generator.RADII)), color)

        if hold_density:
            vary_density(density := next(generator.DENSITIES))

        if not paused:
            for collision in collisions.handle(BALLS, LIMITS, e=e):
                logger.info(collision)

            generator.Ball.update(BALLS, TIME, gravity, acc, direction)

        if not controls:
            draw_balls(density=density, vector=vector)

        pygame.display.update()


if __name__ == "__main__":
    main()