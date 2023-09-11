"""Python script for plotting graph with rocket launches statistics.
Data taken from General Catalog of Artificial Space Objects
by Jonathan C. McDowell: https://planet4589.org/space/gcat/web/launch/
Event Catalogs, Deep Space Catalog: https://planet4589.org/space/gcat/web/cat/
Data products: plots with orbital, failed, marginal, suborbital
and deep space launches.
Plots may include parameter approximation and predictions.
Example parameter usage: -vlofmdr option set gives a graph with the Deep space,
Orbital, Failed, Marginal launches numbers, with lineaR approximations
and prediction to a given year number.
Also with Verbose output and Local data files.
"""

from datetime import datetime, timedelta
import os
import locale
import urllib.request
from argparse import ArgumentParser
import json

import pandas
import seaborn
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import datestr2num, date2num
from scour import scour


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


def get_table(url, local=False):
    """Read ASCII data table from pre html element"""
    if local:
        html = open(url, encoding="utf-8")
    else:
        html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    return soup.findAll("pre")[1].text.splitlines()


def get_data_array(data, date_col=(26, 41)):
    """Parse ASCII data of launch lists.
    TODO: merge with parser for suborbital list.
    """
    dates, nums = [], []
    launches_num = 0
    no_altitude = 0
    for line in data:
        apo = line[236:244].strip()
        try:
            apo = int(apo)
        except ValueError:
            no_altitude += 1
        if line:
            try:
                dat = datetime.strptime(
                    line[date_col[0]:date_col[1]], f"{STRPFRM} %H%M"
                )
            except ValueError:
                dat = datetime.strptime(line[date_col[0]:date_col[1] - 4], STRPFRM)
            dates.append(dat)
            launches_num += 1
            nums.append(launches_num)
    print("No apogee altitude data for", no_altitude, "entries")
    return dates, nums


def get_data_array_deep(data, date_col=(106, 117), sort=True):
    """Parse ASCII data of launch lists.
    TODO: merge with parser for suborbital list.
    """
    dates = []
    nnas = 0
    for line in data:
        satcat = line[13:18].strip()
        if satcat.startswith("NNA"):
            nnas += 1
            # continue
        if line:
            name = line[48:76].strip()
            ldate = datetime.strptime(line[date_col[0]:date_col[1]], STRPFRM)
            dates.append([ldate, name, satcat])
    print("No satellite cat entry for", nnas, "deepcat entries")
    if sort:
        dates.sort(key=lambda row: row[0])
    return dates


def predict_linear_trend(xes, ykas, dat):
    """Get the slope and intercept of the regression line, then
    calculate x and y values for a given date."""
    slope, intercept = np.polyfit(xes, ykas, 1)
    x = date2num(dat)
    return x, round(slope * x + intercept)


def mk_dataframe(dates, nums, frm=1964, to=None):
    """Make dataframe from dates and numbers limited by given year numbers."""
    df = pandas.DataFrame({
        "date": pandas.to_datetime(dates),  # pandas dates
        "datenum": datestr2num([day.strftime(STRFFRM) for day in dates]),
        "value": nums,
    })
    if to:
        df = df[(df["date"].dt.year > frm) & (df["date"].dt.year < to)]
    else:
        df = df[df["date"].dt.year > frm]
    return df


parser = ArgumentParser(description="Graph plotter script with number of rocket launches")
parser.add_argument("-v", "--verbose", action="store_true",
    help="Print additional information")
parser.add_argument("-d", "--deep", action="store_true",
    help="Plot launches to deep space")
parser.add_argument("-a", "--savelist", action="store_true",
    help="Save list of deep space launches to file")
parser.add_argument("-o", "--orbital", action="store_true",
    help="Plot number of suborbital launches")
parser.add_argument("-f", "--failed", action="store_true",
    help="Plot number of failed launches")
parser.add_argument("-m", "--marginal", action="store_true",
    help="Plot number of marginal launches")
parser.add_argument("-s", "--suborb", action="store_true",
    help="Plot number of suborbital launches")
parser.add_argument("-l", "--local", action="store_true",
    help="Use local files")
parser.add_argument("-e", "--height", type=int, default=100,
    help="Set apogee height in km for suborbital launches. Default is 100 km")
parser.add_argument("-r", "--regressfit", action="store_true",
    help="Plot regression fit using Seaborn")

args = parser.parse_args()


LOC = "en_US"  # "ru_RU"
with open(f"../locales/launches-{LOC[:2]}.json", "r", encoding="utf8") as loc_file:
    msgs = json.load(loc_file)

DATA_URL_TEMPL = "../../../data/{}.html"
BASE_URL = "https://planet4589.org/space/gcat/data/"
LISTS_DIR = "ldes/"
MS = 3
STRPFRM = "%Y %b %d"
STRFFRM = "%Y-%m-%d"

PREDIDATE = datetime(year=2026, month=1, day=1)
YR_APPROX = 1999

