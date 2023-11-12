"""Python script for plotting histograms with the distribution of
Solar system objects along the semimajor axis.
Data source: https://www.minorplanetcenter.net/iau/MPCORB.html
"""

from datetime import datetime
import locale
from argparse import ArgumentParser

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

from plot_sso_supply import plot_vert_pla, plot_vert_resonances


parser = ArgumentParser(description="Graph plotter script with distribution of Solar system objects")
parser.add_argument("-t", "--translate", action="store_true",
                    help="translate all inscriptions into Russian")

args = parser.parse_args()

LOC = "en_US"
if args.translate:
    LOC = "ru_RU"

locale.setlocale(locale.LC_ALL, LOC)
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year
LOC = "-ru" if args.translate else ""
PLOTS_DIR = "../../../plots/solarsystem/"
DATA_DIR = "../../../data/"
DATA = np.genfromtxt(
    DATA_DIR+'MPCORB.DAT.gz', usecols=(8, 10), skip_header=43,
    delimiter=(
        7, 6, 7, 5, 10,
        11, 11, 11, 11, 12,
        14, 2, 10, 6, 4,
        10, 5, 4, 4, 11,
        5, 28, 9
    ),
    dtype=[
        ("Names", "U7"), ("H", "f8"), ("G", "f8"), ("Ep", "U5"), ("M", "f8"),
        ("Peri", "f8"), ("Node", "f8"), ("i", "f8"), ("e", "f8"), ("n", "f8"),
        ("a", "f8"), ("U", "U1"), ("Ref", "U10"), ("Obs", "int"), ("Opp", "int"),
        ("Arc", "U9"), ("rms", "f8"), ("p1", "U3"), ("p2", "U3"), ("Com", "U10"),
        ("Flags", "U4"), ("Desig", "U27"), ("Last", "int"),
    ])

for a1, a2, b1, b2, bins, xmal, plot_tno, objs_nam in (
        (0.7, 5.4, 0, 1190, 8000, 0.5, False, "малых планет"),
        (29, 70, 0, 49.2, 900, 5, True, "транснептуновых объектов")):
    Filtered = DATA[DATA["a"] >= a1]
    Filtered = Filtered[Filtered["a"] <= a2]
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)
    ax.xaxis.set_major_locator(MultipleLocator(xmal))
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    plt.hist(Filtered["a"], bins=bins)
    plot_vert_pla(b1, b2)
    plot_vert_resonances(b1, b2, plot_tno=plot_tno)
    plt.xlim(a1, a2)
    plt.ylim(b1, b2)
    plt.title(
        f"Распределение {len(Filtered)} {objs_nam} по большой полуоси. "
        + f"{MONTH} {YEAR} года", fontsize=15)
    plt.xlabel("Большая полуось орбиты, а.е.", fontsize=14)
    plt.ylabel("Количество объектов", fontsize=14)
    plt.savefig(PLOTS_DIR + f"mpcorb-hist-a{a1}-{a2}{LOC}.png", dpi=120)
