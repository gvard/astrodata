"""Python script for plotting graph with number of people in space.
Data taken from Jonathan's Space Pages:
https://planet4589.org/space/astro/web/pop.html
List of spaceflight-related accidents:
https://en.wikipedia.org/wiki/List_of_spaceflight-related_accidents_and_incidents
"""

from datetime import datetime, timedelta
import os
import locale
import urllib.request
import argparse
import json
import textwrap
from decimal import Decimal
import csv

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from scour import scour
from astropy.time import Time


class CompactJSONEncoder(json.JSONEncoder):
    """A JSON Encoder that puts small containers on single lines.
    https://gist.github.com/jannismain/e96666ca4f059c3e5bc28abb711b5c92
    """

    CONTAINER_TYPES = (list, tuple, dict)
    """Container datatypes include primitives or other containers."""

    MAX_WIDTH = 134
    """Maximum width of a container that might be put on a single line."""

    MAX_ITEMS = 7
    """Maximum number of items in container that might be put on single line."""

    def __init__(self, *args, **kwargs):
        # using this class without indentation is pointless
        if kwargs.get("indent") is None:
            kwargs["indent"] = 2
        super().__init__(*args, **kwargs)
        self.indentation_level = 0

    def encode(self, o):
        """Encode JSON object *o* with respect to single line lists."""
        if isinstance(o, (list, tuple)):
            return self._encode_list(o)
        if isinstance(o, dict):
            return self._encode_object(o)
        if isinstance(o, float):
            return format(Decimal(str(o)), "f")
            # return format(o, "g")  # Use scientific notation for floats

        return json.dumps(
            o,
            skipkeys=self.skipkeys,
            ensure_ascii=self.ensure_ascii,
            check_circular=self.check_circular,
            allow_nan=self.allow_nan,
            sort_keys=self.sort_keys,
            indent=self.indent,
            separators=(self.item_separator, self.key_separator),
            default=self.default if hasattr(self, "default") else None,
        )

    def _encode_list(self, o):
        if self._put_on_single_line(o):
            return "[" + ",".join(self.encode(el) for el in o) + "]"
        self.indentation_level += 1
        output = [self.indent_str + self.encode(el) for el in o]
        self.indentation_level -= 1
        return "[\n" + ",\n".join(output) + "\n" + self.indent_str + "]"

    def _encode_object(self, o):
        if not o:
            return "{}"
        if self._put_on_single_line(o):
            return (
                "{"
                + ", ".join(
                    f"{self.encode(k)}: {self.encode(el)}" for k, el in o.items()
                )
                + "}"
            )
        self.indentation_level += 1
        output = [
            f"{self.indent_str}{json.dumps(k)}: {self.encode(v)}" for k, v in o.items()
        ]

        self.indentation_level -= 1
        return "{\n" + ",\n".join(output) + "\n" + self.indent_str + "}"

    def iterencode(self, o, **kwargs):
        """Required to also work with `json.dump`."""
        return self.encode(o)

    def _put_on_single_line(self, o):
        return (
            self._primitives_only(o)
            and len(o) <= self.MAX_ITEMS
            and len(str(o)) - 2 <= self.MAX_WIDTH
        )

    def _primitives_only(self, o: list | tuple | dict):
        if isinstance(o, (list, tuple)):
            return not any(isinstance(el, self.CONTAINER_TYPES) for el in o)
        elif isinstance(o, dict):
            return not any(isinstance(el, self.CONTAINER_TYPES) for el in o.values())

    @property
    def indent_str(self) -> str:
        if isinstance(self.indent, int):
            return " " * (self.indentation_level * self.indent)
        elif isinstance(self.indent, str):
            return self.indentation_level * self.indent
        else:
            raise ValueError(
                f"indent must either be of type int or str (is: {type(self.indent)})"
            )


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


def unite_legends(axes):
    """Hack to display legend over other plots
    https://github.com/matplotlib/matplotlib/issues/3706#issuecomment-164265176
    """
    han, lab = [], []
    for ax in axes:
        tmp = ax.get_legend_handles_labels()
        han.extend(tmp[0])
        lab.extend(tmp[1])
    return han, lab


def get_table(url, local=False):
    """Read ASCII data table from pre html element"""
    if local:
        html = open(url, encoding="utf-8")
    else:
        html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html5lib")
    return soup.find("table").findAll("tr")