nums, nums_fail, nums_marg, nums_deep, so_nums = [], [], [], [], []
if args.orbital:
    DATA_URL = BASE_URL + LISTS_DIR + "O.html"
    if args.local:
        DATA_URL = DATA_URL_TEMPL.format("O")
    data = get_table(DATA_URL, local=args.local)[1:]
    dates, nums = get_data_array(data)
    print("Orbital launches:", len(dates))
    orb_df = mk_dataframe(dates, nums, frm=YR_APPROX)
if args.failed:
    DATA_URL = BASE_URL + LISTS_DIR + "F.html"
    if args.local:
        DATA_URL = DATA_URL_TEMPL.format("F")
    data = get_table(DATA_URL, local=args.local)[1:]
    dates_fail, nums_fail = get_data_array(data)
    print("Launches failed:", len(dates_fail))
    fail_df = mk_dataframe(dates_fail, nums_fail, frm=1975, to=2020)
if args.marginal:
    DATA_URL = BASE_URL + LISTS_DIR + "U.html"
    if args.local:
        DATA_URL = DATA_URL_TEMPL.format("U")
    data = get_table(DATA_URL, local=args.local)[1:]
    dates_marg, nums_marg = get_data_array(data)
    print("Marginal launches:", len(dates_marg))
if args.suborb:
    if args.verbose:
        print("Plot suborb graph")
    FILE_EXT = "png"
    MS = 5
    DATA_URL = BASE_URL + LISTS_DIR + "S.html"
    if args.local:
        DATA_URL = DATA_URL_TEMPL.format("S")
    suborb_data = get_table(DATA_URL, local=args.local)[1:]
    so_dates, so_nums, so_heights = [], [], []
    so_launches_num = 0
    no_altitude = 0
    qm = 0
    for line in suborb_data:
        apo = line[239:244].strip()
        question_mark = line[244].strip()
        if question_mark == "?":
            qm += 1
        try:
            apo = int(apo)
        except ValueError:
            no_altitude += 1
            continue
        if line and line[35:37].strip() and apo and int(apo) >= args.height:
            if line[37] == "?" or line[38] == " ":
                dat = datetime.strptime(line[26:37], STRPFRM)
            else:
                dat = datetime.strptime(line[26:42], f"{STRPFRM} %H%M")
            so_heights.append(apo)
            so_dates.append(dat)
            so_launches_num += 1
            so_nums.append(so_launches_num)
    suborb_df = mk_dataframe(so_dates, so_nums, frm=YR_APPROX)
    print(f"No apogee altitude data for {no_altitude} entries, {qm} questioned")
    print("Suborbital launches:", len(so_dates))

if args.deep:
    FILE_EXT = "png"
    DATA_URL = BASE_URL + "cat/deepcat.html"
    # if args.local:
    #     DATA_URL = "../../../data/deepcat.html"
    # datt = get_table(DATA_URL, local=args.local)[1:]
    datt = get_table(DATA_URL)[1:]
    dates_deep = get_data_array_deep(datt)
    dates_only, names, nums_only = [], [], []
    unique_dtes = {}

    for data, name, satnum in dates_deep:
        if data not in unique_dtes:
            unique_dtes[data] = [name]
        else:
            unique_dtes[data].append(name)
        dates_only.append(data)
        names.append(name)
        nums_only.append(satnum)

    if args.savelist:
        DEEP_FILENAME = "deepcat.txt"
        with open(DEEP_FILENAME, "w", encoding="utf-8") as f:
            for dat, space_objects_lst in unique_dtes.items():
                print(str(dat.date()), space_objects_lst, file=f)
        print("Deep space launches list saved to", DEEP_FILENAME)

    dates_deep = list(unique_dtes.keys())
    nums_deep = range(1, len(dates_deep) + 1)
    deep_df = mk_dataframe(dates_deep, nums_deep, frm=1963, to=1974)
    deep2_df = mk_dataframe(dates_deep, nums_deep, frm=2000, to=2023)
    print("Deep space objects:", len(dates_deep))

fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)
years = mdates.YearLocator(5)
oneyear = mdates.YearLocator()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(oneyear)
tdlt = timedelta(days=630)
locale.setlocale(locale.LC_ALL, LOC)
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year

TITLE = msgs["title"]
if args.suborb:
    plt.plot(
        so_dates, so_nums, ".k", ms=5,
        label=f"{msgs['so'][0]} {args.height} {msgs['km']})",
    )
    plt.ylim(
        -35 if args.height < 86 else -21,
        so_nums[-1] + 1500 if args.height < 86 else so_nums[-1] + 936,
    )
    TITLE = msgs["title"]
    if args.regressfit:
        seaborn.regplot(
            data=suborb_df, x="datenum", y="value", ax=ax,
            truncate=False, color="darkgrey", line_kws={"linestyle": "--"},
        )
        x, y = predict_linear_trend(suborb_df["datenum"], suborb_df["value"], PREDIDATE)
        if args.verbose:
            print(f"Suborbital: prediction for {PREDIDATE} is {y}")
        plt.plot(x, y, "or", ms=5)
        plt.annotate(f"{round(y)}", xy=(x, y + 220), fontsize=12, ha="center")
