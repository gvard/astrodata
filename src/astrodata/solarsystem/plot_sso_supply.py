"""Plot parameters of Solar system bodies"""

from dataclasses import dataclass
from typing import Final

import matplotlib.pyplot as plt

Y_OFFSET_MULTIPLIER = 0.011

@dataclass(frozen=True, slots=True)
class BodyParams:
    name: str
    runame: str
    a: float
    e: float
    i: float
    color: str = "grey"
    line_style: str = "--"
    line_width: float = 2
    is_planet: bool = True

PL: Final[dict[str, BodyParams]] = {
    "me": BodyParams("Mercury", "Меркурий", 0.387, 0.206, 7, color="orange"),
    "ve": BodyParams("Venus", "Венера", 0.723, 0.007, 3.4, color="c"),
    "ea": BodyParams("Earth", "Земля", 1.0, 0.016, 0, color="b"),
    "ma": BodyParams("Mars", "Марс", 1.524, 0.093, 1.85, color="r"),
    "ju": BodyParams("Jupiter", "Юпитер", 5.204, 0.049, 1.3, color="brown"),
    "sa": BodyParams("Saturn", "Сатурн", 9.583, 0.057, 2.49, color="y"),
    "ur": BodyParams("Uranus", "Уран", 19.219, 0.046, 0.77, color="c"),
    "ne": BodyParams("Neptune", "Нептун", 30.07, 0.01, 1.77, color="#00b"),
    "ce": BodyParams("Ceres", "Церера", 2.7656, 0.07958, 10.5879, color="m"),
    "ves": BodyParams("Vesta", "Веста", 2.3614, 0.0901, 7.14395, color="m", is_planet=False),
    "hy": BodyParams("Hygiea", "Гигея", 3.14759, 0.108224, 3.83294, color="m", is_planet=False),
    "pl": BodyParams("Pluto", "Плутон, 2:3", 39.33986, 0.24707, 17.1758, color="#808"),
    "ha": BodyParams("Haumea", "Хаумеа", 43.006, 0.1958, 28.208, color="#808"),
    "mk": BodyParams("Makemake", "Макемаке", 45.4497, 0.1619, 29.0339, color="#808"),
    "er": BodyParams("Eris", "Эрида", 67.997, 0.43697, 43.869, color="#808"),
    "go": BodyParams("Gonggong", "Гун-гун", 66.8951, 0.5032, 30.8664, line_width=1.5, is_planet=False),
    "qu": BodyParams("Quaoar", "Квавар", 43.1629, 0.03664, 7.991, line_width=1.5, is_planet=False),
    "or": BodyParams("Orcus", "Орк", 39.2892, 0.22314, 20.5555, line_width=1.5, is_planet=False),
    "sal": BodyParams("Salacia", "Салация", 42.1154, 0.1034, 23.9271, line_width=1.5, is_planet=False),
    "se": BodyParams("Sedna", "Седна", 506.0, 0.85, 11.93, line_width=1.5, is_planet=False),
}


def plot_vert_pla(b1: float, b2: float, show_inner_asteroids: bool = True) -> None:
    """Plots vertical lines and text descriptions for planets and large SSOs."""
    y_text_top = b2 - (b2 * Y_OFFSET_MULTIPLIER)

    for key, body in PL.items():
        if key in {"ce", "ves", "hy"} and not show_inner_asteroids:
            continue

        plt.plot([body.a, body.a], [b1, b2], c=body.color, ls=body.line_style, lw=body.line_width)

        x_offset = 0.02
        if key in {"go", "qu", "or", "sal", "se"}:
            x_offset = -0.72
        elif key in {"ves", "ce", "hy"}:
            x_offset = -0.075
        elif body.is_planet and body.a < 10:
            x_offset = 0.02
        elif (body.is_planet and body.a > 20) or not body.is_planet:
            x_offset = 0.15

        text_color = "black" if body.color == "#808" else body.color

        plt.text(
            body.a + x_offset, y_text_top, body.runame,
            c=text_color, rotation="vertical", va="top", fontsize=15 if body.line_width == 1 else 16
        )

    if show_inner_asteroids:
        plt.text(1.89, b2 * 0.43, "Семейство Венгрии", c="#45714E", rotation="vertical", va="top", fontsize=14)

def plot_vert_resonances(b1: float, b2: float, lw: float = 0.7, plot_tno: bool = False) -> None:
    """Plots Kirkwood gaps and planetary resonances."""
    y_text_top = b2 - (b2 * Y_OFFSET_MULTIPLIER)

    resonances = [
        (1.78, "5:1"), (2.065, "4:1"), (2.502, "3:1"),
        (2.825, "5:2"), (2.958, "7:3"), (3.279, "2:1"),
        (3.972, "Семейство Хильды, 3:2")
    ]
    if plot_tno:
        resonances.extend([(36.5, "3:4"), (43.92, "4:7"), (47.8, "1:2"), (55.4, "2:5")])

    for a, name in resonances:
        x_offset = 0.15 if a > 20 else 0.016
        plt.plot([a, a], [b1, b2], "--k", lw=lw)
        plt.text(a + x_offset, y_text_top, name, rotation="vertical", va="top", fontsize=14)
