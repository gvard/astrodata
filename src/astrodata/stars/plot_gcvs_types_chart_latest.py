"""Script for plotting a bar chart with types of variable stars in
the current version of the General Catalog of Variable Stars (GCVS).
Data source: http://www.sai.msu.su/gcvs/gcvs/gcvs5/gcvs5.txt
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

def read_gcvs_cat_types(cat):
    """Read GCVS file, get each type of variable star, count them,
    merge with uncertainly defined types, collect in dict.
    """
    types_dct = {}
    for line in cat:
        typ = line[41:51].strip().strip(':')
        try:
            types_dct[typ] += 1
        except KeyError:
            types_dct[typ] = 1
    return types_dct


with open('../../../data/gcvs/gcvs5.txt', encoding='ascii') as gcvs:
    cat = gcvs.readlines()
    types_dct = read_gcvs_cat_types(cat)

locale.setlocale(locale.LC_ALL, 'ru_RU')
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year

types_dct = dict(sorted(types_dct.items(), key=lambda x: x[1]))
NUM = -37
most_numerous_types = list(types_dct.values())[NUM:]
most_numerous_types_names = list(types_dct.keys())[NUM:]
data = {'Количество переменных звезд в ОКПЗ': most_numerous_types}
df = pd.DataFrame(data, index=most_numerous_types_names)
print('Типы выборки:', most_numerous_types_names, 'их количество:',
    len(most_numerous_types_names), 'всего типов в статистике:',
    len(types_dct.keys()), 'всего звезд в каталоге:', sum(types_dct.values()))

ax = df.plot(kind='bar', figsize=(16, 9), width=0.88, rot=45)

plt.subplots_adjust(left=0.04, bottom=0.09, right=0.985, top=0.955)
plt.xlabel('Типы переменных звезд', fontsize=14, labelpad=0)
plt.ylabel('Количество переменных звезд', fontsize=14, labelpad=0)
plt.title('Распределение по типам переменных звезд в текущей версии ОКПЗ. ' + \
    f'{MONTH} {YEAR} года', fontsize=16)
plt.legend(fontsize=14, loc='upper left')
ax.bar_label(ax.containers[-1])

FILE_EXT = 'svg'
PLT_PTH = '../../../plots/stars/gcvs_types_distribution-combined-sorted-latest'
tmp_pth = f'{PLT_PTH}_.{FILE_EXT}'
pth = f'{PLT_PTH}.{FILE_EXT}'
plt.savefig(tmp_pth, dpi=240)
if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
