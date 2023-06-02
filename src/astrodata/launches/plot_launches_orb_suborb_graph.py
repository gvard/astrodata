"""Python script for plotting graph with rocket launches statistics.
Data taken from General Catalog of Artificial Space Objects
by Jonathan C. McDowell: https://planet4589.org/space/gcat/web/launch/
Event Catalogs, Deep Space Catalog: https://planet4589.org/space/gcat/web/cat/
Data products: plots with 1) suborbital launches and 2) deep space launches.
"""

from datetime import datetime, timedelta
import os
import locale
import urllib.request
from argparse import ArgumentParser

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scour import scour


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


parser = ArgumentParser(description='Graph plotter script with number of rocket launches')
parser.add_argument('-v', '--verbose', action='store_true', help='Print additional information')
parser.add_argument('-d', '--deep', action='store_true', help='Plot launches to deep space')
parser.add_argument('-a', '--savelist', action='store_true',
    help='Save list of deep space launches to file')
parser.add_argument('-o', '--orbital', action='store_true',
    help='Plot number of suborbital launches')
parser.add_argument('-f', '--failed', action='store_true', help='Plot number of failed launches')
parser.add_argument('-m', '--marginal', action='store_true',
    help='Plot number of marginal launches')
parser.add_argument('-s', '--suborb', action='store_true',
    help='Plot number of suborbital launches')
parser.add_argument('-l', '--local', action='store_true', help='Use local files')
parser.add_argument('-e', '--height', type=int, default=100,
    help='Set apogee height in km for suborbital launches. Default is 100 km')

args = parser.parse_args()

BASE_URL = 'https://planet4589.org/space/gcat/data/'
LISTS_DIR = 'ldes/'
MS = 3
nums, nums_fail, nums_marg, nums_deep, so_nums = [], [], [], [], []
if args.orbital:
    DATA_URL = BASE_URL + LISTS_DIR + "O.html"
    data = get_table(DATA_URL)[1:]
    dates, nums = get_data_array(data)
    print("Orbital launches:", len(dates))
if args.failed:
    DATA_URL = BASE_URL + LISTS_DIR + "F.html"
    data = get_table(DATA_URL)[1:]
    dates_fail, nums_fail = get_data_array(data)
    print("Launches failed:", len(dates_fail))
if args.marginal:
    DATA_URL = BASE_URL + LISTS_DIR + "U.html"
    data = get_table(DATA_URL)[1:]
    dates_marg, nums_marg = get_data_array(data)
    print("Marginal launches:", len(dates_marg))
if args.suborb:
    if args.verbose:
        print('Plot suborb graph')
    FILE_EXT = 'svg'
    MS = 5
    DATA_URL = BASE_URL + LISTS_DIR + "S.html"
    if args.local:
        DATA_URL = '../../../data/S.html'
    suborb_data = get_table(DATA_URL, local=args.local)[1:]
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
        except ValueError:
            no_altitude += 1
            continue
        if line and line[35:37].strip() and apo and int(apo) >= args.height:
            if line[37] == '?' or line[38] == ' ':
                dat = datetime.strptime(line[26:37], '%Y %b %d')
            else:
                dat = datetime.strptime(line[26:42], '%Y %b %d %H%M')
            so_heights.append(apo)
            so_dates.append(dat)
            so_launches_num += 1
            so_nums.append(so_launches_num)
    print(f"No apogee altitude data for {no_altitude} entries, {qm} questioned")
    print("Suborbital launches:", len(so_dates))

if args.deep:
    FILE_EXT = 'svg'
    DATA_URL = BASE_URL + 'cat/deepcat.html'
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

    if args.savelist:
        DEEP_FILENAME = 'deepcat.txt'
        with open(DEEP_FILENAME, 'w', encoding='utf-8') as f:
            for dat, space_objects_lst in unique_dtes.items():
                print(str(dat.date()), space_objects_lst, file=f)
        print("Deep space launches list saved to", DEEP_FILENAME)

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

TITLE = 'Рост числа ракетных запусков. Всего '
if args.suborb:
    plt.plot(so_dates, so_nums, '.k',
        label=f'Каталогизированные суборбитальные запуски (апогей от {args.height} км)', ms=5)
    ylim = (-35 if args.height<86 else -21, so_nums[-1]+500 if args.height<86 else so_nums[-1]+312)
    plt.ylim(ylim)
    TITLE = 'Рост числа запусков в космос. Всего '
if args.orbital:
    plt.plot(dates, nums, '.b', label='Орбитальные ракетные запуски', ms=MS)
if args.failed:
    plt.plot(dates_fail, nums_fail, '.r', label='Неудачные попытки', ms=MS)
if args.deep:
    plt.plot(dates_deep, nums_deep, '.k', label='Запуски в глубокий космос', ms=6)
    plt.ylim(-5, nums_deep[-1]+190)
if args.marginal:
    plt.plot(dates_marg, nums_marg, '.g', label='Граничные запуски', ms=MS) #ms=2
ORB_TITL = f'{len(nums)} орбитальных запусков, ' if nums else ''
FAILD_TITL = f'{len(nums_fail)} неудач, ' if nums_fail else ''
MARG_TITL = f'{len(nums_marg)} граничных запусков, ' if nums_marg else ''
DEEP_TITL = f'{len(nums_deep)} запусков в глубокий космос' if nums_deep else ''
SUBORB_TITL = f'{len(so_nums)} суборбитальных запусков' if so_nums else ''
xlim = (dates[0]-tdlt, dates[-1]+tdlt) if args.deep and args.orbital else \
       (datetime(1942, 8, 5), so_dates[-1]+tdlt)
plt.xlim(xlim)
plt.title(f'{TITLE}{ORB_TITL}{FAILD_TITL}{MARG_TITL}{DEEP_TITL}{SUBORB_TITL}. {MONTH} {YEAR} года')
plt.legend(fontsize=13)
plt.xlabel('Время, годы', fontsize=14)
plt.ylabel('Количество запусков', fontsize=12)
plt.grid(linestyle='dotted')

ORB_POSTFIX = "-orb" if args.orbital else ""
SUBORB_POSTFIX = f"-suborb-{args.height}km" if args.suborb else ""
DEEP_POSTFIX = "-deep" if args.deep else ""
FILENAME = f'launches{ORB_POSTFIX}{DEEP_POSTFIX}{SUBORB_POSTFIX}'
plots_dir = os.path.join(os.pardir, os.pardir, os.pardir, 'plots', 'launches')
tmp_pth = os.path.join(plots_dir, FILENAME+'_.'+FILE_EXT)
pth = os.path.join(plots_dir, FILENAME+'.'+FILE_EXT)
plt.savefig(tmp_pth, dpi=120)

if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
