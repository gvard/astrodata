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

from dataclasses import dataclass, field
from typing import Final

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

Y_OFFSET_MULTIPLIER = 0.011


@dataclass(slots=True)
class PlotConfig:
    dx: float = 0.01
    dy: float = 150
    color: str = "black"
    bg_color: str = "white"
    line_style: str = "--"
    line_width: float = 2.0


@dataclass(slots=True)  # frozen=True,
class BodyParams:
    name: str
    runame: str
    a: float = 0.0
    e: float = 0.0
    i: float = 0.0
    mpc_id: str = ""
    dv: float = 0
    tt: float = 0
    is_planet: bool = False  # True for both major and dwarf planets.

    plot_configs: dict[str | tuple[str, float, float], PlotConfig] = field(default_factory=dict)

PL: Final[dict[str, BodyParams]] = {
    "me": BodyParams("Mercury", "Меркурий", a=0.3871, e=0.2056, i=7.0050, is_planet=True,
        plot_configs={"line": PlotConfig(color="orange")}),
    "ve": BodyParams("Venus", "Венера", a=0.7233, e=0.0068, i=3.3947, is_planet=True,
        plot_configs={"line": PlotConfig(color="c")}),
    "ea": BodyParams("Earth", "Земля", a=1.00, e=0.0167, i=-0.000015, is_planet=True,
        plot_configs={"line": PlotConfig(color="b")}),
    "ma": BodyParams("Mars", "Марс", a=1.5237, e=0.0934, i=1.8497, is_planet=True,
        plot_configs={"line": PlotConfig(color="r")}),
    "ju": BodyParams("Jupiter", "Юпитер", a=5.2029, e=0.0484, i=1.3044, is_planet=True,
        plot_configs={"line": PlotConfig(color="brown")}),
    "sa": BodyParams("Saturn", "Сатурн", a=9.5367, e=0.0539, i=2.4860, is_planet=True,
        plot_configs={"line": PlotConfig(color="y")}),
    "ur": BodyParams("Uranus", "Уран", a=19.1892, e=0.0473, i=0.7726, is_planet=True,
        plot_configs={"line": PlotConfig(color="c")}),
    "ne": BodyParams("Neptune", "Нептун", a=30.0699, e=0.0086, i=1.7700, is_planet=True,
        plot_configs={"line": PlotConfig(color="#00b")}),
    "ce": BodyParams("Ceres", "Церера", mpc_id="(1) Ceres", is_planet=True,
        plot_configs={"line": PlotConfig(color="m")}),
    "ves": BodyParams("Vesta", "Веста", mpc_id="(4) Vesta", is_planet=False,
        plot_configs={"line": PlotConfig(color="m")}),
    "pa": BodyParams("Pallas", "Паллада", mpc_id="(2) Pallas", is_planet=False,
        plot_configs={"line": PlotConfig(color="m")}),
    "hy": BodyParams("Hygiea", "Гигея", mpc_id="(10) Hygiea", is_planet=False,
        plot_configs={"line": PlotConfig(color="m")}),
    "in": BodyParams("Interamnia", "Интерамния", mpc_id="(704) Interamnia", is_planet=False,
        plot_configs={"line": PlotConfig(color="m")}),
    "pl": BodyParams("Pluto", "Плутон", a=39.4817, e=0.2488, i=17.1418, mpc_id="(134340) Pluto", is_planet=True,
        plot_configs={"line": PlotConfig(color="#808")}),
    "ix": BodyParams("Ixion", "Иксион", mpc_id="(28978) Ixion", is_planet=False,
        plot_configs={"line": PlotConfig(color="grey", line_width=1.5)}),
    "or": BodyParams("Orcus", "Орк", mpc_id="(90482) Orcus", is_planet=False,
        plot_configs={"line": PlotConfig(color="grey", line_width=1.5)}),
    "ac": BodyParams("Achlys", "Ахлис", mpc_id="(208996) Achlys", is_planet=False,
        plot_configs={"line": PlotConfig(color="grey", line_width=1.5)}),
    "man": BodyParams("Máni", "Мани", mpc_id="(307261) Mani", is_planet=False,
        plot_configs={"line": PlotConfig(color="grey", line_width=1.5)}),
    "sal": BodyParams("Salacia", "Салация", mpc_id="(120347) Salacia", is_planet=False,
        plot_configs={"line": PlotConfig(color="grey", line_width=1.5)}),
    "ha": BodyParams("Haumea", "Хаумеа", mpc_id="(136108) Haumea", is_planet=True,
        plot_configs={"line": PlotConfig(color="#808")}),
    "qu": BodyParams("Quaoar", "Квавар", mpc_id="(50000) Quaoar", is_planet=False,
        plot_configs={"line": PlotConfig(color="grey", line_width=1.5)}),
    "mk": BodyParams("Makemake", "Макемаке", mpc_id="(136472) Makemake", is_planet=True,
        plot_configs={"line": PlotConfig(color="#808")}),
    "va": BodyParams("Varda", "Варда", mpc_id="(174567) Varda", is_planet=False,
        plot_configs={"line": PlotConfig(color="grey", line_width=1.5)}),
    "ay": BodyParams("Aya", "Айа", mpc_id="(55565) Aya", is_planet=False,
        plot_configs={"line": PlotConfig(color="grey", line_width=1.5)}),
    "ch": BodyParams("Chiminigagua", "Чиминигагуа", mpc_id="(532037) Chiminigagua", is_planet=False,
        plot_configs={"line": PlotConfig(color="grey", line_width=1.5)}),
    "go": BodyParams("Gonggong", "Гун-гун", mpc_id="(225088) Gonggong", is_planet=False,
        plot_configs={"line": PlotConfig(color="grey", line_width=1.5)}),
    "er": BodyParams("Eris", "Эрида", mpc_id="(136199) Eris", is_planet=True,
        plot_configs={"line": PlotConfig(color="#808")}),
    "se": BodyParams("Sedna", "Седна", mpc_id="(90377) Sedna", is_planet=False,
        plot_configs={"line": PlotConfig(color="grey", line_width=1.5)}),
}

