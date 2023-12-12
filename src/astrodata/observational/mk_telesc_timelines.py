"""Python script for plotting scatter plot with telescopes and observatories first light dates
"""

from datetime import datetime, timedelta
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from matplotlib.lines import Line2D

with open("../../../data/observatories.json", encoding="utf-8") as json_data:
    data = json.loads(json_data.read())

nams = []
dats = []
diams = []
areas = []
types = []
mirrors = []
locs = []
for instr, dat in data.items():
    numbr = 1
    diam = dat["diam"]
    fl = dat["firstlight"]
    tp = dat.get("type")
    mr = dat.get("mirror")
    lc = dat.get("loc")
    if isinstance(diam, str):
        diam = [eval(i) for i in diam.split("x")]
        if isinstance(fl, list) and diam[-1] == len(fl):
            for i, fili in enumerate(fl):
                nams.append(" ".join((instr, str(i + 1))))
                dats.append(datetime.strptime(fili, "%Y-%m-%d"))
                diams.append(diam[0])
                areas.append(np.pi * (diam[0] / 1000) ** 2)
                types.append(tp)
                mirrors.append(mr)
                locs.append(lc)
            continue
        numbr, diam = diam[1], diam[0]
    diams.append(diam)
    types.append(tp)
    mirrors.append(mr)
    locs.append(lc)
    if isinstance(fl, list):
        fl = fl[0]
    if isinstance(fl, dict):
        fl = list(fl.values())[0]
    dats.append(datetime.strptime(fl, "%Y-%m-%d"))
    area = dat.get("area")
    if area and isinstance(area, str):
        if area[0] == "<":
            area = float(area[1:])
        elif "x" in area:
            area = np.prod([eval(i) for i in area.split("x")])
    if True:  # not area:
        area = numbr * np.pi * (diam / 1000) ** 2
    areas.append(round(area, 2))
    nams.append(instr)

fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)

XLIMS = (datetime(1917, 4, 10), datetime(2026, 1, 1))
# XLIMS = (datetime(1990, 4, 15), datetime(2007, 11, 15))

NAMES_DCT = {"TBL": "", "HET-1996": "HET (1996)", "HET-2015": "HET (2015)",
             "MMT-1979": "MMT (1979)", "MMT-2000": "MMT (2000)", "PS 1": "PS1",
             "PS 2": "PS2",
             }
if XLIMS[1] == datetime(2007, 11, 15):
    NAMES_DCT.update({"UBC": "UBC/Laval LMT"})
    ARS_DCT = {
        "Subaru": 9,  # 2
        "Gemini 1": -30,  # -16,
        "Gemini 2": -30,  # -16,
        "VLTI": -26,
        "SDSS": -8,
        "LMT": -26,
        "ARC": 14,
        "VLT": -3,
    }
    DYS_DCT = {
        "GTC": -80,
        "VLTI": 4,
        "PS1": -90,
        "SDSS": 15,
        "WIYN": -200,
        "ARC": -20,
        "Starfire OR": 20,
        "UBC/Laval LMT": -30,
        "MMT (2000)": -30,
    }
    _DYS, _ARS = 10, 9
else:
    _DYS, _ARS = 10, 4
    ARS_DCT = {
        "LBT": -7,
        "Subaru": 2,
        "Gemini 1": -16,
        "Gemini 2": -16,
        "VLTI": -24,
        "JWST": 2,
        "SDSS": -6,
        "ESO-3.6m": -13,
        "NASA-IRTF": -13,
        "CFHT": -10,
        "UKIRT": -4,
        "Blanco": -4,
        "TNG": -7,
        "2MASS": -5,
        "HARPS": -3,
        "LAMOST": 1,
        "VISTA": -10,
        "Herschel": -12.5,
        "MPI-CAHA": 0.6,
        "Starfire OR": -13,
        "ARC": -8,
        "INO": -14,
        "SST-2020": -2,
        "SST": -5,
        "SOFIA": -1,
        "LMT": -14,
        "Byurakan": -10,
        "Terskol-2m": -7,
        "VST": -6,
        "ShAO": -8,
        "SAI-2.5": -3,
        "INT": -14,
        "du Pont": -6,
        "HST": -14,
        "UBC": -1,
        "Hiltner": -14,
        "Bok": -10,
        "PS1": -6,
    }
    DYS_DCT = {
        "LBT": -990,
        "GTC": -70,
        "VLTI": 4,
        "Mayall, KPNO": -3000,
        "AAT": -200,
        "ESO-3.6m": -1900,
        "CFHT": 90,
        "UKIRT": 60,
        "Blanco": 100,
        "TNG": 100,
        "2MASS": 100,
        "SDSS": 110,
        "HARPS": 100,
        "SOAR": -800,
        "LAMOST": -800,
        "LDT": 100,
        "VISTA": 150,
        "Herschel": 100,
        "MPI-CAHA": -400,
        "NTT": 100,
        "ARC": -1000,
        "WIYN": -650,
        "SST": 120,
        "SST-2020": 60,
        "Starfire OR": 60,
        "Terskol-2m": 150,
        "NASA-IRTF": 100,
        "Byurakan": 120,
        "SOFIA": -1200,
        "NOT": -600,
        "H.Smith": -1200,
        "ShAO": -1340,  # 130,
        "SAI-2.5": 160,
        "INT": -500,
        "du Pont": -1890,
        "HST": -350,
        "UBC": -1000,
        "VST": 90,
        "Hiltner": -500,
        "Bok": 150,
        "MMT (2000)": -2700,
        "PS1": 120,
    }
