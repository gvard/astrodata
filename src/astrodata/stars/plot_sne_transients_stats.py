"""Python script for genererating charts with supernovae and transient statistics.
Data sources:
David Bishop, Latest Supernovae Archives
https://www.rochesterastronomy.org/snimages/archives.html
Transient Name Server
https://www.wis-tns.org/stats-maps
Central Bureau for Astronomical Telegrams List of SNe
http://www.cbat.eps.harvard.edu/lists/Supernovae.html
"""

import os
from datetime import datetime, timedelta
import locale
import argparse
import json
import textwrap
from decimal import Decimal

from scour import scour
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import pandas as pd

from transients import (
    add_iau_sne,
    get_soup_request,
    get_sn_stats,
    get_sn_count,
    get_tns_stats,
    get_tns_year_stats,
    mk_sne_iau_lst,
    mk_transient_total_numbers,
    mk_tns_data,
    mk_urls_lst,
    today,
)


def optimize_svg(tmp_path, path):
    """Optimize svg file using scour"""
    with open(tmp_path, "rb") as inputfile, open(path, "wb") as outputfile:
        options = scour.generateDefaultOptions()
        options.enable_viewboxing = True
        options.strip_comments = True
        options.strip_ids = True
        options.remove_metadata = True
        options.shorten_ids = True
        options.indent_type = "none"
        options.newlines = False
        scour.start(options, inputfile, outputfile)


class CompactJSONEncoder(json.JSONEncoder):
    """A JSON Encoder that puts small containers on single lines.
    https://gist.github.com/jannismain/e96666ca4f059c3e5bc28abb711b5c92
    """

    CONTAINER_TYPES = (list, tuple, dict)
    """Container datatypes include primitives or other containers."""

    MAX_WIDTH = 1240
    """Maximum width of a container that might be put on a single line."""

    MAX_ITEMS = 200
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
        return "[\n" + ",".join(output) + "\n" + self.indent_str + "]"

    def _encode_object(self, o):
        if not o:
            return "{}"
        if self._put_on_single_line(o):
            return (
                "{" + ", ".join(
                    f"{self.encode(k)}: {self.encode(el)}" for k, el in o.items()
                ) + "}"
            )
        self.indentation_level += 1
        output = [
            f"{self.indent_str}{json.dumps(k)}: {self.encode(v)}" for k, v in o.items()
        ]

        self.indentation_level -= 1
        if output[0].startswith('"202'):
            return "{" + ",\n".join(output) + "}"
        return "{" + ", ".join(output) + self.indent_str + "}"

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


parser = argparse.ArgumentParser(description="Graph plotter script with number of transients")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="Print additional information")
parser.add_argument("-y", "--startyear", type=int, default=2004,
                    help="Set year to start. Default is 2004")
parser.add_argument("-t", "--translate", action="store_true",
                    help="translate all inscriptions into Russian")
args = parser.parse_args()

DPI = 120
LOC = "en_US"
if args.translate:
    LOC = "ru_RU"
locale.setlocale(locale.LC_ALL, LOC)
YEAR, MONTH, DAY = today.year, today.strftime("%B"), today.strftime("%d")
MONTH2 = today.strftime("%m")
COLORS = plt.rcParams["axes.prop_cycle"].by_key()["color"]
COLORS = [COLORS[3], COLORS[0], COLORS[1]]
STARS_DIR = os.path.join(os.pardir, os.pardir, os.pardir, "plots", "stars")

stat_cat_pub, stat_cat_all = get_tns_stats()
nums_pub, yrs_ints, realdates, stats_pub_dct, tns_pub_final_dct = get_tns_year_stats(stat_cat_pub)
nums_all, yrs_ints, realdates, stats_all_dct, tns_all_final_dct = get_tns_year_stats(stat_cat_all)
sne_final_dct = add_iau_sne(tns_pub_final_dct)
total_dct = dict(sorted(sne_final_dct.items()))
total_lst = mk_transient_total_numbers(total_dct)
SNE_IAU_LST = mk_sne_iau_lst(args.startyear, YEAR)
data_to_plot_dct, nums_diff_dct = mk_tns_data(
    stats_pub_dct, stats_all_dct, start_year=args.startyear
)
ALL_TNS = sum(data_to_plot_dct.values())

