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
wvs = []
for instr, dat in data.items():
    numbr = 1
    diam = dat["diam"]
    if dat.get("firstlight"):
        fl = dat["firstlight"]
    else:
        continue
    tp = dat.get("type")
    mr = dat.get("mirror")
    lc = dat.get("loc")
    wv = dat.get("wvband")
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
                wvs.append(wv)
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
    if dat.get("effdiam"):
        areas.append(round(np.pi * (dat.get("effdiam") / 1000) ** 2, 2))
    else:
        areas.append(round(area, 2))
    nams.append(instr)
    if isinstance(wv, list) and "NIR" in wv or wv == "NIR":
        wv = "NIR"
    else:
        wv = ""
    wvs.append(wv)

fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)

XLIMS = (datetime(1917, 4, 10), datetime(2026, 1, 1))
# XLIMS = (datetime(1990, 4, 15), datetime(2007, 11, 15))

NAMES_DCT = {"TBL": "", "HET-1996": "HET (1996)", "HET-2015": "HET (2015)",
             "MMT-1979": "MMT (1979)", "MMT-2000": "MMT (2000)", "PS 1": "PS1",
             "PS 2": "PS2", "INT (1967)": "INT", "INT (1984)": "INT", "SST (2020)": "SST-2020",
             "Byurakan": "BAO", "Vainu Bappu": "", "ATT": "", "UH88": "",
             "2MASS 1": "2MASS", "2MASS 2": "", "JST250": "JST", "MRO-2.4": "", "APF": "", "TNT": "",
             "Aristarchos": "", "Lijiang": "", "Xinglong 2.16m": "", "MPG/ESO": "", "MPG/ESO": "",
             "Jorge Sahade": "", "UNAM 2.12": "", "MPIA-CAHA": "", "INAOE 2.12": "",
             "Fraunhofer": "", "Ondrejov": "", "Rozhen 2m": "", "Radcliffe 1976": "",
             "Radcliffe 1948": "Radcliffe", "Faulkes N": "", "Faulkes S": "", "NAYUTA": "",
             "Okayama 1.88m": "", "LT": "", "RTT150": "", "MAGNUM": "", "Kottamia": "",
             "KPNO 2.1": "KPNO", "VATT": "", "Perkins": "",
             "Great Melbourne Telescope-Mt. Stromlo": "Great Melbourne",
             }  # "ELODIE": "",
SHIFT_DCT = {"Starfire OR": 60}
if XLIMS[1] == datetime(2007, 11, 15):
    NAMES_DCT.update({"UBC": "UBC/Laval LMT", "ELODIE": "ELODIE"})
    SHIFT_DCT.update({"Starfire OR": 30})
    ARS_DCT = {
        "VLT": -3,
        "VLTI": -28,
        "Subaru": 9,
        "Gemini 1": -30,
        "Gemini 2": -30,
        "SDSS": -8,
        "LMT": -26,
        "ARC": 14,
        "Terskol": -3,
        "ELODIE": -10
    }
    DYS_DCT = {
        "GTC": -80,
        "VLTI": 20,
        "PS 1": -90,
        "SDSS": 15,
        "WIYN": -200,
        "ARC": -20,
        "Starfire OR": 20,
        "UBC": -30,
        "MMT (2000)": -30,
        "ELODIE": 20
    }
    _DYS, _ARS = 10, 9
