"""Python script for plotting charts with localized GRBs statistics.
Data source: Jochen Greiner,
Gamma-ray bursts localized within a few hours to days to less than 1 degree
https://www.mpe.mpg.de/~jcg/grbgen.html
"""

import os
from datetime import datetime
import locale
import argparse
import json

from scour import scour
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import pandas as pd

from transients import get_soup_request


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


def get_grbs_tables(soup):
    """Get GRBs stats from all data and summary tables."""
    _all_tabs = soup.findAll("table")
    trs_all = _all_tabs[0].findAll("tr")
    trs_summary = _all_tabs[-1].findAll("tr")
    return trs_all, trs_summary


def get_summary_grbs_stats(trs):
    """Get GRBs stats from raws of summary table."""
    years, gnums, opts = [], [], []
    for tr in trs[1:-1]:
        tds = tr.findAll("td")
        opt = int(tds[3].text)
        years.append(int(tds[0].text))
        gnums.append(int(tds[1].text) - opt)
        opts.append(opt)
    return years, gnums, opts


def parse_table(trs):
    """Get GRBs stats from rows of big data table"""
    nums, ot_num, xa_num, ra_num, rs_num = 0, 0, 0, 0, 0
    grb_dates, grbnums, otnums, xanums, ranums, rss = [], [], [], [], [], []
    years_dct, opts_dct, ra_dct, xa_dct, rs_dct = {}, {}, {}, {}, {}
    if args.verbose:
        print("Start parsing table with GRBs stats")
    for tr in trs[1:]:
        tds = tr.findAll("td")
        grbname = tds[0].a.text
        xray_ag = tds[5].text
        opt_ag = tds[6].text
        rad_ag = tds[7].text
        redshift = tds[9].text
        year = grbname[:2]
        if year[0] in ("2", "1", "0"):
            year = int("20" + year)
        elif year[0] == "9":
            year = int("19" + year)
        if redshift.strip():
            rs_num += 1
            try:
                rs_dct[year] += 1
            except KeyError:
                rs_dct[year] = 1
        if xray_ag and xray_ag[0] == "y":
            xa_num += 1
            try:
                xa_dct[year] += 1
            except KeyError:
                xa_dct[year] = 1
        if rad_ag and rad_ag[0] == "y":
            ra_num += 1
            try:
                ra_dct[year] += 1
            except KeyError:
                ra_dct[year] = 1
        grb_date = datetime(year, int(grbname[2:4]), int(grbname[4:6]))
        if opt_ag and opt_ag.strip() in ("y", "SN"):  # with or without "y?"
            ot_num += 1
            try:
                opts_dct[year] += 1
            except KeyError:
                opts_dct[year] = 1
        try:
            years_dct[year] += 1
        except KeyError:
            years_dct[year] = 1
        grb_dates.append(grb_date)
        nums += 1
        grbnums.append(nums)
        otnums.append(ot_num)
        xanums.append(xa_num)
        ranums.append(ra_num)
        rss.append(rs_num)
    return (grb_dates, grbnums, otnums, xanums, ranums, rss, years_dct,
            opts_dct, ra_dct, xa_dct, rs_dct)


parser = argparse.ArgumentParser(
    description="Graph plotter script with number of gamma-ray bursts")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="Print additional information")
parser.add_argument("-s", "--savedata", action="store_true",
                    help="Save data to JSON file")
parser.add_argument("-t", "--translate", action="store_true",
                    help="translate all inscriptions into Russian")
args = parser.parse_args()

soup = get_soup_request("https://www.mpe.mpg.de/~jcg/grbgen.html", "lxml")
if args.verbose:
    print("get GRBs stats tables")
trs_all, trs_summary = get_grbs_tables(soup)
if args.verbose:
    print("get data from GRBs stats summary table")
years_s, gnums_s, opts_s = get_summary_grbs_stats(trs_summary)
(
    years, grbnums, otnums, xanums, ranums, rss, years_dct, opts_dct, ra_dct,
    xa_dct, rs_dct
) = parse_table(trs_all)

DPI = 120
LOC = "en_US"
if args.translate:
    LOC = "ru_RU"
with open(f"../locales/grbs-{LOC[:2]}.json", "r", encoding="utf8") as loc_file:
    msgs = json.load(loc_file)
locale.setlocale(locale.LC_ALL, LOC)
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year
PLOTS_DIR = os.path.join(os.pardir, os.pardir, os.pardir, "plots", "stars")
FILE_EXT = "png"
TOTAL_GRBS_FILENAME = f"grbs_total_number_plot-{LOC[:2]}"
pth = os.path.join(PLOTS_DIR, f"{TOTAL_GRBS_FILENAME}.{FILE_EXT}")
tmp_pth = os.path.join(PLOTS_DIR, f"{TOTAL_GRBS_FILENAME}_.{FILE_EXT}")

fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)  # left=0.06, bottom=0.06, right=0.97, top=0.955
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.yaxis.set_minor_locator(MultipleLocator(250))