if args.orbital:
    plt.plot(dates, nums, ".b", label=msgs["orb"][0], ms=MS)
    if args.regressfit:
        seaborn.regplot(
            data=orb_df, x="datenum", y="value", ax=ax,
            truncate=False, color="darkgrey", line_kws={"linestyle": "--"},
        )
        x, y = predict_linear_trend(orb_df["datenum"], orb_df["value"], PREDIDATE)
        if args.verbose:
            print(f"Orbital: prediction for {PREDIDATE} is {y}")
        plt.plot(x, y, "or", ms=5)
        plt.annotate(f"{round(y)}", xy=(x, y + 220), fontsize=13, ha="center")
if args.failed:
    plt.plot(dates_fail, nums_fail, ".r", label=msgs["fail"][0], ms=MS)
    if args.regressfit:
        seaborn.regplot(
            data=fail_df, x="datenum", y="value", ax=ax,
            truncate=False, color="darkgrey", line_kws={"linestyle": "--"},
        )
        x, y = predict_linear_trend(fail_df["datenum"], fail_df["value"], PREDIDATE)
        if args.verbose:
            print(f"Failed: prediction for {PREDIDATE} is {y}")
        plt.plot(x, y, "or", ms=5)
        plt.annotate(f"{round(y)}", xy=(x, y + 5.5), fontsize=13, ha="center")
if args.deep:
    plt.plot(dates_deep, nums_deep, ".k", label=msgs["deep"][0], ms=6)
    plt.ylim(-5, nums_deep[-1] + 190)
    if args.regressfit:
        seaborn.regplot(
            data=deep_df, x="datenum", y="value", ax=ax,
            truncate=False, color="darkgrey", line_kws={"linestyle": "--"},
        )
        x, y = predict_linear_trend(deep_df["datenum"], deep_df["value"], PREDIDATE)
        if args.verbose:
            print(f"Deep space launches: prediction for {PREDIDATE} is {y}")
        plt.plot(x, y, "or", ms=5)
        plt.annotate(f"{round(y)}", xy=(x, y + 5.5), fontsize=13, ha="center")

        seaborn.regplot(
            data=deep2_df, x="datenum", y="value", ax=ax,
            truncate=False, color="darkgrey", line_kws={"linestyle": "--"},
        )
        x, y = predict_linear_trend(deep2_df["datenum"], deep2_df["value"], PREDIDATE)
        if args.verbose:
            print(f"Deep space launches: prediction for {PREDIDATE} is {y}")
        plt.plot(x, y, "or", ms=5)
        plt.annotate(f"{round(y)}", xy=(x, y + 5.5), fontsize=13, ha="center")

if args.marginal:
    plt.plot(dates_marg, nums_marg, ".g", label=msgs["marg"][0], ms=MS)  # ms=2

ORB_TITL = f"{len(nums)} {msgs['orb'][1]}, " if nums else ""
FAILD_TITL = f"{len(nums_fail)} {msgs['fail'][1]}, " if nums_fail else ""
MARG_TITL = f"{len(nums_marg)} {msgs['marg'][1]}, " if nums_marg else ""
DEEP_TITL = f"{len(nums_deep)} {msgs['deep'][1]}" if nums_deep else ""
SUBORB_TITL = f"{len(so_nums)} {msgs['so'][1]}" if so_nums else ""
YR = msgs["yr"]

xlim = (
    (dates[0] - tdlt, dates[-1] + 2 * tdlt)
    if args.deep and args.orbital
    else (datetime(1942, 8, 5), so_dates[-1] + 2.6 * tdlt)
)
plt.xlim(xlim)
plt.title(
    f"{TITLE}{ORB_TITL}{FAILD_TITL}{MARG_TITL}{DEEP_TITL}{SUBORB_TITL}. {MONTH} {YEAR} {YR}"
)
plt.legend(loc="upper left", fontsize=13)
plt.xlabel(msgs["xlbl"], fontsize=14)
plt.ylabel(msgs["ylbl"], fontsize=12)
plt.grid(linestyle="dotted")

REGR = "-regressfit" if args.regressfit else ""
ORB_POSTFIX = "-orb" if args.orbital else ""
SUBORB_POSTFIX = f"-suborb-{args.height}km{REGR}" if args.suborb else ""
DEEP_POSTFIX = f"-deep{REGR}" if args.deep else ""
FILENAME = f"launches{ORB_POSTFIX}{DEEP_POSTFIX}{SUBORB_POSTFIX}-{LOC}"
plots_dir = os.path.join(os.pardir, os.pardir, os.pardir, "plots", "launches")
tmp_pth = os.path.join(plots_dir, FILENAME + "_." + FILE_EXT)
pth = os.path.join(plots_dir, FILENAME + "." + FILE_EXT)
plt.savefig(tmp_pth, dpi=120)

if FILE_EXT == "svg":
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
