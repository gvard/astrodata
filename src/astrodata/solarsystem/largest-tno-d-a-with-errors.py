"""Python script for plotting distribution of Solar system objects along the semimajor axis and diameter estimate.
Data sources are presented in https://en.wikipedia.org/wiki/List_of_possible_dwarf_planets
Recent orbital parameters are taken from https://www.minorplanetcenter.net/iau/MPCORB.html
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator


data = {
    # "name/designation": ["имя", "semimajor axis", ("a-", "a+"), "diameter", ("d-", "d+"), "uncertainty parameter"],
    # Ceres is here
    "Orcus": ["Орк", 39.2892348, (0.00027, 0.00027), 910, (40, 50),         1],
    # "Sedna": ["Седна", 549.5551805, (0.05467, 0.05467), 906, (258, 314),       5],
    # "Sedna": ["Седна", 549.5551805, (0.05467, 0.05467), 1025, (135, 135),      5],
    "Salacia": ["Салация", 42.1155087, (0.00027, 0.00027), 846, (21, 21),   1],
    "Mani": ["Мани", 41.621024, (0.00027, 0.00027), 796, (24, 24),          1],
    "Achlys": ["Ахлис", 39.5852395, (0.00027, 0.00027), 772, (12, 12),      1],
    "Aya": ["Айа", 47.2195337, (0.00093, 0.00093), 768, (38, 39),           2],
    "Varda": ["Варда", 45.6246357, (0.00093, 0.00093), 749, (18, 18),       2],
    "Chiminigagua": ["Чиминигагуа", 58.776487, (0.0056, 0.0056), 742, (83, 78), 3],
    "Ixion": ["Иксион", 39.5286997, (0.0056, 0.0056), 709.6, (0.2, 0.2),    3],
    "Goibniu": ["Гоибниу", 41.772451, (0.00027, 0.00027), 680, (34, 34),    1],
    "Ritona": ["Ритона", 41.553612, (0.00027, 0.00027), 679, (73, 55),      1],
    "Uni": ["Уни", 42.9751954, (0.00093, 0.00093), 659, (38, 38),           2],
    "Varuna": ["Варуна", 43.137263, (0.00027, 0.00027), 654, (102, 154),    1],
    "Rumina": ["Румина", 92.4091498, (0.00006, 0.00006), 644, (15, 15),     0],
    "Gǃkúnǁʼhòmdímà": ["Гкъкунлъʼхомдима", 74.587240, (0.0056, 0.0056), 642, (28, 28), 3],
    "2014 UZ224": ["2014 UZ224", 109.94931, (0.46666, 0.46666), 635, (72, 65), 6],
    "Xewioso": ["Хевиозо", 37.683198, (0.00093, 0.00093), 565, (73, 71),       2],
}

data_nam = {
    "Triton": ["Тритон", 30.07, (0.002, 0.002), 2707, (2, 2),               0],
    "Pluto": ["Плутон", 39.33986, (0.00006, 0.00006), 2377, (3, 3),         0],
    "Eris": ["Эрида", 67.997129, (0.00093, 0.00093), 2326, (12, 12),        2],
    "Haumea": ["Хаумеа", 43.0056888, (0.00027, 0.00027), 1559, (6, 6),      1],
    "Makemake": ["Макемаке", 45.449691, (0.00027, 0.00027), 1429, (20, 38), 1],
    "Charon": ["Харон", 39.33986, (0.00006, 0.00006), 1212, (1, 1),         0],
    "Dysnomia": ["Дисномия", 67.997129, (0.00093, 0.00093), 615, (50, 60),  2],
    "Gonggong": ["Гун-гун", 66.895052, (0.0056, 0.0056), 1230, (50, 50),    3],
    "Quaoar": ["Квавар", 43.1629259, (0.00027, 0.00027), 1086, (4, 4),      1],
}

data_numbered = {
    "2005 UQ513": ["2005 UQ513", 43.5774, (0.00093, 0.00093), 498, (75, 63),   2],
    "2014 EZ51":  ["2014 EZ51", 51.8868, (0.00093, 0.00093), 600, (45, 45),    2],
    "2015 RR245": ["2015 RR245", 82.6937, (0.00933, 0.00933), 630, (160, 160), 4],
    "Chaos":      ["Chaos", 46.0987, (0.00027, 0.00027), 600, (130, 140),      1],
    "2010 RF43":  ["2010 RF43", 49.3014, (0.00093, 0.00093), 650, (200, 200),  2],
    "2002 TX300": ["2002 TX300", 43.4775, (0.00027, 0.00027), 320, (50, 50),   1],
    "2010 JO179": ["2010 JO179", 77.9161, (0.00093, 0.00093), 750, (150, 150), 2],
    "2005 QU182": ["2005 QU182", 112.1647, (0.00027, 0.00027), 584, (144, 155), 1],
}


fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)

for k, d in data.items():
    plt.errorbar(d[1], d[3], xerr=([d[2][0]], [d[2][1]]), yerr=([d[4][0]], [d[4][1]]), fmt='o', capsize=5, label=d[0])

for k, d in data_nam.items():
    plt.errorbar(d[1], d[3], xerr=([d[2][0]], [d[2][1]]), yerr=([d[4][0]], [d[4][1]]), fmt='o', capsize=5)
    t = plt.annotate(d[0], (d[1] + 0.4, d[3]), fontsize=12.5)

for k, d in data_numbered.items():
    plt.errorbar(d[1], d[3], xerr=([d[2][0]], [d[2][1]]), yerr=([d[4][0]], [d[4][1]]), marker="d", ms=8, label=d[0])

XLIMS = (29, 113.3)
# XLIMS = (26, 556.4)
YLIMS = (320, 2760)
# YLIMS = (465, 2760)
XAN = 30.5
# XAN = 46.5
MON, YR = "Ноябрь", 2025
DPI = 160

plt.plot(XLIMS, [939.4, 939.4], "--", lw=0.8, c="k")
t = plt.annotate(
    "Церера", (XAN, 954), color="black", fontsize=12)
plt.plot(XLIMS, [525.4, 525.4], "--", lw=0.8, c="k")
t = plt.annotate(
    "Веста", (XAN, 536), color="black", fontsize=12)
plt.plot(XLIMS, [511, 511], "--", lw=0.8, c="k")
t = plt.annotate(
    "Паллада", (XAN, 470), color="black", fontsize=12)
plt.plot(XLIMS, [399, 399], "--", lw=0.8, c="k")
t = plt.annotate(
    "Мимас", (XAN, 406), color="black", fontsize=12)

ax.fill_between(XLIMS, YLIMS[0], 399, color="#eee")

plt.xlim(XLIMS)
plt.ylim(YLIMS)
plt.xlabel("Большая полуось, а.е.", fontsize=12)
plt.ylabel("Диаметр, км", fontsize=12)
plt.title(f"Параметры транснептуновых объектов. {MON} {YR} г.")
plt.legend()
plt.grid(linestyle="dotted", which="major")
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

# plt.show()
plt.savefig(f"../../../plots/solarsystem/largest-tno-d-a-errors-{round(XLIMS[1])}au-ru-.png", dpi=DPI)
