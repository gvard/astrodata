"""Script for plotting chart with number of variable stars.
Data sources:
General Catalogue of Variable Stars (Samus+, 2007-2017)
https://cdsarc.u-strasbg.fr/ftp/B/gcvs/ReadMe
General catalogue of variable stars: Version GCVS 5.1, 2017ARep...61...80S
The 84th Name-List of Variable Stars. Globular Clusters (Third Part) and Novae, 2021PZ.....41....7S
http://www.astronet.ru/db/varstars/msg/eid/PZ-41-007
General Catalog of Variable Stars, 4th Ed. (GCVS4, Kholopov et al. 1985-1988): II/139B
The fourth edition of the General Catalogue of Variable Stars supersedes the third edition
(Kukarkin et al. 1969-1970: 20437 objects including 148 constant ones, resulting
20289 variables), three supplements (Kukarkin et al. 1971, 1974, 1976) containing
data for 5401 new variable stars and improved data for many earlier designated variables,
and five namelists (62-66) published in the Information Bulletin of Variable Stars
(Kukarkin et al. 1976; Kholopov et al. 1978, 1979, 1981a, 1981b), which included
only cross identifications for 2619 new variables.
https://cdsarc.cds.unistra.fr/viz-bin/cat/II/139B
The Combined General Catalogue of Variable Stars, 4.1 Edition.
General Catalogue of Variable Stars 4th Edition, Volumes I-III, (1998)
https://cdsarc.cds.unistra.fr/viz-bin/cat/II/214A
Combined General Catalog of Variable Stars (GCVS4.2, 2004 Ed.) (2004)
https://cdsarc.cds.unistra.fr/viz-bin/cat/II/250
General Catalog of Variable Stars (GCVS database, Version 2013 Apr.)
http://www.sai.msu.su/gcvs/gcvs/iii/html/
The International Variable Star Index (VSX)
Watson+: 2006SASS...25...47W, 2007JAVSO..35..414W, 2015yCat....102027W
https://cdsarc.u-strasbg.fr/ftp/B/vsx/ReadMe
Estimation of the number of variable stars based on Kepler data (94/150): 2011AJ....141...20B
Estimation of variable sources: 1590800000 Gaia DR3 Sources with object classifications,
6650000 QSO candidates, over 0.87 million variable AGN (about 88% quasars are variable),
4842000 Galaxy candidates, 158152 Solar system objects."""

from datetime import datetime, timedelta
import os
import urllib.request
import locale

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scour import scour

from transients import get_soup_request


def retrieve(url, path):
    """Retrieve file, set Last-Modified date"""
    local_filename, headers = urllib.request.urlretrieve(url, path)
    if 'Last-Modified' in headers:
        lastmod = datetime.strptime(headers['Last-Modified'],
            '%a, %d %b %Y %H:%M:%S GMT').timestamp()
        os.utime(local_filename, (lastmod, lastmod))

def get_vsx_readme_updates(readme, nums=(124, 29)):
    """Get number of sources from ReadMe file of VSX cat."""
    vsx_up_nums = []
    up_dates = []
    for line in readme[nums[0]:-2]:
        line = line.decode()
        if line[16] == 'O':
            numstart = nums[1]
        elif line[16] == ' ':
            numstart = 28
        else:
            numstart = 16
        num = line[numstart:].split()[0]
        try:
            vsx_up_nums.append(int(num) / 1000)
            dat = datetime.strptime(line[4:14], '%Y-%m-%d')
            up_dates.append(dat)
        except ValueError:
            pass
    return up_dates, vsx_up_nums

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


VSX_README_URL = "https://cdsarc.u-strasbg.fr/ftp/B/vsx/ReadMe"
VSX_DATA_URL = "https://www.aavso.org/vsx/external/vsx_csv.dat.gz"
DATA_PTH = '../../../data/'
PLOT_PTH = '../../../plots/stars/'
GCVS_DATA_URL = 'http://www.sai.msu.su/gcvs/gcvs/gcvs5/gcvs5.txt'
# retrieve(GCVS_DATA_URL, DATA_PTH+'gcvs5.txt')
GCVS_DATA_URL = 'https://cdsarc.cds.unistra.fr/ftp/B/gcvs/gcvs_cat.dat.gz'
# retrieve(GCVS_DATA_URL, DATA_PTH+'gcvs_cat.dat.gz')
GCVS_README_URL = 'https://cdsarc.cds.unistra.fr/ftp/B/gcvs/ReadMe'
# retrieve(GCVS_README_URL, DATA_PTH+'gcvs/ReadMe')
# retrieve(VSX_README_URL, DATA_PTH+'ReadMe')
# retrieve(VSX_DATA_URL, DATA_PTH+'vsx_csv.dat.gz')
FILE_EXT = 'svg'
locale.setlocale(locale.LC_ALL, 'ru_RU')
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year