else:
    _DYS, _ARS = 10, 4
    ARS_DCT = {
        "LSST": -14.5,
        "Great Melbourne Telescope-Mt. Stromlo": -5.9,
        "Radcliffe 1948": -1,
        "KPNO 2.1": -1,
        "HCT": -6,
        "JST250": -12,
        "Struve": -2,
        "Plaskett": -1,
        "GTC": -7,
        "LBT": -7,
        "Subaru": 2,
        "Gemini 1": -16,
        "Gemini 2": -16,
        "VLTI": -24,
        "JWST": 2,
        "SDSS": -6,
        "ESO-3.6m": -13,
        "IRTF": -12,
        "CFHT": -10,
        "UKIRT": -4,
        "Blanco": -4,
        "TNG": -7,
        "2MASS": -5,
        "ELODIE": -13,
        "HARPS": -3,
        "LAMOST": 1,
        "VISTA": -10,
        "Herschel": -13,
        "MPI-CAHA": 0.6,
        "Starfire OR": -13,
        "ARC": -8,
        "INO": -14,
        "SST (2020)": -2,
        "SST": -5,
        "SOFIA": -3,
        "LMT": -14,
        "Byurakan": -6,
        "Terskol": -6,
        "VST": -5,
        "ShAO": -10,
        "SAI-2.5": 0,
        "INT": -14,
        "INT (1967)": -7,
        "du Pont": -6,
        "HST": -14,
        "UBC": -1,
        "Hiltner": -15,
        "Bok": -1,
        "PS 1": -7,
        "PS 2": -7,
        "AJT": -4,
        "WIRO": -12.5,
        "2MASS 1": -6,
        "OHP": -6,
        "DDO": -1,
    }
    DYS_DCT = {
        "LSST": -980,
        "Great Melbourne Telescope-Mt. Stromlo": 100,
        "Radcliffe 1948": -100,
        "KPNO 2.1": -800,
        "HCT": 200,
        "DOT": -500,
        "Struve": 120,
        "Seimei": -500,
        "LBT": -990,
        "GTC": -1170,
        "VLTI": 4,
        "Mayall KPNO": -2850,
        "AAT": -200,
        "ESO-3.6m": -1900,
        "CFHT": 90,
        "UKIRT": 60,
        "Blanco": 100,
        "TNG": 100,
        "2MASS": 100,
        "ELODIE": -600,
        "SDSS": 110,
        "HARPS": 100,
        "SOAR": -800,
        "LAMOST": -900,
        "LDT": 100,
        "VISTA": 150,
        "Herschel": 50,
        "MPI-CAHA": -400,
        "NTT": 100,
        "ARC": -1000,
        "WIYN": -650,
        "SST": 120,
        "SST (2020)": 60,
        "Starfire OR": 60,
        "Terskol": 100,
        "IRTF": 100,
        "Byurakan": 120,
        "SOFIA": -1450,
        "NOT": -600,
        "H. Smith": -1200,
        "ShAO": 90,
        "SAI-2.5": 0,
        "INT": -500,
        "INT (1967)": -890,
        "du Pont": -1800,
        "HST": -280,
        "UBC": -1000,
        "VST": 90,
        "Hiltner": -500,
        "Bok": -30,
        "MMT (2000)": -2700,
        "PS 1": 120,
        "PS 2": 120,
        "OHP": -900,
        "AJT": 70,
        "WIRO": -500,
        "Euclid": -800,
        "2MASS 1": 100,
        "JST250": 100,
    }
clrs_dct = {
    "liquid-mirror": "lightgrey", "military": "#555", "spectrograph": "limegreen", "NIR": "salmon",
}
markers_dct = {"segmented": "h", "multiple": "$\clubsuit$", "liquid": "o", "military": "D"}

