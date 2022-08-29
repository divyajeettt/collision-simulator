# collision-simulator

## About collision-simulator

collision-simulator is quite literally a simulation of [collisions](https://en.wikipedia.org/wiki/Collision), with variable coefficients of restitution, built using [`pygame`](https://www.pygame.org/docs/) in Python.

*Date of creation:* `03 September, 2021`

It is an interactive simulation where the user spawns balls on the screen, that collide with each other and with walls (having infinite mass). The collisions are handled using real [collision mechanics](https://www.lehman.edu/faculty/anchordoqui/chapter15.pdf).

## Features

- Spawn balls of different radii and variable densities
- Turn gravity (of variable strength) ON and OFF, and change its direction
- Walls of infinite mass
- Different beep sounds for collisions (depending upon their masses)
- Ability to view the current state of any ball (by clicking it)
- Generation of logs

## Controls

Check the main controls in `controls.txt`. Additional controls are as follows:
- CTRL: To see the controls
- L: Log the current state of the balls

## Edit the logging settings

To modify the level of the `logger`, modify:

```python
logging.basicConfig(
    filename="collisions.log", level=logging.INFO, format=LOG_FORMAT
)
```

 on [Line 56](https://github.com/divyajeettt/collision-simulator/blob/cebc2bcb3bdc8bc4615e95d1917fd9471579347b/main.py#L56) of `main.py` to:
 
 ```python
logging.basicConfig(
    filename="collisions.log", level=LEVEL, format=LOG_FORMAT
)
 ```
 
 where `LEVEL` can be one of:
 - `logging.INFO`
 - `logging.DEBUG`
 - `logging.WARNING`
 - `logging.ERROR`
 - `logging.CRITICAL`

## Run

To run, clone the repository on your device, navigate to the folder, and execute:

```
python3 main.py
```

## Footnotes and Issues

- Beep sounds get delayed when a large number of collisions occur simultaneously.
- If a Ball is moving too fast, it may be able to escape the boundary. This is possibly due to not registering its collision with the wall as its updated position stands outside the boundary.
- For lower restitutions of collision and for fast velocities, two or more balls may get stuck together.