with urllib.request.urlopen(VSX_README_URL) as readme_lines:
    vsx_dates, vsx_nums = get_vsx_readme_updates(readme_lines.readlines())
soup = get_soup_request('https://www.aavso.org/vsx/')
vsx_vars = int(soup.findAll('table')[1].findAll('td')[5].find('b').text.replace(',', ''))
vsx_dates.append(today)
vsx_nums.append(vsx_vars/1000)

gcvs_dates = [datetime.strptime(x, '%Y-%m-%d') for x in
             ['1948-01-01', '1958-01-01', '1968-01-01', '1982-01-01', '1998-01-01',
              '2004-01-01', '2009-06-07', '2011-04-03', '2012-02-26', '2013-04-30',
              '2016-12-31', '2018-09-17', '2020-07-06', '2022-03-31']]
gcvs_nums = [10.762, 14.569, 20.289, 28.484, 31.918, 38.624, 41.639,
             43.675, 45.835, 47.969, 52.011, 52.011, 54.979, 58.202]
gcvs_dates.append(today)
gcvs_nums.append(gcvs_nums[-1])

fig, ax = plt.subplots(figsize=(16, 9))
plt.ylim(0, vsx_nums[-1] + 60)
td = timedelta(days=60)
plt.xlim(vsx_dates[0]-td, today+td)
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.97, top=0.955)
plt.plot(vsx_dates, vsx_nums, '.r--', label="AAVSO International Variable Star Index")
plt.plot(gcvs_dates, gcvs_nums, 'ob--', label="Общий Каталог Переменных Звезд")
plt.plot([datetime(2021, 11, 26)], [58.035], '*g', ms=12,
         label='Именованные переменные звезды в ОКПЗ, 58035 звезд')
plt.plot([datetime(2023, 6, 4)], [124.100], '*k', ms=12,
         label='Транзиенты и вспышки сверхновых, >121700 вспышек и >124100 транзиентов')
plt.title(f'Количество переменных звезд. Всего {vsx_vars} звезд в VSX, ' + \
          f'{round(vsx_vars/9948644.04, 2)}% переменных звезд исследовано. ' + \
          f'{MONTH} {YEAR} года', fontsize=16)
plt.xlabel('Год', fontsize=14)
plt.ylabel('Количество переменных звезд (тысяч)', fontsize=14)
plt.legend(fontsize=14)
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.yaxis.set_minor_locator(MultipleLocator(250))
plt.grid(axis='y', which='major', linestyle='--')
plt.grid(axis='y', which='minor', linestyle=':')
plt.grid(axis='x', which='major', linestyle=':')

TMP_PTH = PLOT_PTH+'variable-stars-count-graph_.' + FILE_EXT
plt.savefig(TMP_PTH, dpi=120)
if FILE_EXT == 'svg':
    optimize_svg(TMP_PTH, PLOT_PTH+'variable-stars-count-graph.svg')
    os.remove(TMP_PTH)

fig, ax = plt.subplots(figsize=(16, 9))
plt.ylim(0, 60)
td = timedelta(weeks=60)
plt.xlim(gcvs_dates[0]-td, today+td)
plt.subplots_adjust(left=0.06, bottom=0.06, right=0.97, top=0.955)
plt.plot(gcvs_dates, gcvs_nums, 'ob--', label="Общий Каталог Переменных Звезд")
plt.plot([datetime(2021, 11, 26)], [58.035], '*r', ms=12,
         label='Именованные переменные звезды в ОКПЗ, 58035 звезд')
plt.title(f'Количество переменных звезд. Всего {vsx_vars} звезд в VSX, ' + \
          f'{round(vsx_vars/9948644.04, 2)}% переменных звезд исследовано. ' + \
          f'{MONTH} {YEAR} года', fontsize=16)
plt.xlabel('Год', fontsize=14)
plt.ylabel('Количество переменных звезд (тысяч)', fontsize=14)
plt.legend(fontsize=14)
ax.xaxis.set_major_locator(mdates.YearLocator(5))
ax.xaxis.set_minor_locator(mdates.YearLocator(1))
ax.yaxis.set_minor_locator(MultipleLocator(2))
plt.grid(axis='y', which='major', linestyle='--')
plt.grid(axis='x', which='major', linestyle=':')

FNAME = 'gcvs-variable-stars-count-graph'
TMP_PTH = f'{PLOT_PTH}{FNAME}_.{FILE_EXT}'
plt.savefig(TMP_PTH, dpi=120)
if FILE_EXT == 'svg':
    optimize_svg(TMP_PTH, f'{PLOT_PTH}{FNAME}.{FILE_EXT}')
    os.remove(TMP_PTH)