years = years[::-1]
MS = 2
plt.plot(years, grbnums, "ok-", ms=MS + 2,
         label=f"{msgs['lgrbs']}: {len(grbnums)} {msgs['event'][0]}")
plt.plot(years, xanums, "o-", ms=MS, color="indigo",
         label=f"{msgs['xrag']}: {xanums[-1]} {msgs['event'][1]}")
plt.plot(years, otnums, "og-", ms=MS + 1,
         label=f"{msgs['optag']}: {otnums[-1]} {msgs['event'][1]}")
plt.plot(years, rss, "o-", ms=MS, color="red",
         label=f"{msgs['rs']}: {rss[-1]} {msgs['event'][0]}")
plt.plot(years, ranums, "o-", ms=MS, color="navy",
         label=f"{msgs['raag']}: {ranums[-1]} {msgs['event'][1]}")

plt.xlim(datetime(1996, 1, 1), datetime(2023, 12, 1))
plt.ylim(-15, 2500)
TITLE = msgs["title"]
plt.title(f"{TITLE}. {MONTH} {YEAR} {msgs['yr']}", fontsize=15)
plt.xlabel(msgs["xlbl"], fontsize=14)
plt.ylabel(msgs["ylbl"], fontsize=14)
plt.grid(axis="y", which="major", linestyle="--")
plt.grid(axis="x", which="major", linestyle=":")
plt.grid(axis="y", which="minor", linestyle=":")
plt.legend(fontsize=14, loc="upper left")

plt.savefig(tmp_pth, dpi=DPI)
if FILE_EXT == "svg":
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)

if args.verbose:
    print("Plot stacked bar chart with numbers of optical afterglows")

grbnums = list(years_dct.values())[::-1]
years_to_plot = list(years_dct.keys())[::-1]
all_grbs = sum(grbnums)

result_dct = {}
grbnums_noopt = []
all_grb_count, xa_count, opt_count, ra_count, rs_count = 0, 0, 0, 0, 0
for i, year in enumerate(years_to_plot):
    all_grb_count += grbnums[i]
    if year in xa_dct:
        xa_count += xa_dct[year]
    else:
        xa_dct[year] = 0
    if year in opts_dct:
        opt_count += opts_dct[year]
    else:
        opts_dct[year] = 0
    if year in ra_dct:
        ra_count += ra_dct[year]
    else:
        ra_dct[year] = 0
    if year in rs_dct:
        rs_count += rs_dct[year]
    else:
        rs_dct[year] = 0
    if args.verbose:
        print(
            f"{year}: {grbnums[i]:3d} localized GRBs, {xa_dct[year]:3d} "
            f"X-ray afterglows, {opts_dct[year]:2d} optical AGs, "
            f"{ra_dct[year]:2d} radio AGs, {rs_dct[year]:2d} redshifts. Total "
            f"by the end of the year {all_grb_count} GRBs, {opt_count} optical AGs"
        )
    result_dct[year] = (grbnums[i], xa_dct[year], opts_dct[year], ra_dct[year],
                        rs_dct[year])
    grbnums_noopt.append(grbnums[i] - opts_dct[year])

opts = list(opts_dct.values())[::-1]

FILE_EXT = "png"
TMP_FILENAME = f"grbs_stats_bar_chart-{LOC[:2]}_.{FILE_EXT}"
FILENAME = f"grbs_stats_bar_chart-{LOC[:2]}.{FILE_EXT}"
tmp_pth = os.path.join(PLOTS_DIR, TMP_FILENAME)
pth = os.path.join(PLOTS_DIR, FILENAME)

df = pd.DataFrame(
    {
        f"{msgs['lgrbs']} {msgs['ag'][0]}": grbnums_noopt,
        f"{msgs['grbs'][0]} {msgs['ag'][1]}": opts,
    }, index=years_to_plot)

ax = df.plot(kind="bar", stacked=True, figsize=(16, 9), width=0.85, rot=0)
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.97, top=0.955)  # 0.048, 0.06, 0.99, 0.97
plt.xlabel(msgs["xlbl"], fontsize=14)
plt.ylabel(msgs["ylbl2"], fontsize=14)
plt.title(f"{TITLE}. {msgs['total']}{all_grbs} {msgs['event'][0]}, {opt_count} "
          + f"{msgs['ag'][2]}. {MONTH} {YEAR} {msgs['yr']}", fontsize=14)
plt.legend(fontsize=14, loc="upper left")
ax.yaxis.set_minor_locator(MultipleLocator(5))
for x, y in enumerate(df.sum(axis=1)):
    ax.annotate(int(y), (x, y+1), ha="center")
# ax.bar_label(ax.containers[-1])

plt.savefig(tmp_pth, dpi=DPI)
if FILE_EXT == "svg":
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)

if args.savedata:
    JSON_FILENAME = "../../../data/stars/grbs-localized-stats.json"
    with open(JSON_FILENAME, "w", encoding="utf8") as json_file:
        json.dump(result_dct, json_file, indent=None,
                  separators=(",", ": "), ensure_ascii=False)
