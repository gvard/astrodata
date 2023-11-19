"""Plot parameters of Solar system bodies
"""

import matplotlib.pyplot as plt


PL = {
    "me": {"n": "Меркурий", "a": 0.387, "e": 0.206, "i": 7},
    "ve": {"n": "Венера", "a": 0.723, "e": 0.007, "i": 3.4},
    "ea": {"n": "Земля", "a": 1, "e": 0.016, "i": 0},
    "ma": {"n": "Марс", "a": 1.524, "e": 0.093, "i": 1.85},
    "ju": {"n": "Юпитер", "a": 5.204, "e": 0.049, "i": 1.3},
    "sa": {"n": "Сатурн", "a": 9.583, "e": 0.057, "i": 2.49},
    "ur": {"n": "Уран", "a": 19.219, "e": 0.046, "i": 0.77},
    "ne": {"n": "Нептун", "a": 30.07, "e": 0.01, "i": 1.77},
    "ce": {"n": "Церера", "a": 2.77, "e": 0.076, "i": 10.6},
    "pl": {"n": "Плутон, 2:3", "a": 39.48, "e": 0.249, "i": 17.16},
    "ha": {"n": "Хаумеа", "a": 43.12, "e": 0.196, "i": 28.2},
    "mk": {"n": "Макемаке", "a": 45.43, "e": 0.161, "i": 29},
    "er": {"n": "Эрида", "a": 67.86, "e": 0.436, "i": 44.04},
    "go": {"n": "Гун-гун", "a": 67.485, "e": 0.499, "i": 30.6},
    "se": {"n": "Седна", "a": 491.5, "e": 0.845, "i": 11.93},
}


def plot_vert_pla(b1, b2, off=0.6, ash=0.02, veroff=10, ve=True):
    """Plot vertical lines and its text descriptions for planets, dwarf planets
    and largest tran-Neptunian objects.
    """
    dark_magenta = "#808"
    plt.plot([PL["ve"]["a"], PL["ve"]["a"]], [b1, b2], "--c")
    plt.text(
        PL["ve"]["a"] + ash,
        b2 - veroff,
        PL["ve"]["n"],
        c="c",
        rotation="vertical",
        va="top",
        fontsize=14,
    )
    plt.plot([PL["ea"]["a"], PL["ea"]["a"]], [b1, b2], "--b")
    plt.text(
        PL["ea"]["a"] + ash,
        b2 - veroff,
        PL["ea"]["n"],
        c="b",
        rotation="vertical",
        va="top",
        fontsize=14,
    )
    plt.plot([PL["ma"]["a"], PL["ma"]["a"]], [b1, b2], "--r")
    plt.text(
        PL["ma"]["a"] + ash,
        b2 - veroff,
        PL["ma"]["n"],
        c="r",
        rotation="vertical",
        va="top",
        fontsize=14,
    )
    if ve:
        plt.text(
            1.89,
            500,
            "Семейство Венгрии",
            c="#45714E",
            rotation="vertical",
            va="top",
            fontsize=14,
        )
    plt.plot([PL["ce"]["a"], PL["ce"]["a"]], [b1, b2], "--m")
    plt.text(
        PL["ce"]["a"] - 0.07,
        b2 - veroff,
        PL["ce"]["n"],
        c="m",
        rotation="vertical",
        va="top",
        fontsize=14,
    )
    plt.plot([PL["ju"]["a"], PL["ju"]["a"]], [b1, b2], "--", color="brown")
    plt.text(
        PL["ju"]["a"] + 0.02,
        b2 - veroff,
        PL["ju"]["n"],
        c="brown",
        rotation="vertical",
        va="top",
        fontsize=14,
    )
    plt.plot([PL["sa"]["a"], PL["sa"]["a"]], [b1, b2], "--y")
    plt.plot([PL["ur"]["a"], PL["ur"]["a"]], [b1, b2], "--c")
    plt.plot([PL["ne"]["a"], PL["ne"]["a"]], [b1, b2], "--", color="#00b", lw=2.3)
    plt.text(
        PL["ne"]["a"] + 0.15,
        b2 - off,
        PL["ne"]["n"],
        color="#00b",
        rotation="vertical",
        va="top",
        fontsize=16,
    )
    plt.plot([PL["pl"]["a"], PL["pl"]["a"]], [b1, b2], "--", color=dark_magenta, lw=2.3)
    plt.text(
        PL["pl"]["a"] + 0.15,
        b2 - off,
        PL["pl"]["n"],
        c="black",
        rotation="vertical",
        va="top",
        fontsize=16,
    )
    plt.plot([PL["er"]["a"], PL["er"]["a"]], [b1, b2], "--", color=dark_magenta, lw=2.3)
    plt.text(
        PL["er"]["a"] + 0.15,
        b2 - off,
        PL["er"]["n"],
        c="black",
        rotation="vertical",
        va="top",
        fontsize=16,
    )
    plt.plot([PL["ha"]["a"], PL["ha"]["a"]], [b1, b2], "--", color=dark_magenta, lw=2.3)
    plt.text(
        PL["ha"]["a"] + 0.15,
        b2 - off,
        PL["ha"]["n"],
        c="black",
        rotation="vertical",
        va="top",
        fontsize=16,
    )
    plt.plot([PL["mk"]["a"], PL["mk"]["a"]], [b1, b2], "--", color=dark_magenta, lw=2.3)
    plt.text(
        PL["mk"]["a"] + 0.15,
        b2 - off,
        PL["mk"]["n"],
        c="black",
        rotation="vertical",
        va="top",
        fontsize=16,
    )
    plt.plot([PL["go"]["a"], PL["go"]["a"]], [b1, b2], "--", color="grey")
    plt.text(
        PL["go"]["a"] - 0.75,
        b2 - off,
        PL["go"]["n"],
        c="grey",
        rotation="vertical",
        va="top",
        fontsize=16,
    )
    plt.plot([PL["se"]["a"], PL["se"]["a"]], [b1, b2], "--", color="grey")
    plt.text(
        PL["se"]["a"] + 0.15,
        b2 - off,
        PL["se"]["n"],
        c="grey",
        rotation="vertical",
        va="top",
        fontsize=16,
    )