parser = argparse.ArgumentParser(
    description="Graph plotter script with number of people in space"
)
parser.add_argument("-m", "--method", action="store_true", help="Switch to plt.stairs method")
parser.add_argument("-f", "--filled", action="store_true", help="Fill plot area")
parser.add_argument("-a", "--accidents", action="store_true", help="Plot accidents dates")
parser.add_argument("-p", "--private", action="store_true", help="Plot private spaceflights dates")
parser.add_argument("-s", "--spent", action="store_true",
                    help="Plot total time spent by humans in space")
parser.add_argument("-t", "--translate", action="store_true",
                    help="translate all inscriptions into Russian")
args = parser.parse_args()

SPACEPOP_URL = "https://planet4589.org/space/astro/web/pop.html"

data = get_table(SPACEPOP_URL)
nums, dats, mjds, manyrs, manyr_sums = [], [], [], [], []
dataj, datac = [], []
orbnums, recsnums, reconums = [], [], []
for i, tr in enumerate(data[3:]):
    tds = tr.findAll("td")
    mjds.append(float(tds[0].text))
    nums.append(int(tds[1].text))
    orbnums.append(int(tds[2].text))
    recsnums.append(int(tds[3].text))
    reconums.append(int(tds[4].text))
    dt = datetime.strptime(tds[5].text.strip(), "%Y %b %d %H%M:%S")
    dats.append(dt)
    datac.append((
        dt.isoformat(),  # .strftime("%Y-%m-%dT%H:%M:%S"),
        float(tds[0].text),
        int(tds[1].text),
        int(tds[2].text),
        int(tds[3].text),
        int(tds[4].text),
    ))
    dataj.append({
        "mjd": float(tds[0].text),
        "date": dt.isoformat(),  # .strftime("%Y-%m-%d %H:%M:%S"),
        "spop": int(tds[1].text),
        "opop": int(tds[2].text),
        "recsp": int(tds[3].text),
        "recop": int(tds[4].text),
    })

mjds = mjds[::-1]
nums = nums[::-1]
orbnums = orbnums[::-1]
recsnums = recsnums[::-1]
reconums = reconums[::-1]
reconums.append(reconums[-1])
recsnums.append(recsnums[-1])
dats = dats[::-1]
for i, nn in enumerate(nums):
    if i:
        manyrs.append((mjds[i] - mjds[i - 1]) * nums[i - 1] / 365.2425)
    manyr_sums.append(sum(manyrs))
manyrs.append((Time.now().mjd - mjds[i - 1]) * nums[i - 1] / 365.2425)
manyr_sums.append(sum(manyrs))

# For reverse chronological order comment this lines:
dataj = dataj[::-1]
datac = datac[::-1]

fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.94, 0.97)  # 0.99
years = mdates.YearLocator(5)  # 1 2
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.yaxis.set_major_locator(MultipleLocator(1))

LOC = "en_US"
if args.translate:
    LOC = "ru_RU"
locale.setlocale(locale.LC_ALL, LOC)
with open(f"../locales/mannedflights-{LOC[:2]}.json", "r", encoding="utf8") as loc_file:
    msgs = json.load(loc_file)
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year

data_to_plot = dats + [today]
dats_rec = dats + [today + timedelta(days=365)]
nums_to_plot = nums + [nums[-1]]
if not args.method:
    LW = 0.9
    if args.filled:
        data_to_plot.append(today)
        nums_to_plot.append(0)
        ax.fill_between(data_to_plot, nums_to_plot, step="post", color="#229")
        LW = 0.5
    if args.filled:
        ax.step(data_to_plot, nums_to_plot, "b", where="post", lw=LW)
    else:
        ax.step(data_to_plot, nums_to_plot, "b", where="post", lw=LW,
                label="Число людей в космосе (высота >80 км)")
    ax.step(dats_rec, recsnums, "--", where="post", lw=2.5, color="darkorange",
            label="Рекордное число людей на высоте более 80.5 км", zorder=3)
    ax.step(dats_rec, reconums, "--k", where="post", lw=2.5,
            label="Рекордное число людей на орбите", zorder=4)
else:
    ax.stairs(nums, data_to_plot, fill=args.filled, alpha=1, color="b")  # baseline=None

tdlt = timedelta(days=300)
plt.xlim(dats[0] - tdlt / 2, dats[-1] + tdlt)
# plt.xlim(datetime(year=1960, month=1, day=1), datetime(year=1987, month=1, day=1))
# plt.xlim(datetime(year=1995, month=1, day=1), datetime(year=2023, month=1, day=1))
# plt.xlim(datetime(year=2010, month=1, day=1), datetime(year=2023, month=1, day=1))
# plt.xlim(datetime(year=2018, month=9, day=1), datetime(year=2023, month=1, day=1))

