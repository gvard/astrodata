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

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scour import scour


def optimize_svg(tmp_pth, pth):
    """Optimize svg file with scour (use pip to install it)."""
    with open(tmp_pth, 'rb') as inputfile, open(pth, 'wb') as outputfile:
        options = scour.generateDefaultOptions()
        options.enable_viewboxing = True
        options.strip_comments = True
        options.strip_ids = True
        options.remove_metadata = True
        options.indent_type = 'none'
        options.shorten_ids = True
        scour.start(options, inputfile, outputfile)

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
evadates, evanums = [], []
astro_num = 0
for line in data:
    if line:
        dd = datetime.strptime(line[170:186], '%Y %b %d %H%M')
        evadates.append(dd)
        astro_num += 1
        evanums.append(astro_num)


fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)
years = mdates.YearLocator(5)
oneyear = mdates.YearLocator()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(oneyear)

tdlt = timedelta(days=630)

locale.setlocale(locale.LC_ALL, 'ru_RU')
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year

# Graph settings
nums, ylim_top_margin, FILENAME = rides_nums, 50, "mannedflights-astronauts-rides-evas_"
# nums, ylim_top_margin, FILENAME = rides_nums, 50, "mannedflights-rides"
# nums, ylim_top_margin, FILENAME = flights_nums, 15, "mannedflights"
# nums, ylim_top_margin, FILENAME = flight_nums, 15, "mannedflights-astronauts"
# nums, ylim_top_margin, FILENAME = evanums, 15, "mannedflights-evas"


accidents = [(1967, 1, 27), (1967, 4, 23), (1971, 6, 29), (1986, 1, 28),
    (2003, 2, 1)]
private_spaceflights = [(2001, 4, 28), (2020, 5, 30), (2021, 7, 11),
    (2021, 7, 20), (2021, 9, 16)]

for ac in accidents:
    dat = datetime(year=ac[0], month=ac[1], day=ac[2])
    plt.plot((dat, dat), (0, nums[-1]+ylim_top_margin), '--r')
for ac in private_spaceflights:
    dat = datetime(year=ac[0], month=ac[1], day=ac[2])
    plt.plot((dat, dat), (0, nums[-1]+ylim_top_margin), '--g')

plt.plot(dates, nums, '.b', label='Количество посещений', ms=6)
plt.plot(evadates, evanums, '.', label='Количество ВКД', color="brown", ms=6)
plt.plot(flight_dates, flight_nums, '.k', label='Количество астронавтов', ms=6)
plt.plot(dates, flights_nums, '.m', label='Количество космических полетов', ms=6)
plt.xlim(dates[0]-tdlt, dates[-1]+tdlt)
plt.ylim(0, nums[-1]+ylim_top_margin)
plt.legend(fontsize=13)

# plt.title(f'Количество космических полетов. Всего {orb_num} орбитальных и ' + \
# plt.title(f'Число астронавтов. Всего {orb_num} орбитальных и ' + \
# plt.title(f'Количество посещений. Всего {orb_num} орбитальных и ' + \
plt.title(f'Присутствие человека в космосе. Всего {orb_num} орбитальных и ' + \
    f'{suborb_num} суборбитальных полетов, {flight_nums[-1]} астронавтов, ' + \
    f'{evanums[-1]} ВКД и {rides_nums[-1]} посещений. {MONTH} {YEAR} года')
plt.xlabel('Время, годы', fontsize=14)
plt.ylabel('Количество полетов астронавтов', fontsize=14)
plt.grid(linestyle='dotted')

FILE_EXT = 'svg'
plots_dir = os.path.join(os.pardir, os.pardir, os.pardir, 'plots', 'manned')
tmp_pth = os.path.join(plots_dir, FILENAME+'_.'+FILE_EXT)
pth = os.path.join(plots_dir, FILENAME+'.'+FILE_EXT)
plt.savefig(tmp_pth, dpi=240)

if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