def plot_vert_resonances(b1, b2, off=0.6, veroff=10, lw=0.7, plot_tno=False):
    """Plot vertical lines and its text descriptions for Kirkwood gaps and other
    resonanses with Solar system planets.
    """
    for a, b in (
        (1.78, "5:1"),
        (2.065, "4:1"),
        (2.502, "3:1"),
        (2.825, "5:2"),
        (2.958, "7:3"),
        (3.279, "2:1"),
        (3.972, "Семейство Хильды, 3:2"),
    ):
        plt.plot([a, a], [b1, b2], "--k", lw=lw)
        plt.text(a + 0.02, b2 - veroff, b, rotation="vertical", va="top", fontsize=14)
    if plot_tno:
        for a, b in ((36.5, "3:4"), (43.92, "4:7"), (47.8, "1:2"), (55.4, "2:5")):
            plt.plot([a, a], [b1, b2], "--k", lw=lw)
            plt.text(a + 0.15, b2 - off, b, rotation="vertical", va="top", fontsize=14)


def planets_ae(mode="e"):
    """Plot points for Solar system planets in a-e plane."""
    plt.plot(0, 0, "oy", ms=12)
    plt.plot(PL["me"]["a"], PL["me"][mode], "o", color="orange", ms=6)
    plt.plot(PL["ve"]["a"], PL["ve"][mode], "oc", ms=6)
    plt.plot(1, PL["ea"][mode], "ob", ms=6)
    plt.plot(PL["ma"]["a"], PL["ma"][mode], "or", ms=6)
    plt.plot(PL["ju"]["a"], PL["ju"][mode], "o", color="brown", ms=6)
    plt.plot(PL["sa"]["a"], PL["sa"][mode], "oy", ms=6)
    plt.plot(PL["ur"]["a"], PL["ur"][mode], "oc", ms=6)
    plt.plot(PL["ne"]["a"], PL["ne"][mode], "ob", ms=6)
    plt.plot(PL["ce"]["a"], PL["ce"][mode], "om", ms=6)
    plt.plot(PL["pl"]["a"], PL["pl"][mode], "om", ms=6)
    plt.plot(PL["ha"]["a"], PL["ha"][mode], "om", ms=6)
    plt.plot(PL["mk"]["a"], PL["mk"][mode], "om", ms=6)
    plt.plot(PL["er"]["a"], PL["er"][mode], "om", ms=6)
    plt.plot(PL["go"]["a"], PL["go"][mode], "o", color="grey", ms=6)
