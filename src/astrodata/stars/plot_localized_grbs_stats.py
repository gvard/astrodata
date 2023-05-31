"""Python script for plotting charts with localized GRBs statistics.
Data source:
Gamma-ray bursts localized within a few hours to days to less than 1 degree
https://www.mpe.mpg.de/~jcg/grbgen.html
"""

import os
from datetime import datetime
import locale
import argparse

from scour import scour
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import pandas as pd

from transients import get_soup_request


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

def get_grbs_tables(soup):
    """Get GRBs stats from all data and summary tables."""
    _all_tabs = soup.findAll('table')
    trs_all = _all_tabs[0].findAll('tr')
    trs_summary = _all_tabs[-1].findAll('tr')
    return trs_all, trs_summary

def get_summary_grbs_stats(trs):
    """Get GRBs stats from raws of summary table."""
    years, gnums, opts = [], [], []
    for tr in trs[1:-1]:
        tds = tr.findAll('td')
        opt = int(tds[3].text)
        years.append(int(tds[0].text))
        gnums.append(int(tds[1].text) - opt)
        opts.append(opt)
    return years, gnums, opts

def parse_table(trs):
    """Get GRBs stats from rows of big data table"""
    nums, ot_num, xa_num, ra_num, rs_num = 0, 0, 0, 0, 0
    grb_dates, grbnums, otnums, xanums, ranums, rss = [], [], [], [], [], []
    years_dct, opts_dct = {}, {}
    if args.verbose:
        print('Start parsing table with GRBs stats')
    for tr in trs[1:]:
        tds = tr.findAll('td')
        grbname = tds[0].a.text
        xray_ag = tds[5].text
        apt_ag = tds[6].text
        rad_ag = tds[7].text
        redshift = tds[9].text

        if redshift.strip():
            rs_num += 1
        if xray_ag and xray_ag[0] =="y":
            xa_num += 1
        if rad_ag and rad_ag[0] =="y":
            ra_num += 1
        year = grbname[:2]
        if year[0] in ("2", "1", "0"):
            year = int("20"+year)
        elif year[0] == "9":
            year = int("19"+year)
        grb_date = datetime(year, int(grbname[2:4]), int(grbname[4:6]))
        if apt_ag and apt_ag.strip() in ("y", "SN"): # with or without "y?"
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
    if args.verbose:
        print('GRBs stats:', years_dct, opts_dct)
    return grb_dates, grbnums, otnums, xanums, ranums, rss, years_dct, opts_dct


parser = argparse.ArgumentParser(description='Graph plotter script with number of gamma-ray bursts')
parser.add_argument('-v', '--verbose', action='store_true', help='Print additional information')
args = parser.parse_args()

soup = get_soup_request('https://www.mpe.mpg.de/~jcg/grbgen.html', 'lxml')
if args.verbose:
    print('get GRBs stats tables')
trs_all, trs_summary = get_grbs_tables(soup)
if args.verbose:
    print('get data from GRBs stats summary table')
years_s, gnums_s, opts_s = get_summary_grbs_stats(trs_summary)
years, grbnums, otnums, xanums, ranums, rss, years_dct, opts_dct = parse_table(trs_all)

locale.setlocale(locale.LC_ALL, 'ru_RU')
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year
PLOTS_DIR = os.path.join(os.pardir, os.pardir, os.pardir, 'plots', 'stars')
FILE_EXT = 'png'
TOTAL_GRBS_FILENAME = 'grbs_total_number_plot.' + FILE_EXT
pth = os.path.join(PLOTS_DIR, TOTAL_GRBS_FILENAME)
tmp_pth = os.path.join(PLOTS_DIR, 'grbs_total_number_plot_.'+FILE_EXT)

fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97) #left=0.06, bottom=0.06, right=0.97, top=0.955
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.yaxis.set_minor_locator(MultipleLocator(250))

years = years[::-1]
MS = 2
plt.plot(years, grbnums, 'ok-', ms=MS+2,
    label=f"Локализованные гамма-всплески: {len(grbnums)} событие")
plt.plot(years, xanums, 'o-', ms=MS, color='indigo',
    label=f"Послесвечения в рентгене: {xanums[-1]} событий")
plt.plot(years, otnums, 'og-', ms=MS+1,
    label=f"Оптические послесвечения: {otnums[-1]} событий")
plt.plot(years, rss, 'o-', ms=MS, color='red',
    label=f"Гамма-всплески с известным красным смещением: {rss[-1]} событие")
plt.plot(years, ranums, 'o-', ms=MS, color='navy',
    label=f"Послесвечения в радио: {ranums[-1]} событий")

plt.xlim(datetime(1996, 1, 1), datetime(2023, 12, 1))
plt.ylim(-15, 2500)
TITLE = 'Статистика гамма-всплесков, локализованных в пределах 1 градуса.'
plt.title(TITLE + f' {MONTH} {YEAR} года', fontsize=15)
plt.xlabel('Время', fontsize=14)
plt.ylabel('Количество гамма-всплесков', fontsize=14)
plt.grid(axis='y', which='major', linestyle='--')
plt.grid(axis='x', which='major', linestyle=':')
plt.grid(axis='y', which='minor', linestyle=':')
plt.legend(fontsize=14, loc='upper left')

plt.savefig(tmp_pth, dpi=120)
if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)

if args.verbose:
    print("Plot stacked bar chart with numbers of optical afterglows")

grbnums = list(years_dct.values())[::-1][1:]
opts = list(opts_dct.values())[::-1]
years_to_plot = list(opts_dct.keys())[::-1]
all_grbs = sum(grbnums)

grbnums_noopt = []
all_grb_count, opt_count = 0, 0
for i, year in enumerate(years_to_plot):
    all_grb_count += grbnums[i]
    opt_count += opts[i]
    if args.verbose:
        print(f"За {year} год {grbnums[i]} локализованных GRB, {opts[i]} послесвечений." + \
            f" Всего к концу года {all_grb_count} GRB, {opt_count} послесвечений")
    grbnums_noopt.append(grbnums[i]-opts[i])

FILE_EXT = 'svg'
TMP_FILENAME = 'grbs_stats_bar_chart_.' + FILE_EXT
FILENAME = 'grbs_stats_bar_chart.' + FILE_EXT
tmp_pth = os.path.join(PLOTS_DIR, TMP_FILENAME)
pth = os.path.join(PLOTS_DIR, FILENAME)

data = {'Локализованные гамма-всплески без afterglow': grbnums_noopt,
'Гамма-всплески с оптическими послесвечениями': opts}
df = pd.DataFrame(data, index=years_to_plot)

ax = df.plot(kind='bar', stacked=True, figsize=(16, 9), width=0.85, rot=0)
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.97, top=0.955) #0.048, 0.06, 0.99, 0.97
plt.xlabel('Год', fontsize=14)
plt.ylabel('Гамма-всплесков за год', fontsize=14)
plt.title(f'{TITLE} Всего {all_grbs} событий. {MONTH} {YEAR} года', fontsize=16)
plt.legend(fontsize=14, loc='upper left')
ax.yaxis.set_minor_locator(MultipleLocator(5))
ax.bar_label(ax.containers[-1])

plt.savefig(tmp_pth, dpi=240)
if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