VISITED: Final[dict[str, BodyParams]] = {
    "ce": BodyParams("Ceres", "Церера", mpc_id="(1) Ceres", is_planet=True,
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.05, dy=640, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.07, dy=640, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.05, dy=-11, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.15, dy=19, color="white", bg_color="none"),
        },
    ),
    "ves": BodyParams("Vesta", "Веста", mpc_id="(4) Vesta",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=0.014, dy=200, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.014, dy=130, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.014, dy=6, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.025, dy=4, color="white", bg_color="none"),
        },
    ),
    "ps": BodyParams("Psyche", "Психея", mpc_id="(16) Psyche",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.09, dy=640, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.017, dy=360, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.09, dy=12, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.02, dy=20, color="white", bg_color="none"),
        },
    ),
    "lu": BodyParams("Lutetia", "Лютеция", mpc_id="(21) Lutetia",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=0.016, dy=0, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.016, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.016, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.1, dy=26, color="white", bg_color="none"),
        },
    ),
    "id": BodyParams("Ida", "Ида", mpc_id="(243) Ida",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.065, dy=0, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.13, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.065, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.027, dy=0, color="white", bg_color="none"),
        },
    ),
    "ma": BodyParams("Mathilde", "Матильда", mpc_id="(253) Mathilde",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=0.016, dy=0, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.029, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.016, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.12, dy=-24, color="white", bg_color="none"),
        },
    ),
    "er": BodyParams("Eros", "Эрос", mpc_id="(433) Eros",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.015, dy=590, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.015, dy=590, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.015, dy=11, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.025, dy=20, color="black", bg_color="white"),
        },
    ),
    "ga": BodyParams("Gaspra", "Гаспра", mpc_id="(951) Gaspra",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=0.013, dy=100, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.06, dy=440, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.013, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.09, dy=21, color="white", bg_color="none"),
        },
    ),
    "st": BodyParams("Steins", "Штейнс", mpc_id="(2867) Steins",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=0.016, dy=200, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.012, dy=330, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.016, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.025, dy=0, color="white", bg_color="none"),
        },
    ),
    "to": BodyParams("Toutatis", "Таутатис", mpc_id="(4179) Toutatis",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.12, dy=-300, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.017, dy=330, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.13, dy=-3, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.13, dy=30, color="black", bg_color="white"),
        },
    ),
    "an": BodyParams("Annefrank", "Аннафранк", mpc_id="(5535) Annefrank",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=0.016, dy=0, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.15, dy=-480, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.016, dy=-2, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.025, dy=-8, color="white", bg_color="none"),
        },
    ),
    "br": BodyParams("Braille", "Брайль", mpc_id="(9969) Braille",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=0.016, dy=0, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.027, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.016, dy=0, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.02, dy=20, color="black", bg_color="white"),
        },
    ),
    "it": BodyParams("Itokawa", "Итокава", mpc_id="(25143) Itokawa",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.01, dy=540, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.02, dy=540, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.01, dy=11, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.11, dy=26, color="black", bg_color="white"),
        },
    ),
    "do": BodyParams("Donaldjohanson", "Дональдджохансон", mpc_id="(52246) Donaldjohanson",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=0.009, dy=-400, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.05, dy=-380, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.013, dy=3, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.019, dy=-7, color="white", bg_color="none"),
        },
    ),
    "di": BodyParams("Didymos", "Дидим", mpc_id="(65803) Didymos",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.015, dy=590, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.015, dy=590, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.015, dy=11, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.02, dy=20, color="black", bg_color="white"),
        },
    ),
    "tor": BodyParams("Torifune", "Торифунэ", mpc_id="(98943) Torifune",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=0.018, dy=0, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.027, dy=0, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.018, dy=0, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.018, dy=-18, color="black", bg_color="white"),
        },
    ),
    "be": BodyParams("Bennu", "Бенну", mpc_id="(101955) Bennu",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.025, dy=540, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.025, dy=540, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.035, dy=11, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.033, dy=11, color="black", bg_color="white"),
        },
    ),
    "pl": BodyParams("Pluto", "Плутон", mpc_id="(134340) Pluto", is_planet=True,
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=0.0, dy=0, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.0, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.0, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.0, dy=0, color="white", bg_color="none"),
        },
    ),
    "din": BodyParams("Dinkinesh", "Динкинеш", mpc_id="(152830) Dinkinesh",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.14, dy=-400, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.29, dy=0, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.14, dy=-8, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.14, dy=-24, color="black", bg_color="white"),
        },
    ),
    "se": BodyParams("Selam", "Селам", mpc_id="(152830) Selam",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=0.0, dy=0, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.0, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.0, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.0, dy=0, color="white", bg_color="none"),
        },
    ),
    "ry": BodyParams("Ryugu", "Рюгу", mpc_id="(162173) Ryugu",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.015, dy=500, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.016, dy=300, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.031, dy=13, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.068, dy=29, color="black", bg_color="white"),
        },
    ),
    "ka": BodyParams("Kamo`oalewa", "Камоалева", mpc_id="(469219) Kamo`oalewa",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.05, dy=640, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.05, dy=640, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.01, dy=-12, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.018, dy=-18, color="black", bg_color="white"),
        },
    ),
    "ar": BodyParams("Arrokoth", "Аррокот", mpc_id="(486958) Arrokoth",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=0.0, dy=0, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.0, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.0, dy=0, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.0, dy=0, color="white", bg_color="none"),
        },
    ),
    "ph": BodyParams("Phaethon", "Фаэтон", mpc_id="(3200) Phaethon",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.05, dy=640, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.05, dy=640, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.05, dy=12, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.21, dy=12, color="black", bg_color="white"),
        },
    ),
    "eu": BodyParams("Eurybates", "Эврибат", mpc_id="(3548) Eurybates",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.2, dy=-640, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.19, dy=-630, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.2, dy=-12, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.24, dy=-15, color="black", bg_color="white"),
        },
    ),
    "po": BodyParams("Polymele", "Полимела", mpc_id="(15094) Polymele",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.2, dy=640, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.26, dy=615, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.2, dy=12, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.28, dy=12, color="black", bg_color="white"),
        },
    ),
    "ap": BodyParams("Apophis", "Апофис", mpc_id="(99942) Apophis",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.05, dy=640, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.19, dy=640, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.05, dy=12, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=-0.15, dy=12, color="black", bg_color="white"),
        },
    ),
    "apl": BodyParams("APL", "APL", mpc_id="(132524) APL",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.05, dy=580, color="white", bg_color="none"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=0.01, dy=360, color="white", bg_color="none"),
            ("tt", 0.59, 2.9): PlotConfig(dx=-0.05, dy=12, color="white", bg_color="none"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.019, dy=21, color="white", bg_color="none"),
        },
    ),
    "ky": BodyParams("1998 KY26", "1998 KY26", mpc_id="1998 KY26",
        plot_configs={
            ("deltav", 0.59, 2.9): PlotConfig(dx=-0.05, dy=640, color="black", bg_color="white"),
            ("deltav", 0.59, 5.3): PlotConfig(dx=-0.19, dy=640, color="black", bg_color="white"),
            ("tt", 0.59, 2.9): PlotConfig(dx=0.015, dy=12, color="black", bg_color="white"),
            ("tt", 0.59, 5.3): PlotConfig(dx=0.027, dy=7, color="black", bg_color="white"),
        },
    ),
}