if args.spent:
    ax2 = ax.twinx()
    ax2.plot(dats + [today], manyr_sums, "--y", lw=4,
             label=msgs["ttime"])
    ax2.set_ylim(0, manyr_sums[-1] + 2.2)
    ax2.set_ylabel(f'{msgs["ttimelbl"]}, {msgs["manyr"]}', fontsize=14)
ax.set_facecolor("none")
ax.set_zorder(1)
YSHIFT = 0.35
YLIM = 20 + YSHIFT
ax.set_ylim(0, YLIM)
ax.set_xlabel(msgs["xlbl"], fontsize=14)
ax.set_ylabel(msgs["ylbl3"], fontsize=14)

TM = timedelta(weeks=48)
TM_SHIFT = timedelta(weeks=12)
SH, SH2 = 0.2 + YSHIFT, 1.9 + YSHIFT
accidents = [
    # (1960, 10, 24, 'Катастрофа на космодроме Байконур, МБР Р-16', SH, TM),
    (1961, 3, 23, msgs["fb"], SH2, -TM_SHIFT),
    (1967, 1, 27, msgs["fa"], SH2, TM),
    (1967, 4, 23, msgs["dk"], SH2, -TM_SHIFT * 2.9),
    (1967, 11, 15, msgs["da"], SH2, -TM_SHIFT * 2.9 - TM_SHIFT),
    (1971, 6, 30, msgs["deprs"], SH2, TM),
    (1980, 3, 18, msgs["pledis"], SH2, TM),
    (1986, 1, 28, msgs["chdis"], SH, TM),
    (2003, 2, 1, msgs["codis"], SH, TM),
]

private_spaceflights = [
    (2001, 4, 28, msgs["titosz"], SH, TM),
    (2020, 5, 30, "SpaceX DM-2", SH, TM),
    (2021, 7, 11, "VG Unity 22/NS-16", SH, TM),
    (2021, 7, 20, "", SH, TM),
    (2021, 9, 16, "Inspirati④n", SH, -TM_SHIFT),
]

if args.accidents:
    for ac in accidents:
        dat = datetime(year=ac[0], month=ac[1], day=ac[2])
        ax.plot((dat, dat), (0, YLIM), "--r")
        ax.text(dat - ac[5], YLIM - ac[4], ac[3], rotation="vertical", va="top", fontsize=14)
if args.private:
    for ac in private_spaceflights:
        dat = datetime(year=ac[0], month=ac[1], day=ac[2])
        ax.plot((dat, dat), (0, YLIM), "--g")
        ax.text(dat - ac[5], YLIM - ac[4], ac[3], rotation="vertical", va="top", fontsize=14)

if args.spent:
    handles, labels = unite_legends([ax, ax2])
    ax.legend(handles, labels, loc="upper left", fontsize=12)
else:
    plt.legend(fontsize=12)

ax.grid(linestyle="dotted", axis="y")
plt.title(
    f'{msgs["census"]}, {len(nums)} {msgs["changes"]}. {msgs["peopspent"]} '
    + f'{round(manyr_sums[-1], 1)} {msgs["manyr"]}. {MONTH} {YEAR} {msgs["yr"]}'
)

METHD = "stairs" if args.method else "steps"
FILENAME = f"spacepop-{'spent-' if args.spent else ''}{METHD}{'-filled' if args.filled else ''}"

LOC = "-ru" if args.translate else ""
FILE_EXT = "png"
plots_dir = os.path.join(os.pardir, os.pardir, os.pardir, "plots", "manned")
tmp_pth = os.path.join(plots_dir, f"{FILENAME}{LOC}_.{FILE_EXT}")
pth = os.path.join(plots_dir, f"{FILENAME}{LOC}.{FILE_EXT}")
plt.savefig(tmp_pth, dpi=120)

if FILE_EXT == "svg":
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)

JSON_FILENAME = "../../../data/space_population.json"
CSV_FILENAME = "../../../data/space_population.csv"
data_json = json.dumps(datac, indent=0, separators=(",", ": "),
                       cls=CompactJSONEncoder, ensure_ascii=False).splitlines()
data_json = '\n'.join([data_json[0], textwrap.dedent('\n'.join(data_json[1:-1])), data_json[-1]])
with open(JSON_FILENAME, "w", encoding="utf8") as json_file:
    json_file.write(data_json)

with open(CSV_FILENAME, 'w', newline='') as f:
    header = ["date", "MJD", "spacepop", "orbitpop", "recspacepop", "recorbitpop"]
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(datac)
