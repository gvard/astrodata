"""Python script for plotting a bar chart of the primary mirror diameters of telescopes
"""

import json

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, ScalarFormatter
import pandas as pd
import seaborn as sns

with open("../../../data/observatories.json", encoding="utf-8") as json_data:
    data = pd.DataFrame.from_dict(json.loads(json_data.read()))

dis = []
limm = 400

exc = ["Radcliffe 1976", "PTF", "INT (1984)", "SST (2020)"]
for tel in data.keys():
    dia = data[tel]["diam"]
    try:
        di = float(dia)
        if tel in exc or data[tel]["type"] == "spectrograph":
            print(tel + ":", di, "!pass!")
            continue
        if di > limm and di < 12999:
            # dis.append(dd)
            print(tel + ":", di)
            dis.append(di)
    except ValueError:
        dd, mul = dia.split("x")
        dd = float(dd)
        if dd > limm and dd < 12999 and tel not in exc:
            for i in range(int(mul)):
                print(tel + ":", dd, "!mul!")
                dis.append(dd)

data = pd.Series(dis)

fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)

bns = 40
sns.histplot(data, bins=bns)  # , log_scale=True)  # , discrete=True)

plt.title(f"Распределение диаметров зеркал телескопов в выборке. Всего {len(data)} зеркал", fontsize=14)
plt.xlabel("Диаметр, мм", fontsize=14, labelpad=1)
plt.ylabel("Количество", fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=12)
plt.gca().xaxis.set_major_formatter(ScalarFormatter())
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.yaxis.set_minor_locator(MultipleLocator(1))
ax.xaxis.set_major_locator(MultipleLocator(1000))
plt.xlim(200, 10700)
plt.savefig("../../../plots/observational/telescope_diameters_chart.png", dpi=160)
# plt.show()
