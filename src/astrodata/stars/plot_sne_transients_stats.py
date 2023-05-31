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

from scour import scour
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
import pandas as pd

from transients import add_iau_sne, get_soup_request, get_sn_stats, get_sn_count, \
    get_tns_stats, get_tns_year_stats, mk_sne_iau_lst, mk_transient_total_numbers, \
    mk_tns_data, mk_urls_lst


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


parser = argparse.ArgumentParser(description='Graph plotter script with number of transients')
parser.add_argument('-v', '--verbose', action='store_true', help='Print additional information')
parser.add_argument('-y', '--startyear', type=int, default=2004,
    help='Set year to start. Default is 2004')
args = parser.parse_args()

locale.setlocale(locale.LC_ALL, 'ru_RU')
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year
COLORS = plt.rcParams['axes.prop_cycle'].by_key()['color']
COLORS = [COLORS[3], COLORS[0], COLORS[1]]
STARS_DIR = os.path.join(os.pardir, os.pardir, os.pardir, 'plots', 'stars')

stat_cat_pub, stat_cat_all = get_tns_stats()
nums_pub, yrs_ints, realdates, stats_pub_dct, tns_pub_final_dct = get_tns_year_stats(stat_cat_pub)
nums_all, yrs_ints, realdates, stats_all_dct, tns_all_final_dct = get_tns_year_stats(stat_cat_all)
sne_final_dct = add_iau_sne(tns_pub_final_dct)
total_dct = dict(sorted(sne_final_dct.items()))
total_lst = mk_transient_total_numbers(total_dct)
SNE_IAU_LST = mk_sne_iau_lst(args.startyear, YEAR)
data_to_plot_dct, nums_diff_dct = mk_tns_data(stats_pub_dct, stats_all_dct,
    start_year=args.startyear)
ALL_TNS = sum(data_to_plot_dct.values())

FILE_EXT = 'svg'
TMP_FILENAME = 'transient_stats_bar_chart_.' + FILE_EXT
FILENAME = 'transient_stats_bar_chart.' + FILE_EXT
tmp_pth = os.path.join(STARS_DIR, TMP_FILENAME)
pth = os.path.join(STARS_DIR, FILENAME)
labels = list(data_to_plot_dct.keys())
labels[0] = f"до {args.startyear}"
title = f'Статистика транзиентов по годам, всего {ALL_TNS} публичных транзиентов'
XLABEL = 'Годы'
YLABEL = 'Транзиентов за год'

if args.verbose:
    tns_before_startyear = SNE_IAU_LST[0] + data_to_plot_dct[args.startyear-1]
    print(labels[0] + f" года {SNE_IAU_LST[0]} сверхновых в CBAT, " + \
        f"{data_to_plot_dct[args.startyear-1]} на TNS, всего {tns_before_startyear}")

data = {'Сверхновые CBAT': SNE_IAU_LST,
'Публичные транзиенты': data_to_plot_dct.values(),
'Транзиенты не в публичном доступе': nums_diff_dct.values()}
df = pd.DataFrame(data, index=labels)

ax = df.plot(kind='bar', stacked=True, figsize=(16, 9), color=COLORS, width=0.85, rot=0)
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.97, top=0.955)
plt.xlabel(XLABEL, fontsize=14)
plt.ylabel(YLABEL, fontsize=14)
plt.title(title+f'. {MONTH} {YEAR} года', fontsize=16)
plt.legend(fontsize=14, loc='upper left')
ax.yaxis.set_minor_locator(MultipleLocator(1000))
for x, y in enumerate(df.sum(axis=1)):
    ax.annotate(int(y), (x, y+190), ha='center')

plt.savefig(tmp_pth, dpi=240)
if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)

if args.verbose:
    print("Collect data from Latest Supernovae Archives by David Bishop")