def plot_vert_pla(
    ax: Axes,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    xoff: float = 0,
    show_inner_asteroids: bool = True,
) -> None:
    """Plots vertical lines and text descriptions for planets and large SSOs."""
    y_text_top = ylim[1] - (ylim[1] * Y_OFFSET_MULTIPLIER)

    for key, body in PL.items():
        y_text_offset: float = 0
        if key in {"ce", "ves", "pa", "hy", "in"} and not show_inner_asteroids:
            continue

        if body.a < xlim[0] or body.a > xlim[1]:
            continue

        cfg = body.plot_configs.get("line", PlotConfig(color="grey"))

        ax.plot(
            [body.a, body.a],
            [ylim[0], ylim[1]],
            c=cfg.color,
            ls=cfg.line_style,
            lw=cfg.line_width,
        )

        x_offset = 0.02
        if key in {"go", "qu", "or", "sal", "se", "ay", "ch", "man", "va", "ac"}:
            x_offset = -0.65
        elif key in {"ves", "ce", "pa", "hy", "in"}:
            x_offset = -0.078
        elif body.is_planet and body.a < 10:
            x_offset = 0.02
        elif (body.is_planet and body.a > 20) or not body.is_planet:
            x_offset = 0.15

        if body.name not in (
            "Ixion",
            "Achlys",
        ):
            if body.name == "Pallas":
                x_offset = 0.009
            elif body.name == "Interamnia":
                y_text_offset = 350
            elif body.name == "Pluto":
                y_text_offset = 4.25
            ax.text(
                body.a + x_offset - xoff,
                y_text_top - y_text_offset,
                body.runame,
                c=cfg.color,
                rotation="vertical",
                va="top",
                fontsize=15 if cfg.line_width == 1 else 16,
                bbox={
                    "facecolor": "white",
                    "alpha": 0.8,
                    "edgecolor": "none",
                    "pad": 0.0,
                },
            )
    ix_cfg = PL["ix"].plot_configs.get("line", PlotConfig())
    ac_cfg = PL["ac"].plot_configs.get("line", PlotConfig())
    ax.text(
        PL["ix"].a - 0.68,
        y_text_top - 13,
        PL["ix"].runame,
        c=ix_cfg.color,
        rotation="vertical",
        va="top",
        fontsize=15 if ix_cfg.line_width == 1 else 16,
    )
    ax.text(
        PL["ac"].a + 0.05,
        y_text_top - 13,
        PL["ac"].runame,
        c=ac_cfg.color,
        rotation="vertical",
        va="top",
        fontsize=15 if ac_cfg.line_width == 1 else 16,
    )

    if show_inner_asteroids:
        ax.text(
            1.89,
            ylim[1] * 0.46,
            "Семейство Венгрии",
            c="#45714E",
            rotation="vertical",
            va="top",
            fontsize=14,
        )
        ax.text(
            2.856,
            ylim[1] * 0.73,
            "Семейство Корониды",
            c="#45714E",
            rotation="vertical",
            va="top",
            fontsize=14,
        )
        ax.text(
            3.39,
            ylim[1] * 0.46,
            "Семейство Кибелы",
            c="#45714E",
            rotation="vertical",
            va="top",
            fontsize=14,
        )


