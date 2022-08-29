from generator import Ball, Point
import winsound
import math


WALLS = {0: "Upper", 1: "Lower", 2: "Left", 3: "Right"}


def select(point: Point, balls: list[Ball]) -> Ball|None:
    """returns the Ball on which point lies, if any, else None"""

    for ball in balls:
        if math.dist(point, ball.position) <= ball.radius:
            return ball
    return None


def frequency(ball1: Ball, ball2: Ball|Ball = None) -> int:
    """returns the frequency of Beep to be played on a collision"""

    if ball2 is None:
        r = ball1.radius
        return {(r <= 30): 500, (r <= 20): 750, (r <= 10): 1000}[True]

    r1 = ball1.radius if ball1.radius < ball2.radius else ball2.radius
    r2 = ball2.radius if r1 == ball1.radius else ball1.radius

    if r1 <= 10.0:
        return {(r2 <= 30): 1750, (r2 <= 20): 1500, (r2 <= 10): 1250}[True]
    elif r1 <= 20.0:
        return {(r2 <= 30): 1000, (r2 <= 20): 750}[True]
    else:
        return 500


def collided(ball: Ball, obj: Point|Ball) -> bool:
    """returns True if the given objects have collided and False otherwise"""

    if isinstance(obj, Ball):
        return math.dist(ball.position, obj.position) <= ball.radius+obj.radius
    else:
        return math.dist(obj, ball.position) <= ball.radius


def handle(balls: list[Ball], limits: tuple[Point], e: float) -> list[str]:
    """handles collisions of Balls with walls and with one-another
    updates their velocites according to the collisions
    returns a list containing information about occurred collisions"""

    collisions = []
    lower, upper = limits

    # Handle Collisions with Walls
    for ball in balls:
        x, y = ball.position
        points = [(x, lower), (x, upper), (lower, y), (upper, y)]

        for i, point in enumerate(points):
            if not collided(ball, point):
                continue

            collisions.append(f"Collision: {ball} with {WALLS[i]} Wall")
            winsound.Beep(frequency(ball), 10)

            ball.velocity.y *= -1 if (i < 2) else +1
            ball.velocity.x *= +1 if (i < 2) else -1

    # Handle Collisions with other Balls
    for i, b1 in enumerate(balls, start=1):
        for b2 in balls[i:]:
            if not collided(b1, b2):
                continue

            collisions.append(f"Collision: {b1} with {b2}")
            winsound.Beep(frequency(b1, b2), 10)

            m1, m2, u1, u2 = b1.mass, b2.mass, b1.velocity, b2.velocity
            b1.velocity = ((m1 - e*m2)*u1 + (1 + e)*m2*u2) / (m1 + m2)
            b2.velocity = ((1 + e)*m1*u1 + (m2 - e*m1)*u2) / (m1 + m2)

    return collisions
