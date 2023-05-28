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
    han, lab = [], []
    for ax in axes:
        tmp = ax.get_legend_handles_labels()
        han.extend(tmp[0])
        lab.extend(tmp[1])
    return han, lab

def get_table(url, local=False):
    """Read ASCII data table from pre html element"""
    if local:
        html = open(url, encoding='utf-8')
    else:
        html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html5lib')
    return soup.find('table').findAll('tr')


parser = argparse.ArgumentParser(description='Graph plotter script with number of people in space')
parser.add_argument('-m', '--method', action='store_true', help='Switch to plt.stairs method')
parser.add_argument('-f', '--filled', action='store_true', help='Fill plot area')
parser.add_argument('-a', '--accidents', action='store_true', help='Plot accidents dates')
parser.add_argument('-p', '--private', action='store_true', help='Plot private spaceflights dates')
parser.add_argument('-s', '--spent', action='store_true',
                    help='Plot total time spent by humans in space')
args = parser.parse_args()

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


data_to_plot = dats + [today]
nums_to_plot = nums + [nums[-1]]
if not args.method:
    LW = 0.9
    if args.filled:
        data_to_plot.append(today)
        nums_to_plot.append(0)
        ax.fill_between(data_to_plot, nums_to_plot, step="post", color='#229')
        LW= 0.5
    ax.step(data_to_plot, nums_to_plot, 'b', where='post', lw=LW)
else:
    ax.stairs(nums, data_to_plot, fill=args.filled, alpha=1,
        color='b') # baseline=None

tdlt = timedelta(days=300)
plt.xlim(dats[0]-tdlt/2, dats[-1]+tdlt)
# plt.xlim(datetime(year=1960, month=1, day=1), datetime(year=1987, month=1, day=1))
# plt.xlim(datetime(year=1995, month=1, day=1), datetime(year=2023, month=1, day=1))
# plt.xlim(datetime(year=2010, month=1, day=1), datetime(year=2023, month=1, day=1))
# plt.xlim(datetime(year=2018, month=9, day=1), datetime(year=2023, month=1, day=1))

if args.spent:
    ax2 = ax.twinx()
    ax2.plot(dats + [today], manyr_sums, '--y', lw=4,
        label='Время, проведенное людьми в космосе')
    ax2.set_ylim(0, manyr_sums[-1]+2.2)
    ax2.set_ylabel('Проведенное время в космосе, человеко-лет', fontsize=14)
ax.set_facecolor("none")
ax.set_zorder(1)
YLIM = 20
ax.set_ylim(0, YLIM)
ax.set_xlabel('Время, годы', fontsize=14)
ax.set_ylabel('Человек в космосе', fontsize=14)

TM = timedelta(weeks=48)
TM_SHIFT = timedelta(weeks=12)
SH, SH2 = 0.2, 1.2
accidents = [
    # (1960, 10, 24, 'Катастрофа на космодроме Байконур, МБР Р-16', SH, TM),
    (1961, 3, 23, 'Пожар, гибель В.В. Бондаренко', SH2, -TM_SHIFT),
    (1967, 1, 27, 'Пожар на «Аполлоне-1»', SH2, TM),
    (1967, 4, 23, 'Гибель Комарова, нераскрытие парашюта «Союза-1»', SH2, -TM_SHIFT*2.9),
    (1967, 11, 15, 'X-15, гибель М.Д. Адамса', SH2, -TM_SHIFT*2.9-TM_SHIFT),
    (1971, 6, 30, 'Разгерметизация «Союза-11»', SH2, TM),
    (1980, 3, 18, 'Катастрофа на космодроме Плесецк', SH2, TM),
    (1986, 1, 28, 'Катастрофа «Челленджера»', SH, TM),
    (2003, 2, 1, 'Катастрофа «Колумбии»', SH, TM)]

private_spaceflights = [(2001, 4, 28, 'Деннис Тито, Союз ТМ-32', SH, TM),
    (2020, 5, 30, 'SpaceX DM-2', SH, TM), (2021, 7, 11, 'VG Unity 22/NS-16', SH, TM),
    (2021, 7, 20, '', SH, TM), (2021, 9, 16, 'Inspirati④n', SH, -TM_SHIFT)]

if args.accidents:
    for ac in accidents:
        dat = datetime(year=ac[0], month=ac[1], day=ac[2])
        ax.plot((dat, dat), (0, YLIM), '--r')
        ax.text(dat-ac[5], YLIM-ac[4], ac[3], rotation='vertical', va="top", fontsize=14)
if args.private:
    for ac in private_spaceflights:
        dat = datetime(year=ac[0], month=ac[1], day=ac[2])
        ax.plot((dat, dat), (0, YLIM), '--g')
        ax.text(dat-ac[5], YLIM-ac[4], ac[3], rotation='vertical', va="top", fontsize=14)

if args.spent:
    handles, labels = unite_legends([ax, ax2])
    ax.legend(handles, labels, loc='upper left', fontsize=13)

ax.grid(linestyle='dotted', axis='y')
plt.title(f'Перепись космического населения, {len(nums)} изменений. Люди ' + \
    f'провели в космосе {round(manyr_sums[-1], 1)} человеко-лет. {MONTH} {YEAR} года')

METHD = 'stairs' if args.method else 'steps'
FILENAME = f"spacepop-{'spent-' if args.spent else ''}{METHD}{'-filled' if args.filled else ''}"

FILE_EXT = 'svg'
plots_dir = os.path.join(os.pardir, os.pardir, os.pardir, 'plots', 'manned')
tmp_pth = os.path.join(plots_dir, FILENAME+'_.'+FILE_EXT)
pth = os.path.join(plots_dir, FILENAME+'.'+FILE_EXT)
plt.savefig(tmp_pth, dpi=240)

if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
