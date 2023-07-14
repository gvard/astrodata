"""Script for plotting various distributions of Milky Way clusters.
Data sources:
Improving the open cluster census. II. An all-sky cluster catalogue with Gaia DR3
https://ui.adsabs.harvard.edu/abs/2023A%26A...673A.114H/abstract
VizieR Online Data Catalog: Improving the open cluster census. II. (Hunt+, 2023)
Data source: https://cdsarc.cds.unistra.fr/viz-bin/cat/J/A+A/673/A114
Last modification: 23-May-2023
See https://cdsarc.cds.unistra.fr/ftp/J/A+A/673/A114/ReadMe for byte-by-byte
description of clusters.dat
"""


import os

from scour import scour
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, ScalarFormatter
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


PLOTS_DIR = "../../../plots/stars/"
DATA_DIR = "../../../data/hunt2023/"
MS = 3
UP = 0.1
DATA = np.genfromtxt(
    DATA_DIR + "clusters.dat",
    #  usecols=(0, 1, 3, 5, 26, 27, 28, 29,
    #  30, 31, 34, 35, 36, 48, 49),
    delimiter=(
        21, 5, 247, 2, 12,
        7, 12, 6, 13, 13,
        13, 12, 12, 12, 12,
        12, 14, 14, 14, 14,
        14, 12, 11, 13, 12,
        11, 13, 12, 11, 16,
        16, 17, 6, 2, 17,
        17, 17, 14, 14, 14, 5,
        10, 10, 11, 11,
        11, 4, 11, 11,
        12, 10, 11, 11, 10,
        11, 11, 12, 12, 12,
        3, 2, 2, 3, 4),
    dtype=[("Name", "U20"), ("ID", "int"), ("AllNames", "U246"), ("Type", "U1"), ("CST", "f8"),
        ("N", "int"), ("CSTt", "f8"), ("Nt", "int"), ("RAdeg", "f8"), ("DEdeg", "f8"),
        ("GLON", "f8"), ("GLAT", "f8"), ("r50", "f8"), ("rc", "f8"), ("rt", "f8"), # GLAT E11.4
        ("rtot", "f8"), ("r50pc", "f8"), ("rcpc", "f8"), ("rtpc", "f8"), ("rtotpc", "f8"),
        ("pmRA", "f8"), ("s_pmRA", "f8"), ("e_pmRA", "f8"), ("pmDE", "f8"), ("s_pmDE", "f8"),
        ("e_pmDE", "f8"), ("Plx", "f8"), ("s_Plx", "f8"), ("e_Plx", "f8"), ("dist16", "f8"),
        ("dist50", "f8"), ("dist84", "f8"), ("Ndist", "int"), ("globalPlx", "int"), ("X", "f8"),
        ("Y", "f8"), ("Z", "f8"), ("RV", "f8"), ("s_RV", "f8"), ("e_RV", "f8"), ("n_RV", "int"),
        ("CMDCl2.5", "f8"), ("CMDCl16", "f8"), ("CMDCl50", "f8"), ("CMDCl84", "f8"),
        ("CMDCl97.5", "f8"), ("CMDClHuman", "U3"), ("logAge16", "f8"), ("logAge50", "f8"),
        ("logAge84", "f8"), ("AV16", "f8"), ("AV50", "f8"), ("AV84", "f8"), ("diffAV16", "f8"),
        ("diffAV50", "f8"), ("diffAV84", "f8"), ("MOD16", "f8"), ("MOD50", "f8"), ("MOD84", "f8"),
        ("minClSize", "int"), ("isMerged", "int"), ("isGMMMemb", "int"), ("NXmatches", "int"),
        ("XmatchType", "U3")
        ])

df = pd.DataFrame(DATA)
df["Name"] = df["Name"].str.strip()
df["age"] = 10**df["logAge50"] / 10**9
df_o = df[df["Type"] == "o"]
df_m = df[df["Type"] == "m"]
df_g = df[df["Type"] == "g"]

with pd.option_context("display.max_rows", 4):
    print("Open clusters:")
    print(df_o[["Name", "dist50", "age", "logAge50", "logAge84"]].sort_values(by="logAge50"))
    print("Moving groups:")
    print(df_m[["Name", "dist50", "age", "logAge50", "logAge84"]].sort_values(by="logAge50"))
    print("Globular clusters:")
    print(df_g[["Name", "dist50", "age", "logAge50", "logAge84"]].sort_values(by="logAge50"))

ple = df[df["Name"] == "Melotte_22"]
hya = df[df["Name"] == "Melotte_25"]
praesepe = df[df["Name"] == "NGC_2632"]
ruprecht147 = df[df["Name"] == "Ruprecht_147"]

df_nearest = df[df["dist50"] < 80].sort_values(by="dist50")
print("Nearest clusters:")
print(df_nearest[["Name", "dist50", "age", "logAge50"]])

fig, ax = plt.subplots(figsize=(16, 9))
plt.subplots_adjust(left=0.051, bottom=0.06, right=0.98, top=0.955)
sct = plt.scatter(df.dist50, df.age, s=MS, label="Open clusters")
sct_m = plt.scatter(df_m.dist50, df_m.age, s=MS + 1, c="r", label="Moving groups")
sct_g = plt.scatter(df_g.dist50, df_g.age, s=MS + 1, c="k", label="Globular clusters")
plt.plot(ple.dist50, ple.age, "ok", ms=5)
plt.plot(hya.dist50, hya.age, "og", ms=5)
plt.plot(praesepe.dist50, praesepe.age, "o", ms=5, c="midnightblue")
plt.plot(ruprecht147.dist50, ruprecht147.age, "o", c="orange", ms=5)
plt.plot((10, 10000), (4.6, 4.6), "--y", lw=2, label="The age of the Sun")

plt.text(hya.dist50.iloc[0], hya.age.iloc[0] + UP, "Hyades", fontsize=10)
plt.text(ple.dist50.iloc[0], ple.age.iloc[0] + UP, "Pleiades", fontsize=10)
plt.text(praesepe.dist50.iloc[0], praesepe.age.iloc[0] + UP, "Praesepe", fontsize=10)
plt.text(ruprecht147.dist50.iloc[0] + 2, ruprecht147.age.iloc[0] + UP, "Ruprecht 147", fontsize=10)

plt.xscale("log")
plt.xlim(10, 10000)
plt.ylim(-0.02, 9.518)
ax.yaxis.set_minor_locator(AutoMinorLocator())
plt.title("All known clusters in distance-age space (Hunt+, 2023)")
plt.xlabel("Distance (pc)", labelpad=3)  # , fontsize=12
plt.ylabel("Age (Gyr)", labelpad=8)
plt.legend(loc="upper left")
plt.grid(axis="both", which="major", linestyle=":")
ax.xaxis.set_major_formatter(ScalarFormatter())

FILE_EXT = "png"
PLT_PTH = PLOTS_DIR + "clusters-dist-age-omg-annotated"
tmp_pth = f"{PLT_PTH}_.{FILE_EXT}"
pth = f"{PLT_PTH}.{FILE_EXT}"
plt.savefig(tmp_pth, dpi=120)

if FILE_EXT == "svg":
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
