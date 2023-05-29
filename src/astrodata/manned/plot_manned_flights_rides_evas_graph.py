"""Python script for plotting graph with manned flights statistics:
flights, astronauts, its rides and EVAs.
Data taken from:
Jonathan's Space Pages https://planet4589.org/space/astro/web/
World Space Flight. Chronological Order of All FAI First Flights
https://www.worldspaceflight.com/bios/chronology.php
Sequential Flight List
https://www.worldspaceflight.com/bios/sequence.php
"""

from datetime import datetime, timedelta
import os
import locale
import urllib.request
from argparse import ArgumentParser

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
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

def get_table(url):
    """Read ASCII data table from pre html element"""
    html = urllib.request.urlopen(url).read()
    #html = open(url) # for local file
    soup = BeautifulSoup(html, 'html.parser')
    return soup.findAll('pre')[1].text.splitlines()

def get_flights_table(url):
    """Read date from HTML page"""
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup.findAll('table')[0]


DATA_BASE_URL = "https://planet4589.org/space/astro/lists/"
MISSIONS_URL = DATA_BASE_URL + "missions.html"
EVAS_URL = DATA_BASE_URL +  "evas.html"
FLIGHTS_URL = "https://www.worldspaceflight.com/bios/chronology.php"

parser = ArgumentParser(description='Graph plotter script with number of people in space')
parser.add_argument('-r', '--rides', action='store_true', help='Plot rides')
parser.add_argument('-e', '--evas', action='store_true', help='Plot EVAs')
parser.add_argument('-a', '--astros', action='store_true', help='Plot astronauts numbers')
parser.add_argument('-f', '--flights', action='store_true', help='Plot flights numbers')
parser.add_argument('-c', '--counts', action='store_true', help='Plot EVAs counts')
args = parser.parse_args()

data = get_table(MISSIONS_URL)[1:]
dates, flights_nums, rides_nums = [], [], []
flights_num, rides_num = 0, 0
orb_num, suborb_num = 0, 0
for line in data:
    if line and line[1] == '0':
        dd = datetime.strptime(line[77:93], '%Y %b %d %H%M')
        dates.append(dd)
        flights_num += 1
        rides_num += int(line[139])
        OrbID = line[197:203]
        if OrbID[:2] == 'SO':
            suborb_num += 1
        elif OrbID[:2] == 'OR':
            orb_num += 1
        flights_nums.append(flights_num)
        rides_nums.append(rides_num)

flights_table = get_flights_table(FLIGHTS_URL)
flights_num = 0
flight_nums, flight_dates, ships = [], [], []
for tr in flights_table.findAll('tr'):
    tds = tr.findAll('td')
    if len(tds):
        flights_num += 1
        flight_nums.append(flights_num)
        flight_dates.append(datetime.strptime(tds[2].text, '%d %B %Y'))

data = get_table(EVAS_URL)[1:]
evadates, evanums, evatds = [], [], []
astro_num = 0
evas_total_time = timedelta(0)
for line in data:
    if line:
        depress_time = datetime.strptime(line[170:186], '%Y %b %d %H%M') #dd
        repress_time = datetime.strptime(line[296:312], '%Y %b %d %H%M')
        if repress_time == datetime.strptime('2021 Aug  3 0633', '%Y %b %d %H%M'):
            repress_time = datetime.strptime('2021 Aug 20 0633', '%Y %b %d %H%M')
        elif repress_time == datetime.strptime('2023 Apr 15 0950', '%Y %b %d %H%M'):
            repress_time = datetime.strptime('2023 Apr 19 0950', '%Y %b %d %H%M')
        eva_duration = repress_time - depress_time
        evas_total_time += eva_duration
        evadates.append(depress_time)
        evatds.append(evas_total_time.total_seconds()/86400) # in days
        astro_num += 1
        evanums.append(astro_num)


fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)
years = mdates.YearLocator(5)
oneyear = mdates.YearLocator()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(oneyear)

tdlt = timedelta(days=468)
locale.setlocale(locale.LC_ALL, 'ru_RU')
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year

# Graph settings
TM = timedelta(weeks=48)
TM_SHIFT = timedelta(weeks=12)
SH, SH2 = 13, 230
YLIM_TOP_MARGIN = 15
TITLE = 'Присутствие человека в космосе'
if args.rides:
    HIGHEST_NUM = rides_nums[-1]
    YLIM_TOP_MARGIN = 50
    ax.plot(dates, rides_nums, '.b', label='Количество посещений', ms=6)
elif not args.rides and args.evas:
    HIGHEST_NUM = evanums[-1]
    SH, SH2 = 9, 160
elif not args.rides and not args.evas and args.astros:
    HIGHEST_NUM = flight_nums[-1]
    SH, SH2 = 6, 102
elif not args.rides and not args.evas and not args.astros and args.flights:
    HIGHEST_NUM = flights_nums[-1]
    SH, SH2 = 2, 64
    TITLE = 'Количество космических полетов'
YLIM = HIGHEST_NUM + YLIM_TOP_MARGIN
if args.evas:
    ax.plot(evadates, evanums, '.', label='Количество ВКД', color="brown", ms=6)
