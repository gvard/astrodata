"""Python script for plotting data revisions submitted to AAVSO VSX"""

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator, ScalarFormatter, FixedLocator
import pandas as pd
import seaborn as sns


submissions = pd.read_csv("SearchResults.csv")

fig1, ax = plt.subplots(figsize=(16, 9))
fig1.subplots_adjust(0.048, 0.06, 0.99, 0.97)
plt.title(f"Constellations of stars, revised in AAVSO VSX, {len(submissions)} variables", fontsize=14)
print("Constellations:", sorted(set(submissions["Const"])))
print("Number of constellations:", len(set(submissions["Const"])))
sns.histplot(data=sorted(submissions["Const"]))
plt.xlabel("Constellations", fontsize=14, labelpad=1)
plt.ylabel("Number", fontsize=14)
ax.yaxis.set_minor_locator(MultipleLocator(1))
ax.tick_params(which="major", length=3.5)
ax.tick_params(which="minor", length=2.5)
plt.xticks(fontsize=12)
plt.yticks(fontsize=14)

plt.savefig("../vsx-constellations-chart.png", dpi=120)


fig2, ax = plt.subplots(figsize=(16, 9))
fig2.subplots_adjust(0.048, 0.06, 0.99, 0.97)
plt.title(f"Variability types of stars revised in AAVSO VSX, {len(submissions)} variables", fontsize=14)
print("Variability types:", sorted(set(submissions["Type"])))
print("Number of variability types:", len(set(submissions["Type"])))
sns.histplot(data=sorted(submissions["Type"]))
plt.xlabel("Variability types", fontsize=14, labelpad=1)
plt.ylabel("Number", fontsize=14)
ax.yaxis.set_minor_locator(MultipleLocator(2))
ax.tick_params(which="major", length=3.5)
ax.tick_params(which="minor", length=2.5)
plt.xticks(fontsize=12)
plt.yticks(fontsize=14)

plt.savefig("../vsx-vtypes-chart.png", dpi=120)


submissions = submissions[submissions["Period"] != "--"]
submissions["Period"] = submissions["Period"].astype("float")

fig3, ax = plt.subplots(figsize=(16, 9))
fig3.subplots_adjust(0.048, 0.06, 0.99, 0.97)
plt.title(f"Distribution of the periods of stars revised in AAVSO VSX, {len(submissions["Period"])} variables", fontsize=14)
print("Periods:", sorted(submissions["Period"]))
print("Number of periods:", len(set(submissions["Period"])))
sns.histplot(data=sorted(submissions["Period"]))
plt.xlabel("Period", fontsize=14, labelpad=1)
plt.ylabel("Number", fontsize=14)
ax.yaxis.set_minor_locator(MultipleLocator(1))
ax.xaxis.set_minor_locator(MultipleLocator(10))
ax.tick_params(which="major", length=3.5)
ax.tick_params(which="minor", length=2.5)
plt.xticks(fontsize=12)
plt.yticks(fontsize=14)

plt.savefig("../vsx-periods-chart.png", dpi=120,)