all_telescopes = set()
for i, ar in enumerate(areas):
    DYS, ARS = _DYS, _ARS
    if (ar > 5 and ar < 452) or nams[i] in ("Euclid"):
        if nams[i] == "VLTI":
            ar = 844.9628
        if nams[i]:
            all_telescopes.add(nams[i])  # .split("(")[0]
        clr = "k"
        if types[i] in clrs_dct:
            clr = clrs_dct[types[i]]
        if wvs[i] == "NIR" and nams[i] != "BTA":  # or (type(wvs[i]) is list and "NIR" in wvs[i]):
            clr = clrs_dct["NIR"]
        marker = "o"
        if mirrors[i] in markers_dct:
            marker = markers_dct[mirrors[i]]
        SFDLT = 0
        if nams[i] in SHIFT_DCT:
            SFDLT = SHIFT_DCT[nams[i]]
        MS = 6
        FS = 13
        if ar > 227:
            MS = 9
            FS = 13
        elif ar < 227 and ar >= 47.78:
            MS = 6
            FS = 12
        elif ar < 47.78 and ar >= 18.095:  # 3.9-2.4
            MS = 5.25
            FS = 12
        elif ar < 18.095 and ar >= 15.2:
            MS = 4.25
            FS = 11
        elif ar < 15.2:
            MS = 3.5
            FS = 10
        if types[i] == "spectrograph":
            MS = 5
            FS = 11
        if types[i] == "military":
            marker = markers_dct["military"]
        if nams[i] == "2MASS 1":
            FS = 8.5
        if locs[i] == "space":
            clr = "cyan"
        ZORD = 1
        if nams[i] in ("HST", "Herschel", "JWST"):
            ax.plot(
                dats[i] + timedelta(days=SFDLT), ar, marker=marker,
                fillstyle="left", c='cyan', markerfacecoloralt='salmon',
                markeredgecolor="black", markeredgewidth=0.5, ms=MS+1, zorder=ZORD,
            )
        else:
            ax.plot(
                dats[i] + timedelta(days=SFDLT), ar, marker=marker, c=clr,
                markeredgecolor="black", markeredgewidth=0.85, ms=MS, zorder=ZORD,
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
        if nams[i] in NAMES_DCT:
            nams[i] = NAMES_DCT[nams[i]]
        t = plt.annotate(
            nams[i].replace(" ", "$\,$"), (dats[i] + timedelta(days=DYS), ar + ARS), fontsize=FS,
            zorder=5
        )

print(all_telescopes, len(all_telescopes))

if XLIMS[1] == datetime(2007, 11, 15):
    ANDLT, ANDLT2 = 5, -20
else:
    ANDLT, ANDLT2 = 3, -12

# plt.plot(XLIMS, (4.5239, 4.5239), ":", c="lightgrey", lw=1, zorder=0)
# t = plt.annotate("1.2 m", (XLIMS[0] + timedelta(days=30), 4.6),
#                  c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (12.566, 12.566), ":", c="lightgrey", lw=1, zorder=0)
# t = plt.annotate("2 m", (XLIMS[0] + timedelta(days=30), 12.7),
#                  c="grey", fontsize=13, zorder=5)
# plt.plot(XLIMS, (12.566, 12.566), ":", c="lightgrey", lw=1, zorder=0)
# t = plt.annotate("2.1 m", (XLIMS[0] + timedelta(days=30), 5.0),
#                  c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (50.265, 50.265), ":", c="lightcoral", lw=1, zorder=0)
t = plt.annotate("4 m", (XLIMS[0] + timedelta(days=30), 51 + ANDLT - 1),
                 c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (113.097, 113.097), ":", c="tomato", lw=1, zorder=0)
t = plt.annotate("6 m", (XLIMS[0] + timedelta(days=30), 113.097 + ANDLT),
                 c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (201.062, 201.062), ":c", lw=1, zorder=0)
t = plt.annotate("8 m", (XLIMS[0] + timedelta(days=30), 201.062 + ANDLT),
                 c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (314.159, 314.159), ":", c="slateblue", lw=1, zorder=0)
t = plt.annotate("10 m", (XLIMS[0] + timedelta(days=30), 314.159 + ANDLT2),  # - 15
                 c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (452.389, 452.389), ":", c="lightgrey", lw=1, zorder=0)
t = plt.annotate("12 m", (XLIMS[0] + timedelta(days=30), 452.389 + ANDLT2),  #  - 30
                 c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (615.752, 615.752), ":", c="lightgrey", lw=1, zorder=0)
t = plt.annotate("14 m", (XLIMS[0] + timedelta(days=30), 615.752 + ANDLT2),
                 c="grey", fontsize=13, zorder=5)
plt.plot(XLIMS, (804.248, 804.248), ":", c="lightgrey", lw=1, zorder=0)
t = plt.annotate("16 m", (XLIMS[0] + timedelta(days=30), 804.248 + ANDLT2),
                 c="grey", fontsize=13, zorder=5)

plt.xlim(XLIMS)
if XLIMS[1] == datetime(2007, 11, 15):
    plt.ylim(1.3, 845)
else:
    plt.ylim(2.3, 454)
    # plt.ylim(4.3, 470)
if XLIMS[1] == datetime(2007, 11, 15):
    YL, MYL = 2, 1
else:
    YL, MYL = 10, 2
ax.xaxis.set_major_locator(mdates.YearLocator(YL))
ax.xaxis.set_minor_locator(mdates.YearLocator(MYL))
# ax.set_yscale("log")

plt.title(f"Первый свет крупных обсерваторий и установок, всего более {len(all_telescopes)} дат", fontsize=14)
plt.xlabel("Дата, годы", fontsize=13)
plt.ylabel("Площадь главных зеркал, $м^2$", fontsize=13)

handles, labels = plt.gca().get_legend_handles_labels()

MS = 7.5
legend_elements = [
    Line2D([0], [0], label="Segmented mirror", c="k", markeredgecolor="black",
           markeredgewidth=0.85, ms=MS, marker="H", linestyle=""),
    Line2D([0], [0], label="Multiple mirror", c="k", markeredgecolor="black",
           markeredgewidth=0.85, ms=MS, marker="$\clubsuit$", linestyle=""),
    Line2D([0], [0], label="Liquid mirror", c="lightgrey", markeredgecolor="black",
           markeredgewidth=0.85, ms=MS, marker="o", linestyle=""),
    Line2D([0], [0], label="Space-based", c="cyan", markeredgecolor="black",
           markeredgewidth=0.85, ms=MS, marker="o", linestyle=""),
    Line2D([0], [0], label="Infrared", c="salmon", markeredgecolor="black",
           markeredgewidth=0.85, ms=MS, marker="o", linestyle=""),
    Line2D([0], [0], label="Spectrograph", c="limegreen", markeredgecolor="black",
           markeredgewidth=0.85, ms=MS, marker="o", linestyle=""),
    Line2D([0], [0], label="Military", c=clrs_dct["military"], markeredgecolor="black",
           markeredgewidth=0.85, ms=MS-1, marker=markers_dct["military"], linestyle=""),
]
handles.extend(legend_elements)
plt.legend(handles=handles, loc="upper right", fontsize=13)

plots_dir = os.path.join(os.pardir, os.pardir, os.pardir, "plots", "observational")
FILE_EXT = "png"
if XLIMS[1] == datetime(2007, 11, 15):
    FILENAME = "first-light-1990-2008"
else:
    FILENAME = "first-light-1917-2025"
tmp_pth = os.path.join(plots_dir, f"{FILENAME}_.{FILE_EXT}")
pth = os.path.join(plots_dir, f"{FILENAME}.{FILE_EXT}")
plt.savefig(tmp_pth, dpi=160)