if args.astros:
    ax.plot(flight_dates, flight_nums, '.k', label='Количество астронавтов', ms=6)
if args.flights:
    ax.plot(dates, flights_nums, '.m', label='Количество космических полетов', ms=6)


accidents = [
    (1961, 3, 23, 'Пожар, гибель В.В. Бондаренко', SH, -TM_SHIFT),
    (1967, 1, 27, 'Пожар на «Аполлоне-1»', SH, TM),
    (1967, 4, 23, 'Гибель Комарова, нераскрытие парашюта «Союза-1»', SH, -2.9*TM_SHIFT),
    (1967, 11, 15, 'X-15, гибель М.Д. Адамса', SH, -TM_SHIFT*3.9),
    (1971, 6, 29, 'Разгерметизация «Союза-11»', SH, TM),
    (1980, 3, 18, 'Катастрофа на космодроме Плесецк', SH, TM),
    (1986, 1, 28, 'Катастрофа «Челленджера»', SH2, TM),
    (2003, 2, 1, 'Катастрофа «Колумбии»', SH, TM)]
private_spaceflights = [(2001, 4, 28, 'Деннис Тито', SH2, TM),
    (2020, 5, 30, 'SpaceX DM-2', SH2-10, TM), (2021, 7, 11, 'VG Unity 22/NS-16', SH2-10, TM),
    (2021, 7, 20, '', SH, TM), (2021, 9, 16, 'Inspirati④n', SH2-10, -TM_SHIFT)]

for ac in accidents:
    dat = datetime(year=ac[0], month=ac[1], day=ac[2])
    plt.plot((dat, dat), (0, HIGHEST_NUM+YLIM_TOP_MARGIN), '--r')
    ax.text(dat-ac[5], YLIM-ac[4], ac[3], rotation='vertical', va="top", fontsize=14)
for ac in private_spaceflights:
    dat = datetime(year=ac[0], month=ac[1], day=ac[2])
    plt.plot((dat, dat), (0, HIGHEST_NUM+YLIM_TOP_MARGIN), '--g')
    ax.text(dat-ac[5], YLIM-ac[4], ac[3], rotation='vertical', va="top", fontsize=14)

ax.set_xlim(dates[0]-tdlt, dates[-1]+tdlt) # datetime(2060, 1, 1)
ax.set_ylim(-3, HIGHEST_NUM+YLIM_TOP_MARGIN) # 2500
ax.legend(fontsize=13, loc='upper center')

plt.title(f'{TITLE}. Всего {orb_num} орбитальных и ' + \
    f'{suborb_num} суборбитальных полетов, {flight_nums[-1]} астронавтов, ' + \
    f'{evanums[-1]} ВКД и {rides_nums[-1]} посещений. {MONTH} {YEAR} года')
plt.xlabel('Время, годы', fontsize=14)
plt.ylabel('Количество', fontsize=14)
plt.grid(linestyle='dotted')

FILENAME = f"manned{'flights' if args.flights else ''}{'-astronauts' if args.astros else ''}" + \
    f"{'-rides' if args.rides else ''}{'-evas' if args.evas else ''}"

FILE_EXT = 'svg'
plots_dir = os.path.join(os.pardir, os.pardir, os.pardir, 'plots', 'manned')
tmp_pth = os.path.join(plots_dir, FILENAME+'_.'+FILE_EXT)
pth = os.path.join(plots_dir, FILENAME+'.'+FILE_EXT)
plt.savefig(tmp_pth, dpi=240)

if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)


# SECOND PLOT

fig, bx = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.94, 0.97)
years = mdates.YearLocator(5)
bx.xaxis.set_major_locator(years)
bx.xaxis.set_minor_locator(mdates.YearLocator())
bx.yaxis.set_major_locator(MultipleLocator(25))

tdlt = timedelta(days=300)
plt.xlim(evadates[0]-tdlt, evadates[-1]+tdlt)
plt.plot(evadates, evatds, 'ok', label='Суммарная длительность ВКД', ms=3)
plt.grid(linestyle='dotted')

plt.title(f'Полная длительность ВКД, {round(evas_total_time.total_seconds()/86400, 1)}' + \
          f' суток в {len(evadates)} выходах. {MONTH} {YEAR} года')
bx.set_xlabel('Время, годы', fontsize=14)
bx.set_ylabel('Суммарная длительность ВКД, сутки', fontsize=14)
plt.grid(linestyle='dotted')

if args.counts:
    bx2 = bx.twinx()
    bx2.plot(evadates, evanums, '.', label='Количество ВКД', color="brown", ms=6)
    bx.set_ylim(bottom=-0.7)
    bx2.set_ylim(bottom=-1.5)
    bx2.set_ylabel('Количество ВКД', fontsize=14)
    bx2.set_facecolor("none")

handles, labels = unite_legends([bx, bx2])
bx.legend(handles, labels, loc='upper left', fontsize=13)

FILENAME = f"evas-total-time{'-counts' if args.counts else ''}"
FILE_EXT = 'svg'
tmp_pth = os.path.join(plots_dir, FILENAME+'_.'+FILE_EXT)
pth = os.path.join(plots_dir, FILENAME+'.'+FILE_EXT)
plt.savefig(tmp_pth, dpi=240)

if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
