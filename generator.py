from dataclasses import dataclass, field
import numpy as np
import itertools
import random


# Type Aliases
Color = tuple[int, int, int]
Point = tuple[float, float]


def iterable(lower: float, upper: float, dx: float) -> itertools.cycle:
    """returns an inifite iterable lower -> upper -> lower -> ...
    dx is the difference between successive terms"""

    return itertools.cycle(itertools.chain(
        np.arange(lower, upper+dx, dx), np.arange(upper, lower-dx, -dx)
    ))


# Iterable containing Radii
dR: float = 0.5
minR: float = 2.0
maxR: float = 30.0
RADII = iterable(minR, maxR, dR)

# Iterable containing Densities
dD: float = 0.25
minD: float = 1.0
maxD: float = 15.0
DENSITIES = iterable(minD, maxD, dD)


def color() -> Color:
    """returns a random color"""

    return tuple(random.randrange(256) for _ in range(3))


def reset(iterable: itertools.cycle, lower: float) -> None:
    """resets the iterable to start from 0.0 (RADII) / 1.0 (DENSITIES) again"""

    while next(iterable) != lower:
        next(iterable)


@dataclass
class Ball:
    """
    represents a Ball object that moves in 2D-space
    attributes:
        self.color: color of the Ball
        self.radius: radius of the Ball (as float)
        self.position: position of center of the Ball
        self.velocity: velocity Vector of the Ball
        self.density: density of the Ball
        self.mass: mass of the Ball
    """

    color: Color
    radius: float
    position: "pygame.math.Vector2"
    velocity: "pygame.math.Vector2"
    density: float
    mass: float = field(init=False, repr=False)

    def __post_init__(self):
        self.mass = float(np.pi * self.radius**2 * self.density)

    @staticmethod
    def update(
            balls: list["Ball"], dt: float, gravity: bool, g: float, dirn: str
        ) -> None:
        """updates the position (and veloctiy) of the Balls according to their
        velocities and gravitational acceleration, if any"""

        sign, axis = dirn
        at, at2 = g*dt, 1/2*g*dt**2
        for ball in balls:
            if gravity:
                exec(f"ball.position.{axis} {sign}= at2")
                exec(f"ball.velocity.{axis} {sign}= at")
            ball.position += ball.velocity * dt