import tkinter as tk
import tkinter.messagebox as msg


# Coefficient of Restitution
E: float = 1.0


def select(e: float) -> None:
    """sets the e value from the Slider"""
    global E

    E = e
    root.destroy()


def main(current: float) -> float:
    """prompts to change the value of e by selecting from a Slider
    current is the current value of e"""
    global root, E

    root = tk.Tk()
    root.title("Change Coefficient of Restitution")
    root.resizable(False, False)

    E = current

    tk.Label(
        text=(
            "Change the value of Coefficient of Restitution\n"
            "Pick a value from the Slider (0.0 - 1.0)"
        ),
        font=("CONSOLAS", 13 ,"bold")
    ).pack()

    slider = tk.Scale(
        from_=0.0, to=1.0, length=400, sliderrelief=tk.FLAT, resolution=0.001,
        orient=tk.HORIZONTAL,
    )
    slider.pack()

    enter = tk.Button(
        text="SELECT", width=46, bd=3, font=("CONSOLAS", 13, "bold"),
        command=lambda: select(e=slider.get())
    )
    enter.pack()

    root.mainloop()
    return E