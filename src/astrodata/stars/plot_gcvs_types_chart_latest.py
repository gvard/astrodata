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
    with open(tmp_path, "rb") as inputfile, open(path, "wb") as outputfile:
        options = scour.generateDefaultOptions()
        options.enable_viewboxing = True
        options.strip_comments = True
        options.strip_ids = True
        options.remove_metadata = True
        options.shorten_ids = True
        options.indent_type = "none"
        options.newlines = False
        scour.start(options, inputfile, outputfile)

def read_gcvs_cat_types(cat, splt_char="+", strip=True):
    """Read GCVS file, get each type of variable star, count them,
    merge with uncertainly defined types if strip == True, collect in dict.
    According to GCVS Variability Types description, if a variable belongs to several
    types of variability, the types are joined in the data field by a "+" sign, e.g.,
    E+UG, UV+BY. We collect them separatly in additional data array.
    if not splt_char, types_splt_dct will be empty.
    """
    types_dct = {}
    types_splt_dct = {}
    for line in cat:
        typ = line[41:51].strip()
        if strip:
            typ = typ.strip(":")
        if splt_char and splt_char in typ:
            for typsplit in typ.split(splt_char):
                if strip:
                    typsplit = typsplit.strip(":")
                try:
                    types_splt_dct[typsplit] += 1
                except KeyError:
                    types_splt_dct[typsplit] = 1
        try:
            types_dct[typ] += 1
        except KeyError:
            types_dct[typ] = 1
    return types_dct, types_splt_dct


SPLIT_CHAR = "+" # False
with open("../../../data/gcvs/gcvs5.txt", encoding="ascii") as gcvs:
    cat = gcvs.readlines()
    types_dct, types_splt_dct = read_gcvs_cat_types(cat, splt_char=SPLIT_CHAR)

locale.setlocale(locale.LC_ALL, "ru_RU")
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year
NUM = -37

# types_dct = dict(sorted(types_dct.items(), key=lambda x: x[1]))
most_numerous_types = list(types_dct.values())[NUM:]
most_numerous_types_names = list(types_dct.keys())[NUM:]
# splitted_types = list(types_dct.values())

df = pd.DataFrame({"gcvs": pd.Series(types_dct),
        "+": pd.Series(types_splt_dct)}).fillna(0).sort_values(by="gcvs")[NUM:]
# .sort_values(by="gcvs", ascending=False

print("Типы выборки:", most_numerous_types_names, "их количество:",
    len(most_numerous_types_names), "всего типов в статистике:",
    len(types_dct.keys()), "всего звезд в каталоге:", sum(types_dct.values()))

if SPLIT_CHAR:
    ax = df.plot.bar(stacked=True, figsize=(16, 9), width=0.88, rot=45)
    ax.legend(["Типы переменных звезд ОКПЗ",
               "Звезды с несколькими типами переменности"],
               fontsize=12, loc="upper left")
else:
    ax = df.plot.bar(stacked=True, figsize=(16, 9), width=0.88, rot=45, legend=False)

plt.subplots_adjust(left=0.051, bottom=0.102, right=0.985, top=0.955)
plt.xlabel("Типы переменных звезд", fontsize=14)
plt.ylabel("Количество переменных звезд", fontsize=14)
plt.title("Распределение по типам переменных звезд в текущей версии ОКПЗ, " + \
    f"всего {sum(types_dct.values())} объектов. {MONTH} {YEAR} года", fontsize=15)

for x, y in enumerate(df.sum(axis=1)):
    ax.annotate(int(y), (x, y+42), ha="center")
# ax.bar_label(ax.containers[-1])

FILE_EXT = "png"
PLT_PTH = "../../../plots/stars/gcvs_types_distribution-combined-sorted-latest+"
tmp_pth = f"{PLT_PTH}_.{FILE_EXT}"
pth = f"{PLT_PTH}.{FILE_EXT}"
plt.savefig(tmp_pth, dpi=120)
if FILE_EXT == "svg":
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
