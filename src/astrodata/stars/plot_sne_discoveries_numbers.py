"""Python script for reading numbers of discovered supernova in all versions of
html page with statistics from git repo.
How to get all previous versions of a specific file/folder:
https://stackoverflow.com/questions/12850030/git-getting-all-previous-version-of-a-specific-file-folder
Github repo: https://github.com/gvard/gvard.github.io
html files with stats:
https://github.com/gvard/gvard.github.io/blob/main/stars/stats/index.html
https://github.com/gvard/gvard.github.io/blob/main/stars/stats.html
"""

import re
import os
import itertools
import locale
import calendar
from datetime import datetime, timedelta

from scour import scour
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator


def optimize_svg(tmp_path, path):
    """Optimize svg file using scour"""
    with open(tmp_path, 'rb') as inputfile, open(path, 'wb') as outputfile:
        options = scour.generateDefaultOptions()
        options.enable_viewboxing = True
        options.strip_comments = True
        options.strip_ids = True
        options.remove_metadata = True
        options.shorten_ids = True
        options.indent_type = 'none'
        options.newlines = False
        scour.start(options, inputfile, outputfile)


def get_nums(html, ul_num=0):
    """Get supernova numbers from html code"""
    dct = {}
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.findAll("ul")[ul_num]
    lis = ul.findAll("li")
    for li in lis:
        txt = li.text.split()
        try:
            if int(txt[1]) == 1996 and int(txt[4]) > 1000:
                # number of SN discoveries before 1996 are saved with 1995 key
                dct[int(txt[1]) - 1] = int(txt[4])
            else:
                dct[int(txt[1])] = int(txt[4])
        except ValueError:
            pass  # unused strings with total stats are ignored
    for yr in range(2021, END_YR):
        if yr not in dct:
            dct[yr] = None
    return dct


def get_date(fname, hms=True):
    """Make datetime object from numbers in file name"""
    if hms:
        (day, mon, h, m, s, yr) = datetime_pattern.findall(fname)[0]
        mon = MNTH_NAMNUM[mon]
        f_date = datetime(int(yr), mon, int(day), int(h), int(m), int(s))
    else:
        (day, mon, yr) = date_pattern.findall(fname)[0]
        mon = MNTH_NAMNUM[mon]
        f_date = datetime(int(yr), mon, int(day))
    return f_date


def fill_dct(filename, ul_num=0):
    """Fill dictionary"""
    with open(filename, encoding="utf-8") as html:
        dct = get_nums(html, ul_num=ul_num)
        for year, num in dct.items():
            all_nums[year].append(num)


def sort_data(dats, all_nums_year):
    """Sort data"""
    all_data = []
    for i, dat in enumerate(dats):
        if i < len(all_nums_year):
            all_data.append([dat, all_nums_year[i]])
    all_data.sort(key=lambda row: row[0])
    dats_sorted, nums_sorted = zip(*all_data)
    dats_sorted = list(dats_sorted)
    nums_sorted = list(nums_sorted)
    return dats_sorted, nums_sorted


MNTH_NAMNUM = {mnth: ind for ind, mnth in enumerate(calendar.month_abbr) if mnth}
ST_YR = 2015
END_YR = 2024
DATA_DIR = "../../../data/sne/"
PLOTS_DIR = "../../../plots/stars/"


# get lists of all filenames:
files_to_read = []
for html_files_dir, ul_num in (
        ("stars-stats-index.html", 0),
        ("stars-stats.html", 0),
        ("stars-stats.html-old", 1)):
    files_path = os.path.join(DATA_DIR, html_files_dir)
    filenames_lst = next(os.walk(files_path), (None, None, []))[2]
    files_to_read.append((files_path, filenames_lst, ul_num))

date_pattern = re.compile(
    r"\d+.(\d{1,2})-(Jan?|Feb?|Mar?|Apr?|May|Jun?|Jul?|Aug?|Sep?|Oct?|Nov?|"
    r"Dec?)-(\d{4}).*")
datetime_pattern = re.compile(
    r"\d+.(\d{1,2})-(Jan?|Feb?|Mar?|Apr?|May|Jun?|Jul?|Aug?|Sep?|Oct?|Nov?|"
    r"Dec?)-(\d{2})_(\d{2})_(\d{2})-(\d{4}).*")
all_nums = dict((year, []) for year in range(1995, END_YR))
dats = []
for files_path, filenames_lst, ul_num in files_to_read:
    for fname in filenames_lst:
        if files_path in (os.path.join(DATA_DIR, "stars-stats.html"),
                          os.path.join(DATA_DIR, "stars-stats-index.html")):
            f_date = get_date(fname)
        elif files_path == os.path.join(DATA_DIR, "stars-stats.html-old"):
            f_date = get_date(fname, hms=False)
        filename = os.path.join(files_path, fname)
        dats.append(f_date)
        fill_dct(filename, ul_num=ul_num)

print("Number of commits with SN data:", len(dats))

colors = itertools.cycle(["c", "m", "y", "k", "r", "g", "b", "orange", "brown", "grey"])

fig, ax = plt.subplots(figsize=(16, 9))

for year in [1995] + list(range(ST_YR, END_YR)):
    dats_sorted, nums_sorted = sort_data(dats, all_nums[year])
    dats_final, nums_final = [], []
    dats_final.append(dats_sorted[0])
    nums_final.append(nums_sorted[0])
    for i, num in enumerate(nums_sorted):
        if num != nums_final[-1]:
            dats_final.append(dats_sorted[i])
            nums_final.append(num)
    dats_final.append(dats_sorted[-1])
    nums_final.append(nums_sorted[-1])
    LBL = year
    if year == 1995:
        LBL = "до 1996"
    plt.plot(dats_final, nums_final, "o-", color=next(colors), label=LBL)

plt.legend(fontsize=9, loc="upper left")
plt.subplots_adjust(left=0.055, bottom=0.083, right=0.985, top=0.96)
dats_sorted = sorted(dats)
td = timedelta(days=20)
xlims = [dats_sorted[0], dats_sorted[-1] + td]
plt.xlim(xlims[0], xlims[-1])
plt.ylim(0, 22000)

locale.setlocale(locale.LC_ALL, "ru_RU")
today = datetime.now()
MONTH = today.strftime("%B")

ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=range(1, 13, 2)))
ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.yaxis.set_major_locator(MultipleLocator(2000))
plt.xticks(rotation=20)
plt.title(f"Динамика открытий сверхновых по годам. {MONTH} {today.year} года",
          fontsize=15)
plt.xlabel("Время", fontsize=14)
plt.ylabel("Количество сверхновых", fontsize=14)
plt.grid(axis="both", which="major", linestyle=":")

FILE_EXT = "png"
plt_pth = PLOTS_DIR + f"sne_discoveries_numbers-{ST_YR}-{END_YR}"
tmp_pth = f"{plt_pth}_.{FILE_EXT}"
pth = f"{plt_pth}.{FILE_EXT}"
plt.savefig(tmp_pth, dpi=120)

if FILE_EXT == "svg":
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
