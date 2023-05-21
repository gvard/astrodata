"""Python script for plotting graph with statistics of near-Earth objects.
Data taken from: https://cneos.jpl.nasa.gov/stats/totals.html
List of successfully predicted asteroid impacts:
https://en.wikipedia.org/wiki/Asteroid_impact_prediction#List_of_successfully_predicted_asteroid_impacts
"""

from datetime import datetime, timedelta
import locale
import os
import csv

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scour import scour


def optimize_svg(tmp_pth, pth):
    """Optimize svg file using scour"""
    with open(tmp_pth, 'rb') as inputfile, open(pth, 'wb') as outputfile:
        options = scour.generateDefaultOptions()
        options.enable_viewboxing = True
        options.strip_comments = True
        options.strip_ids = True
        options.remove_metadata = True
        options.shorten_ids = True
        options.indent_type = 'none'
        options.newlines = False
        scour.start(options, inputfile, outputfile)


CSV_PTH = '../../../data/Discovery StatisticsPrintDownload.csv'

with open(CSV_PTH, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    dats, pha_nums, phakm_nums, nea_nums, neo_nums = [], [], [], [], []
    neakm_nums, nea140_nums = [], []
    for row in reader:
        dats.append(datetime.strptime(row['Date'], '%Y-%m-%d'))
        pha_nums.append(int(row['PHA']))
        phakm_nums.append(int(row['PHA-km']))
        nea_nums.append(int(row['NEA']))
        neakm_nums.append(int(row['NEA-km']))
        nea140_nums.append(int(row['NEA-140m']))
        neo_nums.append(int(row['NEO']))

locale.setlocale(locale.LC_ALL, 'ru_RU')
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year
CROP = -12
COLORS = plt.rcParams['axes.prop_cycle'].by_key()['color']
XLIMS = datetime(year=2002, month=1, day=1), today+timedelta(weeks=9)

fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)
years = mdates.YearLocator(1)
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))

plt.plot(dats[:CROP], neo_nums[:CROP], '.-', label="Околоземные объекты", ms=2, lw=1)
plt.plot(dats[:CROP], nea_nums[:CROP], '.-', label="Околоземные астероиды", ms=2, lw=1)
plt.plot(dats[:CROP], nea140_nums[:CROP], '.-', label="Околоземные астероиды от 140 м", ms=5, lw=2)
plt.plot(dats[:CROP], pha_nums[:CROP], '.-k', label="Потенциально опасные астероиды", ms=5, lw=2)
plt.plot(dats[:CROP], neakm_nums[:CROP], '.-', color=COLORS[4],
    label="Околоземные астероиды от 1 км", ms=5, lw=2)
plt.plot(dats[:CROP], phakm_nums[:CROP], '.-', color=COLORS[3],
    label="Потенциально опасные астероиды от 1 км", ms=5, lw=2)

YLIM = (0, neo_nums[0]+700)
plt.ylim(YLIM)
plt.legend(fontsize=13)
plt.xlim(XLIMS)
plt.title(f'Динамика открытий околоземных объектов. Всего {nea_nums[0]} ' + \
    f'околоземных и {pha_nums[0]} потенциально опасных астероидов. {MONTH} {YEAR} года',
    fontsize=14)
plt.xlabel('Дата открытия, годы', fontsize=13)
plt.ylabel('Совокупное количество открытых объектов', fontsize=13)
plt.grid(linestyle='dotted')

FILE_EXT = 'svg'
FILENAME = 'neo_pha_graph-2002'
plots_dir = os.path.join(os.pardir, os.pardir, os.pardir, 'plots', 'solarsystem')
tmp_pth = os.path.join(plots_dir, FILENAME+'_.'+FILE_EXT)
pth = os.path.join(plots_dir, FILENAME+'.'+FILE_EXT)
plt.savefig(tmp_pth, dpi=240)

if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)


fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(mdates.MonthLocator(7))

plt.plot(dats[:CROP], pha_nums[:CROP], '.-k', label="Потенциально опасные астероиды", ms=5, lw=2)
plt.plot(dats[:CROP], neakm_nums[:CROP], '.-', color=COLORS[4],
    label="Околоземные астероиды от 1 км", ms=5, lw=2)
plt.plot(dats[:CROP], phakm_nums[:CROP], '.-r', color=COLORS[3],
    label="Потенциально опасные астероиды от 1 км", ms=5, lw=2)

accidents = [(2008, 10, 6, '2008 TC3'), (2014, 1, 1, '2014 AA'), (2018, 6, 2, '2018 LA'),
             (2019, 6, 22, '2019 MO'), (2022, 3, 11, '2022 EB5'), (2022, 11, 19, '2022 WJ1'),
             (2023, 2, 12, '2023 CX1')]

for ac in accidents:
    dat = datetime(year=ac[0], month=ac[1], day=ac[2])
    plt.plot((dat, dat), YLIM, '--g')
plt.plot((dat, dat), YLIM, '--g', label="Успешно предсказанные столкновения с Землей")

YLIM  = (0, pha_nums[0]+70)
plt.ylim(YLIM)
plt.legend(fontsize=13)
# plt.xlim(datetime(year=1990, month=1, day=1), datetime(year=2023, month=6, day=1))
plt.xlim(XLIMS)
plt.title(f'Динамика открытий околоземных объектов. Всего {nea_nums[0]} ' + \
    f'околоземных и {pha_nums[0]} потенциально опасных астероидов. {MONTH} {YEAR} года',
    fontsize=14)
plt.xlabel('Дата открытия, годы', fontsize=13)
plt.ylabel('Совокупное количество открытых объектов', fontsize=13)
plt.grid(linestyle='dotted')

FILE_EXT = 'svg'
FILENAME = 'pha_graph_predicted_impacts-2002'
tmp_pth = os.path.join(plots_dir, FILENAME+'_.'+FILE_EXT)
pth = os.path.join(plots_dir, FILENAME+'.'+FILE_EXT)
plt.savefig(tmp_pth, dpi=240)

if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
