"""Script for plotting a bar chart with types of variable stars that are members
of clusters, presented in Hunt+, 2023 (Improving the open cluster census. II.
An all-sky cluster catalogue with Gaia DR3, file J/A+A/673/A114/members, 1291929 rows)
Data sources:
https://cdsarc.cds.unistra.fr/viz-bin/cat/J/A+A/673/A114
The current versions of the AAVSO International Variable Star Index
(VSX, file B/vsx/vsx, 2277328 rows) and
the General Catalog of Variable Stars (GCVS, file B/gcvs/gcvs_cat, 58200 rows).
https://cdsarc.cds.unistra.fr/viz-bin/cat/B/vsx
https://cdsarc.cds.unistra.fr/viz-bin/cat/B/gcvs
"""

from datetime import datetime
import locale
import os

import matplotlib.pyplot as plt
import pandas as pd
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

CAT, CAT_RU, NUM_SEC, BOTMAR = 'gcvs', 'ОКПЗ', '1', 0.102 #0.084
# CAT, CAT_RU, NUM_SEC, BOTMAR = 'gcvs', 'ОКПЗ', '2', 0.102 #0.084
# CAT, CAT_RU, NUM_SEC, BOTMAR = 'vsx', 'VSX', '1', 0.102
# CAT, CAT_RU, NUM_SEC, BOTMAR = 'vsx', 'VSX', '2', 0.102
TYPE_COL = 'VarType' if CAT == 'gcvs' else 'Type'
data = pd.read_csv(f'../../../data/hunt2023/xmatch_{CAT}_{NUM_SEC}s.csv', usecols=[TYPE_COL])
df = data[TYPE_COL].str.strip(':')
series = df.squeeze()
NUM = 36
df = series.value_counts()[NUM::-1]
ax = df.plot(kind='bar', figsize=(16, 9), width=0.88, rot=45) #, legend=False
locale.setlocale(locale.LC_ALL, 'ru_RU')
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year

print('Типы выборки:', df, 'их количество:', len(df), 'всего типов в статистике:',
      len(series.value_counts()), 'всего звезд в каталоге:', len(data))

plt.subplots_adjust(left=0.051, bottom=BOTMAR, right=0.985, top=0.955)
plt.xlabel('Типы переменных звезд', fontsize=14, labelpad=0)
plt.ylabel('Количество переменных звезд', fontsize=14)
plt.title(f'Распределение по типам переменных звезд {CAT_RU} в каталоге скоплений' + \
    f' Hunt, 2023. Всего {len(data)} звезд в выборке. {MONTH} {YEAR} года', fontsize=15)
plt.legend([f'Переменные звезды скоплений из {CAT_RU}, кросс-корреляция с радиусом {NUM_SEC}"'],
           fontsize=14, loc='upper left')
ax.bar_label(ax.containers[-1])

FILE_EXT = 'png'
PAR_DIR = '../../../plots/stars/'
PLT_PTH = f'{PAR_DIR}{CAT}_types_distribution-xmatch-hunt2023-{NUM_SEC}s-combined-sorted-latest'
tmp_pth = f'{PLT_PTH}_.{FILE_EXT}'
pth = f'{PLT_PTH}.{FILE_EXT}'
plt.savefig(tmp_pth, dpi=120)
if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
