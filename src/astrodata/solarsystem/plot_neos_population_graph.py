"""Python script for plotting graph with statistics of near-Earth objects.
Data taken from: https://cneos.jpl.nasa.gov/stats/totals.html
List of successfully predicted asteroid impacts:
https://en.wikipedia.org/wiki/Asteroid_impact_prediction#List_of_successfully_predicted_asteroid_impacts
"""

import csv
import locale
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from scour import scour


def optimize_svg(tmp_pth, pth):
    """Optimize svg file using scour"""
    with open(tmp_pth, "rb") as inputfile, open(pth, "wb") as outputfile:
        options = scour.generateDefaultOptions()
        options.enable_viewboxing = True
        options.strip_comments = True
        options.strip_ids = True
        options.remove_metadata = True
        options.shorten_ids = True
        options.indent_type = "none"
        options.newlines = False
        scour.start(options, inputfile, outputfile)


def save_plot(fig, filename: str, loc_suffix: str, ext: str = "png", dpi: int = 160):
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    final_pth = PLOTS_DIR / f"{filename}{loc_suffix}.{ext}"

    if ext == "svg":
        tmp_pth = PLOTS_DIR / f"{filename}{loc_suffix}_.{ext}"
        fig.savefig(tmp_pth, dpi=dpi)
        optimize_svg(tmp_pth, final_pth)
        tmp_pth.unlink()
    else:
        fig.savefig(final_pth, dpi=dpi)

    plt.close(fig)


parser = ArgumentParser(description="Graph plotter script with statistics of near-Earth objects")
parser.add_argument("-t", "--translate", action="store_true",
                    help="translate all inscriptions into Russian")

args = parser.parse_args()

PLOTS_DIR = Path("../../../plots/solarsystem")
CSV_PTH = "../../../data/solarsystem/Discovery Statistics.csv"
DPI = 160

with open(CSV_PTH) as csvfile:
    reader = csv.DictReader(csvfile)
    dats, pha_nums, phakm_nums, nea_nums, neo_nums = [], [], [], [], []
    neakm_nums, nea140_nums = [], []
    for row in reader:
        dats.append(datetime.strptime(row["Date"], "%Y-%m-%d"))
        pha_nums.append(int(row["PHA"]))
        phakm_nums.append(int(row["PHA-km"]))
        nea_nums.append(int(row["NEA"]))
        neakm_nums.append(int(row["NEA-km"]))
        nea140_nums.append(int(row["NEA-140m"]))
        neo_nums.append(int(row["NEO"]))

LOCALE = "en_US"
if args.translate:
    LOCALE = "ru_RU"
locale.setlocale(locale.LC_ALL, LOCALE)
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year
CROP = -12
COLORS = plt.rcParams["axes.prop_cycle"].by_key()["color"]
XLIM = datetime(year=2002, month=1, day=1), today + timedelta(weeks=7)

fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.05, 0.06, 0.99, 0.97)
years = mdates.YearLocator(1)
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))

ax.plot(dats[:CROP], neo_nums[:CROP], ".-", label="Околоземные объекты", ms=2, lw=1)
ax.plot(dats[:CROP], nea_nums[:CROP], ".-", label="Околоземные астероиды", ms=2, lw=1)
ax.plot(dats[:CROP], nea140_nums[:CROP], ".-", label="Околоземные астероиды от 140 м",
         ms=5, lw=2)
ax.plot(dats[:CROP], pha_nums[:CROP], ".-k", label="Потенциально опасные астероиды",
         ms=5, lw=2)
ax.plot(dats[:CROP], neakm_nums[:CROP], ".-", color=COLORS[4],
         label="Околоземные астероиды от 1 км", ms=5, lw=2)
ax.plot(dats[:CROP], phakm_nums[:CROP], ".-", color=COLORS[3],
         label="Потенциально опасные астероиды от 1 км", ms=5, lw=2)

YLIM = (0, neo_nums[0] + 700)
ax.set_ylim(YLIM)
ax.legend(fontsize=13)
ax.set_xlim(XLIM)
ax.set_title(
    f"Динамика открытий околоземных объектов. Всего {nea_nums[0]} "
    + f"околоземных и {pha_nums[0]} потенциально опасных астероидов. {MONTH} {YEAR} года",
    fontsize=14,
)
ax.set_xlabel("Дата открытия, годы", fontsize=13)
ax.set_ylabel("Количество объектов", fontsize=13, labelpad=1)
ax.grid(linestyle="dotted")

