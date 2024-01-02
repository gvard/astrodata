"""Python script for plotting a chart with close asteroid approaches
at a distance of up to 1.1 LD (~422800 km) using a Small-Body DataBase
(SBDB) Close-Approach Data API.
Data source: https://ssd-api.jpl.nasa.gov/doc/cad.html
"""

import json
import urllib.request
from datetime import datetime, timedelta

import matplotlib.pyplot as plt


TODAY = datetime.now()
DIST_MAX = "1.1"
MOON_DIST = (356353, 384399, 406720)
HMAX = 30
START = datetime(2018, 1, 1)
DATE_LIM = START.strftime("%Y-%m-%d")
URL = f"https://ssd-api.jpl.nasa.gov/cad.api?dist-max={DIST_MAX}LD&date-min={DATE_LIM}&h-max={HMAX}&sort=h"
AE = 149597.8707

with urllib.request.urlopen(URL) as data_json_bin:
    data = json.load(data_json_bin)
COUNT = data.get("count")
# FIELDS = data.get('fields')
data = data.get("data")
names, dates, dist = [], [], []
for ast in data:
    names.append(ast[0])
    dat = datetime.strptime(ast[3], "%Y-%b-%d %H:%M")
    dist.append(float(ast[4]) * AE)
    dates.append(dat)

LIMITS = (START, TODAY + timedelta(9))
DTSHIFT = START + timedelta(21)
ZO = 4

fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)
ax.plot(dates, dist, ".k", zorder=3)

NAMSIZE = {
    "2010 WC9": "60–130",
    "2018 AH": "84–190",
    "2018 GE3": "48–110",
    "2019 NN3": "35–77",
    "2019 OD": "60–130",
    "2019 OK": "57–130",
    "2020 LD": "89–200",  # 140
    "2021 SG": "42–94",
    "2023 DZ2": "70–90",
    # "2020 VZ6": "25–57",
}
for i, nam in enumerate(names[:12]):
    if nam in NAMSIZE.keys():
        t = plt.annotate(
            f"{nam} ({NAMSIZE[nam]} м)",
            (dates[i] + timedelta(2.5), dist[i] + 4),
            fontsize=10, zorder=8,
        )
        ax.plot(dates[i], dist[i], c="brown", marker="*", ms=9, zorder=7)

t = plt.annotate(
    "Луна в перигее", (DTSHIFT, 3.5 + MOON_DIST[0] / 1000), fontsize=13, zorder=ZO
)
# t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='white', linewidth=0))
aa1 = ax.plot(LIMITS, [MOON_DIST[0] / 1000, MOON_DIST[0] / 1000], "--r", lw=2, zorder=5)
t = plt.annotate(
    "Большая полуось орбиты Луны",
    (DTSHIFT, 3.5 + MOON_DIST[1] / 1000),
    fontsize=13, zorder=ZO,
)
# t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='white', linewidth=0))
ax.plot(LIMITS, [MOON_DIST[1] / 1000, MOON_DIST[1] / 1000], "--g", lw=2, zorder=5)
t = plt.annotate(
    "Луна в апогее", (DTSHIFT, 3.5 + MOON_DIST[2] / 1000), fontsize=13, zorder=ZO
)
# t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='white', linewidth=0))
aa0 = ax.plot(LIMITS, [MOON_DIST[2] / 1000, MOON_DIST[2] / 1000], "--b", lw=2, zorder=5)
t = plt.annotate(
    "Геостационарная орбита", (DTSHIFT, 3.5 + 35.786), fontsize=13, zorder=ZO
)
# t.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='white', linewidth=0))
ax.plot(LIMITS, [35.786, 35.786], "--m", lw=3, zorder=5)
t = plt.annotate(
    "Самый далекий пилотируемый полет ",
    (LIMITS[1]-timedelta(days=584), 3.5 + 400.171),
    fontsize=14, zorder=6,
)
t.set_bbox(dict(facecolor="white", alpha=0.9, edgecolor="white", linewidth=0))
ax.plot(LIMITS, [400.171, 400.171], "-r", lw=3, zorder=7)

ax.fill_between(LIMITS, MOON_DIST[0] / 1000, MOON_DIST[2] / 1000, color="#eee")

plt.xlim(LIMITS)
plt.ylim(0, 422)
plt.grid()
plt.ylabel("Расстояние, тыс. км", fontsize=14)
plt.xlabel("Дата", fontsize=14)
plt.title(
    "Сближения "
    + str(COUNT)
    + f" астероидов ($ H<30^m$) с Землей с {START.year} по 2024 годы",
    fontsize=14,
)
plt.savefig("../../../plots/solarsystem/asteroid-close-approaches-ru.png", dpi=120)