clrs_dct = {
    "liquid-mirror": "lightgrey", "military": "salmon", "spectrograph": "limegreen",
}
markers_dct = {"segmented": "h", "multiple": "$\clubsuit$", "liquid": "o"}

for i, ar in enumerate(areas):
    DYS, ARS = _DYS, _ARS
    if ar > 7:  # 1.5m or bigger
        if nams[i] == "VLTI":
            ar = 844.9628
        clr = "k"
        if types[i] in clrs_dct:
            clr = clrs_dct[types[i]]
        if locs[i] == "space":
            clr = "cyan"
        marker = "o"
        if mirrors[i] in markers_dct:
            marker = markers_dct[mirrors[i]]
        if nams[i] in NAMES_DCT:
            nams[i] = NAMES_DCT[nams[i]]
        if nams[i] == "Starfire OR":
            SFDLT = 10
            if XLIMS[1] != datetime(2007, 11, 15):
                SFDLT = 60
            ax.plot(
                dats[i] + timedelta(days=SFDLT), ar, marker=marker, c=clr,
                markeredgecolor="black", markeredgewidth=0.85, ms=6, zorder=1,
            )
        elif nams[i] not in ("VLT/HiRISE",):
            ax.plot(
                dats[i], ar, marker=marker, c=clr,
                markeredgecolor="black", markeredgewidth=0.85, ms=6, zorder=1,
            )
        if nams[i] in ARS_DCT:
            ARS += ARS_DCT[nams[i]]
        if nams[i] in DYS_DCT:
            DYS += DYS_DCT[nams[i]]
        if (
            "VLT" in nams[i]
            and nams[i] not in ("VLTI", "VLT/HiRISE")
            and XLIMS[1] != datetime(2007, 11, 15)
        ):
            ARS -= 3
            DYS = 880
            nams[i] = {"VLT 1": "VLT 1-4", "VLT 2": "", "VLT 3": "", "VLT 4": ""}[nams[i]]
        elif "VLT" in nams[i] and nams[i] not in ("VLTI", "VLT/HiRISE"):
            ARS -= 2
        if "Gemini" in nams[i] and XLIMS[1] != datetime(2007, 11, 15):
            nams[i] = {"Gemini 1": "Gemini N/S", "Gemini 2": ""}[nams[i]]
        elif "Gemini" in nams[i] and XLIMS[1]:
            nams[i] = {"Gemini 1": "Gemini N", "Gemini 2": "Gemini S"}[nams[i]]
        if nams[i] == "PS2":
            ARS -= 6
            DYS += 120
        if nams[i] == "Magellan 1" and XLIMS[1] != datetime(2007, 11, 15):
            nams[i] = "Magellan I/II"
            DYS -= 200
        elif nams[i] == "Magellan 1":
            nams[i] = "Magellan I"
            DYS -= 20
        if nams[i] == "Magellan 2" and XLIMS[1] != datetime(2007, 11, 15):
            nams[i] = ""
            DYS += 15
        elif nams[i] == "Magellan 2":
            nams[i] = "Magellan II"
            DYS += 15
        t = plt.annotate(
            nams[i], (dats[i] + timedelta(days=DYS), ar + ARS), fontsize=12, zorder=5
        )

