"""Plot parameters of Solar system bodies.
Data source for planets:
Keplerian elements, with respect to the mean ecliptic and equinox of J2000,
valid for the time-interval 1800 AD - 2050 AD:
https://ssd.jpl.nasa.gov/planets/approx_pos.html
NOTE on Neptune resonance factors:
Instead of a single heliocentric semi-major axis (30.07 au), individual effective
axes (30.125 to 30.210 au) are used based on analytical celestial mechanics.
This accounts for the barycentric shift of the Solar System (caused by Jupiter/Saturn
pulling the Sun) and phase space asymmetry of stable libration zones.
At extreme distances (2:5 resonance), fast barycentric perturbations average out,
returning the effective axis back to the pure heliocentric value of 30.07 au.
"""

from dataclasses import dataclass
from typing import Final

import matplotlib.pyplot as plt

Y_OFFSET_MULTIPLIER = 0.011

@dataclass(slots=True)  # frozen=True,
class BodyParams:
    name: str
    runame: str
    a: float = 0.0
    e: float = 0.0
    i: float = 0.0
    color: str = "grey"
    line_style: str = "--"
    line_width: float = 2
    is_planet: bool = True
    mpc_id: str = ""

PL: Final[dict[str, BodyParams]] = {
    "me": BodyParams("Mercury", "Меркурий", a=0.3871, e=0.2056, i=7.0050, color="orange"),
    "ve": BodyParams("Venus", "Венера", a=0.7233, e=0.0068, i=3.3947, color="c"),
    "ea": BodyParams("Earth", "Земля", a=1.00, e=0.0167, i=-0.000015, color="b"),
    "ma": BodyParams("Mars", "Марс", a=1.5237, e=0.0934, i=1.8497, color="r"),
    "ju": BodyParams("Jupiter", "Юпитер", a=5.2029, e=0.0484, i=1.3044, color="brown"),
    "sa": BodyParams("Saturn", "Сатурн", a=9.5367, e=0.0539, i=2.4860, color="y"),
    "ur": BodyParams("Uranus", "Уран", a=19.1892, e=0.0473, i=0.7726, color="c"),
    "ne": BodyParams("Neptune", "Нептун", a=30.0699, e=0.0086, i=1.7700, color="#00b"),
    "ce": BodyParams("Ceres", "Церера", mpc_id="(1) Ceres", color="m"),
    "ves": BodyParams("Vesta", "Веста", mpc_id="(4) Vesta", color="m", is_planet=False),
    "pa": BodyParams("Pallas", "Паллада", mpc_id="(2) Pallas", color="m", is_planet=False),
    "hy": BodyParams("Hygiea", "Гигея", mpc_id="(10) Hygiea", color="m", is_planet=False),
    "in": BodyParams("Interamnia", "Интерамния", mpc_id="(704) Interamnia", color="m", is_planet=False),
    "pl": BodyParams("Pluto", "Плутон", a=39.4817, e=0.2488, i=17.1418, mpc_id="(134340) Pluto", color="#808"),
    "ix": BodyParams("Ixion", "Иксион", mpc_id="(28978) Ixion", line_width=1.5, is_planet=False),
    "or": BodyParams("Orcus", "Орк", mpc_id="(90482) Orcus", line_width=1.5, is_planet=False),
    "ac": BodyParams("Achlys", "Ахлис", mpc_id="(208996) Achlys", line_width=1.5, is_planet=False),
    "man": BodyParams("Máni", "Мани", mpc_id="(307261) Mani", line_width=1.5, is_planet=False),
    "sal": BodyParams("Salacia", "Салация", mpc_id="(120347) Salacia", line_width=1.5, is_planet=False),
    "ha": BodyParams("Haumea", "Хаумеа", mpc_id="(136108) Haumea", color="#808"),
    "qu": BodyParams("Quaoar", "Квавар", mpc_id="(50000) Quaoar", line_width=1.5, is_planet=False),
    "mk": BodyParams("Makemake", "Макемаке", mpc_id="(136472) Makemake", color="#808"),
    "va": BodyParams("Varda", "Варда", mpc_id="(174567) Varda", line_width=1.5, is_planet=False),
    "ay": BodyParams("Aya", "Айа", mpc_id="(55565) Aya", line_width=1.5, is_planet=False),
    "ch": BodyParams("Chiminigagua", "Чиминигагуа", mpc_id="(532037) Chiminigagua", line_width=1.5, is_planet=False),
    "go": BodyParams("Gonggong", "Гун-гун", mpc_id="(225088) Gonggong", line_width=1.5, is_planet=False),
    "er": BodyParams("Eris", "Эрида", mpc_id="(136199) Eris", color="#808"),
    "se": BodyParams("Sedna", "Седна", mpc_id="(90377) Sedna", line_width=1.5, is_planet=False),
}


