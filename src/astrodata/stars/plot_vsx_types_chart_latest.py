"""Script for plotting a bar chart with types of variable stars in
the current version of the AAVSO International Variable Star Index (VSX).
Data source: https://cdsarc.cds.unistra.fr/viz-bin/cat/B/vsx

According to variable star type designations in vsx,
https://www.aavso.org/vsx/index.php?view=about.vartypes
A colon (:) after the variability type -or any other field- means
the value/classification is uncertain.
A pipe character (|) between two different types signifies a logical OR;
the classification is uncertain and all possible types are indicated.
An example of this is ELL|DSCT, where the star may be an ellipsoidal binary system
or a DSCT-type pulsating variable with half the given period.
A plus character (+) signifies a logical AND; two different variability types
are seen in the same star or system. An example of this would be ELL+DSCT, where
one of the components of an ellipsoidal binary system is a DSCT-type pulsating variable.
A slash character (/) indicates a subtype. In the case of binary systems (eclipsing,
ellipsoidal or reflection variables) it is used to help describe either the physical
properties of the system (E/PN or EA/RS), the luminosity class of the components (EA/DM),
or the degree of filling of their inner Roche lobes (EA/SD).
This is the GCVS classification system. In cataclysmic variables, slash characters
are used to indicate some properties of the system, as in the degree of polarization
(NA/DQ) or the nature of their components (UG/IBWD).
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


data_raw = pd.read_csv("../../../data/vsx/vsx_csv.dat", usecols=["Type"])
df = data_raw["Type"].str.strip(":")
series = df.squeeze()

df = series.value_counts()
print(df[:20], "Length", len(df))

df_plus = df[df.index.str.contains("+", regex=False)]
df_slash = df[df.index.str.contains("/", regex=False)]
df_or = df[df.index.str.contains("|", regex=False)]
types_plus = {}
types_slash = {}
types_or = {}

for ind in df_plus.index:
    for typsplit in ind.split("+"):
        typsplit = typsplit.strip(":")
        try:
            types_plus[typsplit] += df_plus[ind]
        except KeyError:
            types_plus[typsplit] = df_plus[ind]

for ind in df_slash.index:
    for typsplit in ind.split("/"):
        typsplit = typsplit.strip(":")
        try:
            types_slash[typsplit] += df_slash[ind]
        except KeyError:
            types_slash[typsplit] = df_slash[ind]

for ind in df_or.index:
    for typsplit in ind.split("|"):
        typsplit = typsplit.strip(":")
        try:
            types_or[typsplit] += df_or[ind]
        except KeyError:
            types_or[typsplit] = df_or[ind]

print("spl +:")
print(pd.Series(types_plus)[:5])
print("spl /:")
print(pd.Series(types_slash)[:5])
print("spl |:")
print(pd.Series(types_or)[:5])

NUM = -39
data = pd.DataFrame({"vsx": df,
                     "+": pd.Series(types_plus),
                     "/": pd.Series(types_slash),
                     "|": pd.Series(types_or)}).fillna(0).astype(int).sort_values(by="vsx")[NUM:]

ax = data.plot.bar(stacked=True, figsize=(16, 9), width=0.88, rot=45)
ax.legend(["Типы переменных звезд VSX",
           "Звезды с несколькими типами переменности (+)",
           "Компоненты множественных классификаций затменных (/)",
           "Возможные типы, неопределенная классификация (|)"],
          fontsize=12, loc="upper left")

locale.setlocale(locale.LC_ALL, "ru_RU")
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year

print("Типы выборки:")
print(data[:-20:-1])
print("Их количество:", len(data), "всего типов в статистике:",
    len(series.value_counts()), "всего звезд в каталоге:", len(data_raw))

plt.subplots_adjust(left=0.051, bottom=0.102, right=0.985, top=0.955)
plt.xlabel("Типы переменных звезд", fontsize=14, labelpad=0)
plt.ylabel("Количество переменных звезд", fontsize=14, labelpad=0)
plt.title("Распределение по типам переменных звезд в текущей версии VSX, " + \
    f"всего {len(data_raw)} объектов. Июнь {YEAR} года", fontsize=15)
for x, y in enumerate(data.sum(axis=1)):
    ax.annotate(int(y), (x, y+1700), ha="center", fontsize=7)
# ax.bar_label(ax.containers[-1], fontsize=7)

FILE_EXT = "png"
PLT_PTH = "../../../plots/stars/vsx_types_distribution-combined-sorted-latest-spl+"
tmp_pth = f"{PLT_PTH}_.{FILE_EXT}"
pth = f"{PLT_PTH}.{FILE_EXT}"
plt.savefig(tmp_pth, dpi=120)

if FILE_EXT == "svg":
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