if XLIMS[1] == datetime(2007, 11, 15):
    ANDLT, ANDLT2 = 5, -20
else:
    ANDLT, ANDLT2 = 3, -12

plt.plot(XLIMS, (12.566, 12.566), ":", c="lightgrey", lw=1, zorder=0)
plt.plot(XLIMS, (50.265, 50.265), ":", c="lightcoral", lw=1, zorder=0)
t = plt.annotate("4 m", (XLIMS[0] + timedelta(days=30), 50.265 + ANDLT),
                 c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (113.097, 113.097), ":", c="tomato", lw=1, zorder=0)
t = plt.annotate("6 m", (XLIMS[0] + timedelta(days=30), 113.097 + ANDLT),
                 c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (201.062, 201.062), ":c", lw=1, zorder=0)
t = plt.annotate("8 m", (XLIMS[0] + timedelta(days=30), 201.062 + ANDLT),
                 c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (314.159, 314.159), ":", c="slateblue", lw=1, zorder=0)
t = plt.annotate("10 m", (XLIMS[0] + timedelta(days=30), 314.159 + ANDLT2),
                 c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (452.389, 452.389), ":", c="lightgrey", lw=1, zorder=0)
t = plt.annotate("12 m", (XLIMS[0] + timedelta(days=30), 452.389 + ANDLT2),
                 c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (615.752, 615.752), ":", c="lightgrey", lw=1, zorder=0)
t = plt.annotate("14 m", (XLIMS[0] + timedelta(days=30), 615.752 + ANDLT2),
                 c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (804.248, 804.248), ":", c="lightgrey", lw=1, zorder=0)
t = plt.annotate("16 m", (XLIMS[0] + timedelta(days=30), 804.248 + ANDLT2),
                 c="grey", fontsize=13, zorder=5)

plt.xlim(XLIMS)
if XLIMS[1] == datetime(2007, 11, 15):
    plt.ylim(7.1, 845)
else:
    plt.ylim(6.1, 454)
if XLIMS[1] == datetime(2007, 11, 15):
    YL, MYL = 2, 1
else:
    YL, MYL = 10, 2
ax.xaxis.set_major_locator(mdates.YearLocator(YL))
ax.xaxis.set_minor_locator(mdates.YearLocator(MYL))

plt.title("Первый свет крупных обсерваторий и установок", fontsize=14)
plt.xlabel("Дата, годы", fontsize=13)
plt.ylabel("Площадь главных зеркал, $м^2$", fontsize=13)

handles, labels = plt.gca().get_legend_handles_labels()

MS = 6
legend_elements = [
    Line2D([0], [0], label="Segmented mirror", c="k", markeredgecolor="black",
           markeredgewidth=0.85, ms=MS, marker="H", linestyle=""),
    Line2D([0], [0], label="Multiple mirror", c="k", markeredgecolor="black",
           markeredgewidth=0.85, ms=MS, marker="$\clubsuit$", linestyle=""),
    Line2D([0], [0], label="Liquid mirror", c="lightgrey", markeredgecolor="black",
           markeredgewidth=0.85, ms=MS, marker="o", linestyle=""),
    Line2D([0], [0], label="Space-based", c="cyan", markeredgecolor="black",
           markeredgewidth=0.85, ms=MS, marker="o", linestyle=""),
    Line2D([0], [0], label="Military", c="salmon", markeredgecolor="black",
           markeredgewidth=0.85, ms=MS, marker="o", linestyle=""),
    Line2D([0], [0], label="Spectrograph", c="limegreen", markeredgecolor="black",
           markeredgewidth=0.85, ms=MS, marker="o", linestyle=""),
]
handles.extend(legend_elements)
plt.legend(handles=handles, loc="upper right", fontsize=13)

plots_dir = os.path.join(os.pardir, os.pardir, os.pardir, "plots", "observational")
FILE_EXT = "png"
if XLIMS[1] == datetime(2007, 11, 15):
    FILENAME = "first-light-1990-2008"
else:
    FILENAME = "first-light-1917-2022"
tmp_pth = os.path.join(plots_dir, f"{FILENAME}_.{FILE_EXT}")
pth = os.path.join(plots_dir, f"{FILENAME}.{FILE_EXT}")
plt.savefig(tmp_pth, dpi=120)