LANG_SUFFIX = "-ru" if args.translate else ""
FILE_EXT = "png"
FILENAME = "neo_pha_graph-2002"

save_plot(fig, FILENAME, LANG_SUFFIX, FILE_EXT, DPI)

fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))

ax.plot(dats[:CROP], pha_nums[:CROP], ".-k", label="Потенциально опасные астероиды",
         ms=5, lw=2)
ax.plot(dats[:CROP], neakm_nums[:CROP], ".-", color=COLORS[4],
         label="Околоземные астероиды от 1 км", ms=5, lw=2)
ax.plot(dats[:CROP], phakm_nums[:CROP], ".-", color=COLORS[3],
         label="Потенциально опасные астероиды от 1 км", ms=5, lw=2)

@dataclass(frozen=True, slots=True)
class Accident:
    name: str
    date_discovery: datetime
    date_impact: datetime
    x_shift_weeks: float = 14.5
    y_shift: int = 2180


yshift = 2480

accidents = [
    Accident("2008 TC3", datetime(2008, 10, 6), datetime(2008, 10, 7, 2, 46), y_shift=2120),
    Accident("2014 AA", datetime(2014, 1, 1), datetime(2014, 1, 2, 3, 4), y_shift=yshift),
    Accident("2018 LA", datetime(2018, 6, 2), datetime(2018, 6, 2, 16, 45), y_shift=yshift),
    Accident("2019 MO", datetime(2019, 6, 22), datetime(2019, 6, 22, 21, 26), y_shift=yshift),
    Accident("2022 EB5", datetime(2022, 3, 11), datetime(2022, 3, 11, 21, 22)),
    Accident("2022 WJ1", datetime(2022, 11, 19), datetime(2022, 11, 19, 8, 26)),
    Accident("2023 CX1", datetime(2023, 2, 12), datetime(2023, 2, 13, 2, 59), x_shift_weeks=-6),
    Accident("2024 BX1", datetime(2024, 1, 20), datetime(2024, 1, 21, 0, 32)),
    Accident("2024 RW1", datetime(2024, 9, 4), datetime(2024, 9, 4, 16, 39), x_shift_weeks=27),
    Accident("2024 UQ", datetime(2024, 10, 22), datetime(2024, 10, 22, 10, 54), x_shift_weeks=21),
    Accident("2024 XA1", datetime(2024, 12, 3), datetime(2024, 12, 3, 16, 14), x_shift_weeks=-4),
    Accident("2026 JN4", datetime(2026, 5, 15), datetime(2026, 5, 15, 13, 39)),
    Accident("2026 RW1", datetime(2026, 9, 6), datetime(2026, 9, 6, 16, 7)),
]

for i, ac in enumerate(accidents):
    label = "Успешно предсказанные столкновения с Землей" if i == 0 else None
    # ax.axvline(ac.date_discovery, color="g", linestyle="--", label=label)
    ax.axvline(ac.date_impact, color="g", linestyle="--", label=label)

    text_x = ac.date_impact - timedelta(weeks=ac.x_shift_weeks)
    ax.text(
        text_x,
        ac.y_shift,
        ac.name,
        color="#444",
        rotation="vertical",
        va="top",
        fontsize=13,
    )

YLIM = (0, pha_nums[0] + 70)
ax.set_ylim(YLIM)
ax.legend(fontsize=13)
ax.set_xlim(XLIM)
ax.yaxis.set_minor_locator(MultipleLocator(100))
ax.set_title(
    f"Динамика открытий околоземных объектов. Всего {nea_nums[0]} "
    + f"околоземных и {pha_nums[0]} потенциально опасных астероида. {MONTH} {YEAR} года",
    fontsize=14,
)
ax.set_xlabel("Дата открытия, годы", fontsize=13)
ax.set_ylabel("Количество объектов", fontsize=13)
# ax.grid(linestyle="dotted", axis='x')

FILE_EXT = "png"
FILENAME = "pha_graph_predicted_impacts-2002"

save_plot(fig, FILENAME, LANG_SUFFIX, FILE_EXT, DPI)