FILE_EXT = "png"
LOC = "-ru" if args.translate else ""
TMP_FILENAME = f"transient_stats_bar_chart{LOC}_.{FILE_EXT}"
FILENAME = f"transient_stats_bar_chart{LOC}.{FILE_EXT}"
tmp_pth = os.path.join(STARS_DIR, TMP_FILENAME)
pth = os.path.join(STARS_DIR, FILENAME)
labels = list(data_to_plot_dct.keys())
labels[0] = f"до {args.startyear}"
title = f"Статистика транзиентов по годам, всего {ALL_TNS} публичных транзиентов"
XLABEL = "Годы"
YLABEL = "Транзиентов за год"

if args.verbose:
    tns_before_startyear = SNE_IAU_LST[0] + data_to_plot_dct[args.startyear - 1]
    print(labels[0]
          + f" года {SNE_IAU_LST[0]} сверхновых в CBAT, "
          + f"{data_to_plot_dct[args.startyear-1]} на TNS, всего {tns_before_startyear}")

data = {
    "Сверхновые CBAT": SNE_IAU_LST,
    "Публичные транзиенты": data_to_plot_dct.values(),
    "Транзиенты не в публичном доступе": nums_diff_dct.values(),
}
df = pd.DataFrame(data, index=labels)

ax = df.plot(kind="bar", stacked=True, figsize=(16, 9), color=COLORS, width=0.85, rot=0)
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.97, top=0.955)
plt.xlabel(XLABEL, fontsize=14)
plt.ylabel(YLABEL, fontsize=14)
plt.title(title + f". {MONTH} {YEAR} года", fontsize=16)
plt.legend(fontsize=14, loc="upper left")
ax.yaxis.set_minor_locator(MultipleLocator(1000))
for x, y in enumerate(df.sum(axis=1)):
    ax.annotate(int(y), (x, y + 190), ha="center")

plt.savefig(tmp_pth, dpi=DPI)
if FILE_EXT == "svg":
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)

if args.verbose:
    print("Collect data from Latest Supernovae Archives by David Bishop")

snstats = {}
years, sns, snalt, all_sne = [], [], [], []
years_dt = []
all_sn_count, sn_amateur_count = 0, 0
snyears_urls = mk_urls_lst()
KEY = "-".join((str(YEAR), MONTH2, DAY))
sne_stats_dct = {KEY: {}}

for i, (year, snstats_url) in enumerate(snyears_urls):
    soup = get_soup_request(snstats_url)
    snstats[year], lastmod = get_sn_stats(soup)
    sn_num, sn_cbat, sn_amateur, sn_13th = get_sn_count(snstats[year])
    all_sn_count += sn_num
    sn_amateur_count += sn_amateur
    if year == 1995:
        all_sne.append(all_sn_count)
        sne_stats_dct[KEY]["1995"] = (
            sn_num, sne_final_dct[datetime(year + 1, 1, 1)],
            sn_amateur, sn_13th, lastmod,
        )
        print(
            f"До 1996г: {sn_num} сверхновых, {sne_final_dct[datetime(year+1, 1, 1)]}"
            + f" транзиентов, {sn_amateur} открыто любителями, {sn_13th} "
            + f"ярче 13 зв. вел на {lastmod}"
        )
        years.append(year)
        years_dt.append(datetime(year + 1, 1, 1))
        sns.append(sn_num - sn_amateur)
        snalt.append(sn_amateur)
    elif year != "all":
        all_sne.append(all_sn_count)
        if year == YEAR:
            tr_num = sne_final_dct.get(today)
            years_dt.append(today)
        else:
            tr_num = sne_final_dct.get(datetime(year + 1, 1, 1))
            years_dt.append(datetime(year + 1, 1, 1))
        sne_stats_dct[KEY][str(year)] = (sn_num, tr_num, sn_amateur, sn_13th, lastmod)
        print(
            f"{year} год: {sn_num} сверхновых, {tr_num} транзиентов, {sn_amateur}"
            + f" открыто любителями, {sn_13th} ярче 13 зв. вел. Всего к концу года: "
            + f"{all_sn_count}, {total_lst[i]} транзиентов, {sn_amateur_count} "
            + f"любителями на {lastmod}"
        )
        years.append(year)
        sns.append(sn_num - sn_amateur)
        snalt.append(sn_amateur)
    else:
        print(
            f"Всего {sn_num}, а в сумме {all_sne[-1]} СН, {sn_amateur} открыто любителями,"
            + f" {sn_13th} ярче 13 зв. величины на дату {lastmod}"
        )