def plot_vert_resonances(
    ax: Axes, b1: float, b2: float, lw: float = 0.7, plot_tno: bool = False
) -> None:
    """Plots Kirkwood gaps and planetary resonances."""
    y_text_top = b2 - (b2 * Y_OFFSET_MULTIPLIER)

    A_JUPITER: Final[float] = 5.202887
    A_NEPTUNE: Final[float] = 30.069923
    # A_NEPTUNE_EFF: Final[float] = 30.195

    resonances_jupiter = [
        (A_JUPITER * (5 / 1) ** (-2 / 3), "5:1"),
        (A_JUPITER * (4 / 1) ** (-2 / 3), "4:1"),
        (A_JUPITER * (3 / 1) ** (-2 / 3), "3:1"),
        (A_JUPITER * (5 / 2) ** (-2 / 3), "5:2"),
        (A_JUPITER * (7 / 3) ** (-2 / 3), "7:3"),
        (A_JUPITER * (2 / 1) ** (-2 / 3), "2:1"),
        (A_JUPITER * (3 / 2) ** (-2 / 3), "Семейство Хильды, 3:2"),
    ]

    # Индивидуальный учет либрации и барицентрического сдвига
    # NOTE: Effective Neptune axes account for the barycentric shift of the Sun
    # and phase space asymmetry of stable libration zones (Murray & Dermott, "SSD").
    resonances_neptune = [
        (30.125 * (3 / 4) ** (-2 / 3), "3:4"),
        (30.155 * (2 / 3) ** (-2 / 3), "2:3"),  # 39.5142, 2:3 (Плутино)
        (30.210 * (4 / 7) ** (-2 / 3), "4:7"),
        (30.165 * (1 / 2) ** (-2 / 3), "Тутино, 1:2"),
        (A_NEPTUNE * (2 / 5) ** (-2 / 3), "2:5"),  # Pure heliocentric value
    ]

    resonances = resonances_jupiter
    if plot_tno:
        resonances = resonances_neptune

    for a, name in resonances:
        x_offset = 0.15 if a > 20 else 0.019
        ax.plot([a, a], [b1, b2], "--k", lw=lw)
        ax.text(
            a + x_offset, y_text_top, name, rotation="vertical", va="top", fontsize=14
        )
