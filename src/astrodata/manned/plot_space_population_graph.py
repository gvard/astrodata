"""Python script for plotting graph with number of people in space.
Data taken from Jonathan's Space Pages:
https://planet4589.org/space/astro/web/pop.html
"""

from datetime import datetime, timedelta
import os
import locale
import urllib.request

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from scour import scour
from astropy.time import Time


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

def unite_legends(axes):
    """Hack to display legend over other plots
    https://github.com/matplotlib/matplotlib/issues/3706#issuecomment-164265176
    """
    h, l = [], []
    for ax in axes:
        tmp = ax.get_legend_handles_labels()
        h.extend(tmp[0])
        l.extend(tmp[1])
    return h, l

def get_table(url, local=False):
    """Read ASCII data table from pre html element"""
    if local:
        html = open(url, encoding='utf-8')
    else:
        html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html5lib')
    return soup.find('table').findAll('tr')


SPACEPOP_URL = "https://planet4589.org/space/astro/web/pop.html"

data = get_table(SPACEPOP_URL)
nums, dats, mjds, manyrs, manyr_sums = [], [], [], [], []
for i, tr in enumerate(data[3:]):
    tds = tr.findAll('td')
    num = int(tds[1].text)
    dats.append(datetime.strptime(tds[2].text.strip(), '%Y %b %d %H%M:%S'))
    mjd = float(tds[0].text)
    if i:
        manyrs.append((mjd - mjds[-1]) * nums[-1] / 365.2425)
    mjds.append(mjd)
    nums.append(num)
    manyr_sums.append(sum(manyrs))
manyrs.append((Time.now().mjd - mjds[-1]) * nums[-1] / 365.2425)
manyr_sums.append(sum(manyrs))


fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.94, 0.97) #0.99
years = mdates.YearLocator(5) #1 2 5
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(mdates.YearLocator())
ax.yaxis.set_major_locator(MultipleLocator(1))

locale.setlocale(locale.LC_ALL, 'ru_RU')
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year

METHOD = 'step' #stairs
FILLED = True
if METHOD == 'step':
    plt.step(dats + [today, today], nums + [nums[-1], 0], 'b', where='post', lw=0.9)
    if FILLED:
        plt.fill_between(dats, nums, step="post", color='#229')
elif METHOD == 'stairs':
    dats_stairs = dats + [today]
    plt.stairs(nums, dats_stairs, fill=FILLED, alpha=0.9,
        color='b', lw=1, label='stairs()') # baseline=None

tdlt = timedelta(days=300)
plt.xlim(dats[0]-tdlt/2, dats[-1]+tdlt)
# plt.xlim(datetime(year=1960, month=1, day=1), datetime(year=1987, month=1, day=1))
# plt.xlim(datetime(year=1995, month=1, day=1), datetime(year=2023, month=1, day=1))
# plt.xlim(datetime(year=2010, month=1, day=1), datetime(year=2023, month=1, day=1))
# plt.xlim(datetime(year=2018, month=9, day=1), datetime(year=2023, month=1, day=1))

SPENT = 'spent-'
if SPENT:
    ax2 = ax.twinx()
    ax2.plot(dats + [today], manyr_sums, '--y', lw=4,
        label='Время, проведенное людьми в космосе')
    ax2.set_ylim(0, manyr_sums[-1]+2.2)
    ax2.set_ylabel('Проведенное время в космосе, человеко-лет', fontsize=14)
ax.set_facecolor("none")
ax.set_zorder(2)
ax.set_ylim(0, 20)
ax.set_xlabel('Время, годы', fontsize=14)
ax.set_ylabel('Человек в космосе', fontsize=14)

YLIM = 20
TM = timedelta(weeks=48)
accidents = [(1967, 1, 27, 'Пожар на «Аполлоне-1»', 1.2), (1967, 4, 23, '', 0),
    (1971, 6, 29, 'Катастрофа «Союз-11»', 1.2),
    (1986, 1, 28, 'Катастрофа «Челленджера»', 0.2),
    (2003, 2, 1, 'Катастрофа «Колумбии»', 0.2)]
private_spaceflights = [(2001, 4, 28, 'Деннис Тито, Союз ТМ-32'),
    (2020, 5, 30, 'SpaceX DM-2'), (2021, 7, 11, 'VSS Unity 22'),
    (2021, 7, 20, ''), (2021, 9, 16, '')]

if accidents:
    for ac in accidents:
        dat = datetime(year=ac[0], month=ac[1], day=ac[2])
        ax.plot((dat, dat), (0, YLIM), '--r')
        ax.text(dat-TM, YLIM-ac[4], ac[3], rotation='vertical', va="top", fontsize=14,
            zorder=0)
if private_spaceflights:
    for ac in private_spaceflights:
        dat = datetime(year=ac[0], month=ac[1], day=ac[2])
        ax.plot((dat, dat), (0, YLIM), '--g')
        ax.text(dat-TM, YLIM-0.2, ac[3], rotation='vertical', va="top", fontsize=14,
            zorder=0)

handles, labels = unite_legends([ax, ax2])
ax.legend(handles, labels, loc='upper left', fontsize=13)

ax.grid(linestyle='dotted', axis='y')
plt.title(f'Перепись космического населения, {len(nums)} изменений. Люди ' + \
    f'провели в космосе {round(manyr_sums[-1], 1)} человеко-лет. {MONTH} {YEAR} года')

FILENAME = 'spacepop-' + SPENT + METHOD # -accidents -privateflights
if FILLED:
    FILENAME += '-filled'

FILE_EXT = 'svg'
plots_dir = os.path.join(os.pardir, os.pardir, os.pardir, 'plots', 'manned')
tmp_pth = os.path.join(plots_dir, FILENAME+'_.'+FILE_EXT)
pth = os.path.join(plots_dir, FILENAME+'.'+FILE_EXT)
plt.savefig(tmp_pth, dpi=240)

if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
