"""Script for plotting a bar chart with types of variable stars in
the current version of the General Catalog of Variable Stars (GCVS).
Data source: http://www.sai.msu.su/gcvs/gcvs/gcvs5/gcvs5.txt

According to GCVS Variability Types description,
http://www.sai.msu.su/gcvs/gcvs/vartype.htm
if a variable belongs to several types of variability, the types are joined
in the data field by a "+" sign, e.g., E+UG, UV+BY.
Multiple classifications for object types are separated by a solidus ("/").
We collect them separatly in additional data arrays.
Uncertainty on type of variability marked with a colon (:) is discarded for simplicity.
"""


import os

from scour import scour
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
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


def fill_dct(dct, typ):
    """Fill dictionary with given type name."""
    try:
        dct[typ] += 1
    except KeyError:
        dct[typ] = 1


types_dct = {}
types_plus = {}
types_slash = {}
STRIP = True

"""Read GCVS file, get each type of variable star, count them,
merge with uncertainly defined types if STRIP == True, collect in dictionaries.
"""
with open("../../../data/gcvs/gcvs5.txt", encoding="ascii") as gcvs:
    cat = gcvs.readlines()
    for line in cat:
        typ = line[41:51].strip()
        if STRIP:
            typ = typ.strip(":")
        if "+" in typ:
            for typsplit in typ.split("+"):
                if STRIP:
                    typsplit = typsplit.strip(":")
                fill_dct(types_plus, typsplit)
        if "/" in typ:
            for typsplit in typ.split("/"):
                if STRIP:
                    typsplit = typsplit.strip(":")
                fill_dct(types_slash, typsplit)
        fill_dct(types_dct, typ)

NUM = -39
df = pd.DataFrame({
        "gcvs": pd.Series(types_dct),
        "+": pd.Series(types_plus),
        "/": pd.Series(types_slash),
    }).fillna(0).sort_values(by="gcvs")[NUM:]

# print(pd.Series(types_dct).sort_values()[:-5:-1])
# print(pd.Series(types_plus).sort_values()[:-5:-1])
# print(pd.Series(types_slash).sort_values()[:-5:-1])
print(df[:-11:-1])

# ascending=False
ax = df.plot.bar(stacked=True, figsize=(16, 9), width=0.88, rot=45)
ax.legend([
        "Типы переменных звезд ОКПЗ",
        "Звезды с несколькими типами переменности (+)",
        "Компоненты множественных классификаций затменных (/)",
        ], fontsize=12, loc="upper left")

plt.subplots_adjust(left=0.051, bottom=0.102, right=0.985, top=0.955)
plt.xlabel("Типы переменных звезд", fontsize=14)
plt.ylabel("Количество переменных звезд", fontsize=14)
plt.title("Распределение по типам переменных звезд в текущей версии ОКПЗ, "
    + f"всего {sum(types_dct.values())} объектов. Октябрь 2022 года",
    fontsize=15)
ax.yaxis.set_minor_locator(MultipleLocator(250))
for x, y in enumerate(df.sum(axis=1)):
    ax.annotate(int(y), (x, y + 42), ha="center")
# ax.bar_label(ax.containers[-1])

FILE_EXT = "png"
PLT_PTH = "../../../plots/stars/gcvs_types_distribution-combined-sorted-latest+"
tmp_pth = f"{PLT_PTH}_.{FILE_EXT}"
pth = f"{PLT_PTH}.{FILE_EXT}"
plt.savefig(tmp_pth, dpi=120)
if FILE_EXT == "svg":
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