snstats = {}
years, sns, snalt, all_sne = [], [], [], []
years_dt = []
all_sn_count, sn_amateur_count = 0, 0
snyears_urls = mk_urls_lst()
for i, (year, snstats_url) in enumerate(snyears_urls):
    soup = get_soup_request(snstats_url)
    snstats[year], lastmod = get_sn_stats(soup)
    sn_num, sn_cbat, sn_amateur, sn_13th = get_sn_count(snstats[year])
    all_sn_count += sn_num
    sn_amateur_count += sn_amateur
    if year == 1995:
        all_sne.append(all_sn_count)
        print(f"До 1996г: {sn_num} сверхновых, {sne_final_dct[datetime(year+1, 1, 1)]}" + \
              f" транзиентов, {sn_amateur} открыто любителями, {sn_13th} " + \
              f"ярче 13 зв. вел на {lastmod}")
        years.append(year)
        years_dt.append(datetime(year+1, 1, 1))
        sns.append(sn_num - sn_amateur)
        snalt.append(sn_amateur)
    elif year != "all":
        all_sne.append(all_sn_count)
        if year == YEAR:
            tr_num = sne_final_dct.get(today)
            years_dt.append(today)
        else:
            tr_num = sne_final_dct.get(datetime(year+1, 1, 1))
            years_dt.append(datetime(year+1, 1, 1))
        print(f"{year} год: {sn_num} сверхновых, {tr_num} транзиентов, {sn_amateur}" + \
              f" открыто любителями, {sn_13th} ярче 13 зв. вел. Всего к концу года: " + \
              f"{all_sn_count}, {total_lst[i]} транзиентов, {sn_amateur_count} любителями" + \
              f" на {lastmod}")
        years.append(year)
        sns.append(sn_num - sn_amateur)
        snalt.append(sn_amateur)
    else:
        print(f"Всего {sn_num}, а в сумме {all_sne[-1]} СН, {sn_amateur} открыто любителями," + \
              f" {sn_13th} ярче 13 зв. величины на дату {lastmod}")


FILE_EXT = 'svg'
TMP_FILENAME = 'sne_stats_bar_chart_.' + FILE_EXT
FILENAME = 'sne_stats_bar_chart.' + FILE_EXT
tmp_pth = os.path.join(STARS_DIR, TMP_FILENAME)
pth = os.path.join(STARS_DIR, FILENAME)

years[0] = f"до {min(1996, args.startyear)}"
data = {'Сверхновые Latest Supernovae Archives': sns,
'Сверхновые, обнаруженные любителями': snalt}
df = pd.DataFrame(data, index=years)

ax = df.plot(kind='bar', stacked=True, figsize=(16, 9), width=0.85, rot=0)
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.97, top=0.955)
plt.xlabel('Годы', fontsize=14)
plt.ylabel('Открытий сверхновых за год', fontsize=14)
title = f'Статистика открытий сверхновых по годам, всего {all_sne[-1]} сверхновых.'
plt.title(title+f' {MONTH} {YEAR} года', fontsize=16)
plt.legend(fontsize=14, loc='upper left')
ax.yaxis.set_minor_locator(MultipleLocator(500))
ax.bar_label(ax.containers[-1])

plt.savefig(tmp_pth, dpi=240)
if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)


FILE_EXT = 'svg'
TOTAL_SNE_FILENAME = 'sne_transients_total_number_log_plot.' + FILE_EXT
pth = os.path.join(STARS_DIR, TOTAL_SNE_FILENAME)
TMP_FILENAME = 'sne_transients_total_number_log_plot_.' + FILE_EXT
tmp_pth = os.path.join(STARS_DIR, TMP_FILENAME)

fig, ax = plt.subplots(figsize=(16, 9))
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.97, top=0.955)
ax.xaxis.set_major_locator(mdates.YearLocator(1))

plt.plot(years_dt, all_sne, 'ok-', label="David Bishop, Latest Supernovae Archives")
plt.plot(total_dct.keys(), total_lst, 'or-',
    label="Transient Name Server, public + CBAT SNe before 2016")
plt.xlim(datetime(1995, 10, 1), today+timedelta(weeks=31.9))
plt.ylim(1000, 150000)
plt.yscale("log")
plt.legend(fontsize=14)
plt.title(f'Динамика вспышек сверхновых, всего {all_sne[-1]} сверхновых и {total_lst[-1]} ' + \
          f'транзиентов. {MONTH} {YEAR} года', fontsize=16)
plt.xlabel('Время', fontsize=14)
plt.ylabel('Количество открытых сверхновых', fontsize=14)
plt.grid(axis='y', which='major', linestyle='-')
plt.grid(axis='x', which='major', linestyle=':')
plt.grid(axis='y', which='minor', linestyle='--')
plt.savefig(tmp_pth, dpi=240)
if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
