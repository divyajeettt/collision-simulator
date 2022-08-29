import tkinter as tk
import tkinter.messagebox as msg


g: dict[str, float] = {
    "SUN": 273.71,
    "MERCURY": 3.703,
    "VENUS": 8.872,
    "EARTH": 9.8067, "MOON": 1.6250,
    "CERES": 0.28,
    "MARS": 3.728, "PHOBOS": 0.0057, "DEIMOS": 0.003,
    "JUPITER": 25.935, "IO": 1.789, "GANYMEDE": 1.426, "CALLISTO": 1.236,
    "SATURN": 11.19, "TITAN": 1.3455, "ENCELADUS": 0.113,
    "URANUS": 9.01, "TITANIA": 0.3379,
    "NEPTUNE": 11.28, "TRITON": 0.779,
    "PLUTO": 0.61,
    "ERIS": 0.801,
}


def callback(string: str) -> bool:
    """callback: returns if string is a valid input"""

    return string.isalpha() or not string


def enter_name() -> None:
    """prompts to enter name of the Planet whose g value is required"""

    for name, widget in tuple(root.children.items()):
        widget.destroy()

    tk.Button(
        text="GO BACK TO PREVIOUS SCREEN", width=46, bd=3,
        font=("CONSOLAS", 13 ,"bold"), command=main
    ).pack()

    tk.Label(
        text="Enter name of Planet, Moon or Dwarf Planet:",
        font=("CONSOLAS", 13 ,"bold")
    ).pack()

    entry = tk.Entry(
        root, width=46, bd=3, font=("CONSOLAS", 13, "bold"),
        validate="key", validatecommand=(root.register(callback), "%P")
    )
    entry.pack()

    enter = tk.Button(
        text="SELECT", width=46, bd=3, font=("CONSOLAS", 13, "bold"),
        command=lambda: select(planet=entry.get())
    )
    enter.pack()


def pick_value() -> None:
    """prompts to select a g value from a Slider (0.0 - 300.0)"""

    for name, widget in tuple(root.children.items()):
        widget.destroy()

    tk.Button(
        text="GO BACK TO PREVIOUS SCREEN", width=46, bd=3,
        font=("CONSOLAS", 13 ,"bold"), command=main
    ).pack()

    tk.Label(
        text="Pick a value for 'g' from the Slider:",
        font=("CONSOLAS", 13 ,"bold")
    ).pack()

    slider = tk.Scale(
        from_=0.0, to=300.0, length=400, sliderrelief=tk.FLAT, resolution=0.01,
        orient=tk.HORIZONTAL,
    )
    slider.pack()

    enter = tk.Button(
        text="SELECT", width=46, bd=3, font=("CONSOLAS", 13, "bold"),
        command=lambda: select(acc=slider.get())
    )
    enter.pack()


def select(acc: float|None = None, planet: str|None = None) -> None:
    """if acc is not None, set the value of g to given 'acc'
    if planet is not None, fetch the value of g from the dict"""
    global G, PLANET

    if isinstance(acc, float):
        PLANET, G = None, acc
        return root.destroy()

    if not planet:
        return msg.showwarning("Empty Field", "Please enter a Planet Name.")

    try:
        PLANET = planet.upper()
        G = g[PLANET]
    except KeyError:
        message = (
            "Invalid Planet Name. You must select one of the following "
            f"celestial bodies: \n{list(g.keys())}"
        )
        msg.showinfo("INVALID NAME", message)
    else:
        root.destroy()


def main(fps: int, curr_acc: float, curr_planet: str) -> tuple[str, float]:
    """displays options to change the value of Gravitational Acceleration
    fps is the number to scale g by
    current is the current value of g"""
    global root, G, PLANET

    root = tk.Tk()
    root.title("Change Gravitational Acceleration")
    root.resizable(False, False)

    G, PLANET = curr_acc, curr_planet
    for name, widget in tuple(root.children.items()):
        widget.destroy()

    tk.Label(
        text=(
            "Change the value of Gravitational Acceleration\n"
            "Choose one of the two methods:"
        ),
        font=("CONSOLAS", 13 ,"bold")
    ).pack()

    tk.Button(
        text="Enter name of Planet / Dwarf Planet / Moon", width=46, bd=3,
        font=("CONSOLAS", 13, "bold"), command=enter_name
    ).pack()

    tk.Button(
        text="Pick a value from a Slider (0.0 - 300.0)", width=46, bd=3,
        font=("CONSOLAS", 13, "bold"), command=pick_value
    ).pack()

    root.mainloop()
    return PLANET, (G*fps if G != curr_acc else G)