FILE_EXT = "png"
TMP_FILENAME = f"sne_stats_bar_chart{LOC}_.{FILE_EXT}"
FILENAME = f"sne_stats_bar_chart{LOC}.{FILE_EXT}"
tmp_pth = os.path.join(STARS_DIR, TMP_FILENAME)
pth = os.path.join(STARS_DIR, FILENAME)

years[0] = f"до {min(1996, args.startyear)}"
data = {
    "Сверхновые Latest Supernovae Archives": sns,
    "Сверхновые, обнаруженные любителями": snalt,
}
df = pd.DataFrame(data, index=years)

ax = df.plot(kind="bar", stacked=True, figsize=(16, 9), width=0.85, rot=0)
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.97, top=0.955)
plt.xlabel("Годы", fontsize=14)
plt.ylabel("Открытий сверхновых за год", fontsize=14)
title = f"Статистика открытий сверхновых по годам, всего {all_sne[-1]} сверхновых."
plt.title(title + f" {MONTH} {YEAR} года", fontsize=16)
plt.legend(fontsize=14, loc="upper left")
ax.yaxis.set_minor_locator(MultipleLocator(500))
ax.bar_label(ax.containers[-1])

plt.savefig(tmp_pth, dpi=DPI)
if FILE_EXT == "svg":
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)


FILE_EXT = "png"
TOTAL_SNE_FILENAME = f"sne_transients_total_number_log_plot{LOC}.{FILE_EXT}"
pth = os.path.join(STARS_DIR, TOTAL_SNE_FILENAME)
TMP_FILENAME = f"sne_transients_total_number_log_plot{LOC}_.{FILE_EXT}"
tmp_pth = os.path.join(STARS_DIR, TMP_FILENAME)

fig, ax = plt.subplots(figsize=(16, 9))
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.97, top=0.955)
ax.xaxis.set_major_locator(mdates.YearLocator(1))

plt.plot(years_dt, all_sne, "ok-", label="David Bishop, Latest Supernovae Archives")
plt.plot(total_dct.keys(), total_lst, "or-",
         label="Transient Name Server, public + CBAT SNe before 2016")
plt.xlim(datetime(1995, 10, 1), today + timedelta(weeks=31.9))
plt.ylim(1000, 150000)
plt.yscale("log")
plt.legend(fontsize=14)
plt.title(
    f"Динамика вспышек сверхновых, всего {all_sne[-1]} сверхновых и {total_lst[-1]} "
    + f"транзиентов. {MONTH} {YEAR} года", fontsize=16,
)
plt.xlabel("Время", fontsize=14)
plt.ylabel("Количество открытых сверхновых", fontsize=14)
plt.grid(axis="y", which="major", linestyle="-")
plt.grid(axis="x", which="major", linestyle=":")
plt.grid(axis="y", which="minor", linestyle="--")
plt.savefig(tmp_pth, dpi=DPI)
if FILE_EXT == "svg":
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)

JSON_FILENAME = "../../../data/stars/sne-stats.json"

with open(JSON_FILENAME) as json_file:
    data_from_json = json.load(json_file)

data_from_json.update(sne_stats_dct)

data_json = json.dumps(data_from_json, indent=0, separators=(",", ": "),
                       cls=CompactJSONEncoder, ensure_ascii=False).splitlines()

data_json = '\n'.join([data_json[0],
                       textwrap.dedent('\n'.join(data_json[1:-1])),
                       data_json[-1]]) + "\n"
with open(JSON_FILENAME, "w", encoding="utf8") as json_file:
    json_file.write(data_json)