def plot_vert_pla(ax: plt.Axes, b1: float, b2: float, show_inner_asteroids: bool = True) -> None:
    """Plots vertical lines and text descriptions for planets and large SSOs."""
    y_text_top = b2 - (b2 * Y_OFFSET_MULTIPLIER)

    for key, body in PL.items():
        y_text_offset = 0
        if key in {"ce", "ves", "pa", "hy", "in"} and not show_inner_asteroids:
            continue

        ax.plot([body.a, body.a], [b1, b2], c=body.color, ls=body.line_style, lw=body.line_width)

        x_offset = 0.02
        if key in {"go", "qu", "or", "sal", "se", "ay", "ch", "man", "va", "ac"}:
            x_offset = -0.65
        elif key in {"ves", "ce", "pa", "hy", "in"}:
            x_offset = -0.078
        elif body.is_planet and body.a < 10:
            x_offset = 0.02
        elif (body.is_planet and body.a > 20) or not body.is_planet:
            x_offset = 0.15

        if body.name not in ("Ixion", "Achlys", ):
            if body.name == "Pallas":
                x_offset = 0.009
            elif body.name == "Interamnia":
                y_text_offset = 350
            elif body.name == "Pluto":
                y_text_offset = 4.25
            ax.text(
                body.a + x_offset,
                y_text_top - y_text_offset,
                body.runame,
                c=body.color,
                rotation="vertical",
                va="top",
                fontsize=15 if body.line_width == 1 else 16,
                bbox={
                    "facecolor": "white",
                    "alpha": 0.8,
                    "edgecolor": "none",
                    "pad": 0.0
                }
            )
    ax.text(
        PL["ix"].a - 0.68, y_text_top - 13, PL["ix"].runame,
        c=PL["ix"].color, rotation="vertical", va="top", fontsize=15 if PL["ix"].line_width == 1 else 16
    )
    ax.text(
        PL["ac"].a + 0.05, y_text_top - 13, PL["ac"].runame,
        c=PL["ac"].color, rotation="vertical", va="top", fontsize=15 if PL["ac"].line_width == 1 else 16
    )

    if show_inner_asteroids:
        ax.text(1.89, b2 * 0.46, "Семейство Венгрии", c="#45714E", rotation="vertical", va="top", fontsize=14)
        ax.text(2.856, b2 * 0.73, "Семейство Корониды", c="#45714E", rotation="vertical", va="top", fontsize=14)
        ax.text(3.39, b2 * 0.46, "Семейство Кибелы", c="#45714E", rotation="vertical", va="top", fontsize=14)


def plot_vert_resonances(ax: plt.Axes, b1: float, b2: float, lw: float = 0.7, plot_tno: bool = False) -> None:
    """Plots Kirkwood gaps and planetary resonances."""
    y_text_top = b2 - (b2 * Y_OFFSET_MULTIPLIER)

    A_JUPITER: Final[float] = 5.202887
    A_NEPTUNE: Final[float] = 30.069923
    # A_NEPTUNE_EFF: Final[float] = 30.195

    resonances_jupiter = [
        (A_JUPITER * (5/1)**(-2/3), "5:1"),
        (A_JUPITER * (4/1)**(-2/3), "4:1"),
        (A_JUPITER * (3/1)**(-2/3), "3:1"),
        (A_JUPITER * (5/2)**(-2/3), "5:2"),
        (A_JUPITER * (7/3)**(-2/3), "7:3"),
        (A_JUPITER * (2/1)**(-2/3), "2:1"),
        (A_JUPITER * (3/2)**(-2/3), "Семейство Хильды, 3:2"),
    ]

    # Индивидуальный учет либрации и барицентрического сдвига
    # NOTE: Effective Neptune axes account for the barycentric shift of the Sun
    # and phase space asymmetry of stable libration zones (Murray & Dermott, "SSD").
    resonances_neptune = [
        (30.125 * (3/4)**(-2/3), "3:4"),
        (30.155 * (2/3)**(-2/3), "2:3"),  # 39.5142, 2:3 (Плутино)
        (30.210 * (4/7)**(-2/3), "4:7"),
        (30.165 * (1/2)**(-2/3), "Тутино, 1:2"),
        (A_NEPTUNE * (2/5)**(-2/3), "2:5"),  # Pure heliocentric value
    ]

    resonances = resonances_jupiter
    if plot_tno:
        resonances = resonances_neptune

    for a, name in resonances:
        x_offset = 0.15 if a > 20 else 0.019
        ax.plot([a, a], [b1, b2], "--k", lw=lw)
        ax.text(a + x_offset, y_text_top, name, rotation="vertical", va="top", fontsize=14)
