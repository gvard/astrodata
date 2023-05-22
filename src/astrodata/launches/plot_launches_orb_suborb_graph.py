"""Python script for plotting graph with rocket launches statistics.
Data taken from General Catalog of Artificial Space Objects
by Jonathan C. McDowell: https://planet4589.org/space/gcat/web/launch/
Event Catalogs, Deep Space Catalog: https://planet4589.org/space/gcat/web/cat/
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

def get_data_array_deep(data, date_col=(106, 117), sort=True):
    """Parse ASCII data of launch lists.
    TODO: merge with parser for suborbital list.
    """
    dates = []
    nnas = 0
    for line in data:
        satcat = line[13:18].strip()
        if satcat[:3] ==  "NNA":
            nnas += 1
            #continue
        if line:
            name = line[48:76].strip()
            ldate = datetime.strptime(line[date_col[0]:date_col[1]], '%Y %b %d')
            dates.append([ldate, name, satcat])
    print("No satellite cat entry for", nnas, "deepcat entries")
    if sort:
        dates.sort(key=lambda row: row[0])
    return dates


BASE_URL = "https://planet4589.org/space/gcat/data/ldes/"
SUBORB_POSTFIX, DEEP_POSTFIX = "", ""

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

SUBORB = False
DEEP = True

if SUBORB:
    FILE_EXT = 'png'
    MS = 5
    L_ORDER = [3, 1, 2, 0]
    SUBORB_POSTFIX = "-suborb-100km"
    DATA_URL = BASE_URL + "S.html" # DATA_URL = "S.html"
    suborb_data = get_table(DATA_URL, local=False)[1:] # local=True
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

if DEEP:
    FILE_EXT = 'svg'
    MS = 3
    L_ORDER = [1, 2, 3, 0]
    DEEP_POSTFIX = "-deep"
    DATA_URL = "https://planet4589.org/space/gcat/data/cat/deepcat.html"
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

    SAVE_LIST = False
    if SAVE_LIST:
        with open('deepcat.txt', 'w', encoding='utf-8') as f:
            for dat, space_objects_lst in unique_dtes.items():
                print(str(dat.date()), space_objects_lst, file=f)

    dates_deep = list(unique_dtes.keys())
    nums_deep = range(1, len(dates_deep) + 1)
    print("Deep space objects:", len(dates_deep))


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

plt.plot(dates_marg, nums_marg, '.g', label='Граничные запуски', ms=MS) #ms=2
plt.plot(dates, nums, '.b', label='Орбитальные ракетные запуски', ms=MS)
plt.plot(dates_fail, nums_fail, '.r', label='Неудачные попытки', ms=MS)
if SUBORB:
    plt.plot(so_dates, so_nums, '.k',
    label='Каталогизированные суборбитальные запуски (апогей от 100 км)', ms=5)
    plt.xlim(so_dates[0]-tdlt, so_dates[-1]+tdlt)
    plt.ylim(-25, so_nums[-1]+500)
    plt.title(f'Рост числа суборбитальных и орбитальных запусков. Всего {len(dates)} ' + \
    f'орбитальных запусков, {len(nums_fail)} неудач и {len(so_nums)} суборбитальных запусков. {MONTH} {YEAR} года')
if DEEP:
    plt.plot(dates_deep, nums_deep, '.k', label='Запуски в глубокий космос', ms=6)
    plt.xlim(dates[0]-tdlt, dates[-1]+tdlt) #+5*tdlt
    plt.ylim(-5, nums_deep[-1]+190)
    plt.title(f'Рост числа запусков в глубокий космос. Всего {len(dates)} ' + \
    f'орбитальных запусков, {len(nums_fail)} неудач, {len(nums_deep)} запусков в глубокий космос. {MONTH} {YEAR} года')

handles, labels = plt.gca().get_legend_handles_labels()
plt.legend([handles[idx] for idx in L_ORDER],[labels[idx] for idx in L_ORDER], fontsize=13)
plt.xlabel('Время, годы', fontsize=14)
plt.ylabel('Количество запусков', fontsize=12)
plt.grid(linestyle='dotted')

FILENAME = f'launches-orb{DEEP_POSTFIX}{SUBORB_POSTFIX}'
plots_dir = os.path.join(os.pardir, os.pardir, os.pardir, 'plots', 'launches')
tmp_pth = os.path.join(plots_dir, FILENAME+'_.'+FILE_EXT)
pth = os.path.join(plots_dir, FILENAME+'.'+FILE_EXT)
plt.savefig(tmp_pth, dpi=120)

if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
