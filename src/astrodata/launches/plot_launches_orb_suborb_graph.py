"""Python script for plotting graph with rocket launches statistics.
Data taken from General Catalog of Artificial Space Objects
by Jonathan C. McDowell: https://planet4589.org/space/gcat/web/launch/
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

def get_table(url, local=False):
    """Read ASCII data table from pre html element"""
    if local:
        html = open(url, encoding='utf-8')
    else:
        html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup.findAll('pre')[1].text.splitlines()

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
                dat = datetime.strptime(line[date_col[0]:date_col[1]], '%Y %b %d %H%M')
            except ValueError:
                dat = datetime.strptime(line[date_col[0]:date_col[1]-4], '%Y %b %d')
            dates.append(dat)
            launches_num += 1
            nums.append(launches_num)
    print("No apogee altitude data for", no_altitude, "entries")
    return dates, nums


BASE_URL = "https://planet4589.org/space/gcat/data/ldes/"

DATA_URL = BASE_URL + "O.html"
data = get_table(DATA_URL)[1:]
dates, nums = get_data_array(data)
print("Orbital launches:", len(dates))

DATA_URL = BASE_URL + "F.html"
data = get_table(DATA_URL)[1:]
dates_fail, nums_fail = get_data_array(data)
print("Launches failed:", len(dates_fail))

DATA_URL = BASE_URL + "U.html"
data = get_table(DATA_URL)[1:]
dates_marg, nums_marg = get_data_array(data)
print("Marginal launches:", len(dates_marg))

SUBORB = True
if SUBORB:
    DATA_URL = BASE_URL + "S.html"
    DATA_URL = "S.html"
    suborb_data = get_table(DATA_URL, local=True)[1:]
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
            if line and line[35:37].strip() and apo and int(apo) >= 100:
                apo = int(apo)
                try:
                    dat = datetime.strptime(line[26:41], '%Y %b %d %H%M')
                except ValueError:
                    dat = datetime.strptime(line[26:37], '%Y %b %d')
                so_heights.append(apo)
                so_dates.append(dat)
                so_launches_num += 1
                so_nums.append(so_launches_num)
        except ValueError:
            no_altitude += 1
    print(f"No apogee altitude data for {no_altitude} entries, {qm} questioned")
    print("Suborbital launches:", len(so_dates))


fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)
years = mdates.YearLocator(5)
oneyear = mdates.YearLocator()
ax.xaxis.set_major_locator(years)
ax.xaxis.set_minor_locator(oneyear)

if SUBORB:
    plt.plot(so_dates, so_nums, '.k',
    label='Каталогизированные суборбитальные запуски (апогей от 100 км)', ms=5)
plt.plot(dates, nums, '.b', label='Орбитальные ракетные запуски', ms=5)
plt.plot(dates_fail, nums_fail, '.r', label='Неудачные попытки', ms=5)
plt.plot(dates_marg, nums_marg, '.g', label='Граничные запуски', ms=5)

tdlt = timedelta(days=630)
locale.setlocale(locale.LC_ALL, 'ru_RU')
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year

plt.xlim(so_dates[0]-tdlt, so_dates[-1]+tdlt)
plt.ylim(-25, so_nums[-1]+500) # +100
plt.legend(fontsize=13)

plt.title(f'Рост числа суборбитальных и орбитальных запусков. Всего {len(dates)} ' + \
    f'орбитальных запусков и {len(nums_fail)} неудач. {MONTH} {YEAR} года')
plt.xlabel('Время, годы', fontsize=14)
plt.ylabel('Количество запусков', fontsize=12)
plt.grid(linestyle='dotted')

FILENAME = 'launches-orb-suborb-100km'
FILE_EXT = 'png'
plots_dir = os.path.join(os.pardir, os.pardir, os.pardir, 'plots', 'launches')
tmp_pth = os.path.join(plots_dir, FILENAME+'_.'+FILE_EXT)
pth = os.path.join(plots_dir, FILENAME+'.'+FILE_EXT)
plt.savefig(tmp_pth, dpi=120)

if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
