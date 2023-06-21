"""Script for plotting a bar chart with types of variable stars in
the current version of the AAVSO International Variable Star Index (VSX).
Data source: https://cdsarc.cds.unistra.fr/viz-bin/cat/B/vsx
"""

from datetime import datetime
import locale
import os

from scour import scour
import matplotlib.pyplot as plt
import pandas as pd


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


data = pd.read_csv('../../../data/vsx/vsx_csv.dat', usecols=['Type'])
df = data['Type'].str.strip(':')
series = df.squeeze()
NUM = 36
df = series.value_counts()[NUM::-1]
ax = df.plot(kind='bar', figsize=(16, 9), width=0.88, rot=45, legend=False)

locale.setlocale(locale.LC_ALL, 'ru_RU')
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year

print('Типы выборки:', df, 'их количество:',
    len(df), 'всего типов в статистике:',
    len(series.value_counts()), 'всего звезд в каталоге:', len(data))

plt.subplots_adjust(left=0.051, bottom=0.09, right=0.985, top=0.955)
plt.xlabel('Типы переменных звезд', fontsize=14, labelpad=0)
plt.ylabel('Количество переменных звезд', fontsize=14, labelpad=0)
plt.title('Распределение по типам переменных звезд в текущей версии VSX. ' + \
    f'{MONTH} {YEAR} года', fontsize=16)
# plt.legend(fontsize=14, loc='upper left')
ax.bar_label(ax.containers[-1], fontsize=8)

FILE_EXT = 'svg'
PLT_PTH = '../../../plots/stars/vsx_types_distribution-combined-sorted-latest'
tmp_pth = f'{PLT_PTH}_.{FILE_EXT}'
pth = f'{PLT_PTH}.{FILE_EXT}'
plt.savefig(tmp_pth, dpi=240)
if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
