"""Python script for plotting histograms with the distribution of
Solar system objects along the semimajor axis.
Data source: https://www.minorplanetcenter.net/iau/MPCORB.html
"""

from datetime import datetime
import locale
from argparse import ArgumentParser

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
# Импортируем TextBox для создания полей ввода
from matplotlib.widgets import TextBox

from plot_sso_supply import plot_vert_pla, plot_vert_resonances


parser = ArgumentParser(description="Graph plotter script with distribution of Solar system objects")
parser.add_argument("-t", "--translate", action="store_true",
                    help="translate all inscriptions into Russian")

args = parser.parse_args()

LOC = "en_US"
if args.translate:
    LOC = "ru_RU"

locale.setlocale(locale.LC_ALL, LOC)
today = datetime.now()
MONTH, YEAR = today.strftime("%B"), today.year
LOC = "-ru" if args.translate else ""
PLOTS_DIR = "../../../plots/solarsystem/"
DATA_DIR = "../../../data/solarsystem/"
DATA = np.genfromtxt(
    DATA_DIR+'MPCORB.DAT.gz', usecols=(8, 10), skip_header=43,
    delimiter=(
        7, 6, 7, 5, 10,
        11, 11, 11, 11, 12,
        14, 2, 10, 6, 4,
        10, 5, 4, 4, 11,
        5, 28, 9
    ),
    dtype=[
        ("Names", "U7"), ("H", "f8"), ("G", "f8"), ("Ep", "U5"), ("M", "f8"),
        ("Peri", "f8"), ("Node", "f8"), ("i", "f8"), ("e", "f8"), ("n", "f8"),
        ("a", "f8"), ("U", "U1"), ("Ref", "U10"), ("Obs", "int"), ("Opp", "int"),
        ("Arc", "U9"), ("rms", "f8"), ("p1", "U3"), ("p2", "U3"), ("Com", "U10"),
        ("Flags", "U4"), ("Desig", "U27"), ("Last", "int"),
    ])


# Берем параметры для первого графика (малые планеты)
a1, a2, b1, b2, bins, xmal, plot_tno, objs_nam = (0.7, 5.4, 0, 7800, 2900, 0.5, False, "малых планет")

# Фильтруем данные один раз перед отрисовкой
filtered_mask = (DATA["a"] >= 0.1) & (DATA["a"] <= 10)  # Берем с запасом для динамического изменения
Filtered = DATA[filtered_mask]

# Создаем фигуру и резервируем место снизу под интерактивные элементы (GUI)
fig, ax = plt.subplots(figsize=(16, 9))
fig.subplots_adjust(bottom=0.13, left=0.05, right=0.99, top=0.956) # Оставили место снизу (bottom=0.18)

# Строим гистограмму один раз
print(bins)
n, bins_edges, patches = ax.hist(Filtered["a"], bins=bins)

# Отрисовка ваших функций (обратите внимание, им нужно передать ax)
plot_vert_pla(b1, b2)
plot_vert_resonances(b1, b2, plot_tno=plot_tno)

# Устанавливаем начальные лимиты и сетку
ax.xaxis.set_major_locator(MultipleLocator(xmal))
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.set_xlim(a1, a2)
ax.set_ylim(b1, b2)
ax.set_title(f"Распределение {len(Filtered)} {objs_nam} по большой полуоси", fontsize=13)

# --- СОЗДАНИЕ GUI ЭЛЕМЕНТОВ ---
# Координаты для текстовых полей: [left, bottom, width, height]
ax_xmin = fig.add_axes([0.1, 0.03, 0.1, 0.04])
ax_xmax = fig.add_axes([0.3, 0.03, 0.1, 0.04])
ax_ymin = fig.add_axes([0.6, 0.03, 0.1, 0.04])
ax_ymax = fig.add_axes([0.8, 0.03, 0.1, 0.04])

# Инициализируем виджеты TextBox с начальными значениями
txt_xmin = TextBox(ax_xmin, 'X min: ', initial=str(a1))
txt_xmax = TextBox(ax_xmax, 'X max: ', initial=str(a2))
txt_ymin = TextBox(ax_ymin, 'Y min: ', initial=str(b1))
txt_ymax = TextBox(ax_ymax, 'Y max: ', initial=str(b2))

# Функция-обработчик, которая вызывается при изменении значений
def update_limits(text):
    try:
        # Считываем значения из полей ввода
        xmin = float(txt_xmin.text)
        xmax = float(txt_xmax.text)
        ymin = float(txt_ymin.text)
        ymax = float(txt_ymax.text)

        # Обновляем границы осей «на лету» без перерисовки самих данных
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)

        # Принудительно обновляем холст
        fig.canvas.draw_idle()
    except ValueError:
        # Игнорируем некорректный ввод (например, если поле пустое или там буквы)
        pass

# Привязываем функцию ко всем четырем полям (срабатывает при нажатии Enter)
txt_xmin.on_submit(update_limits)
txt_xmax.on_submit(update_limits)
txt_ymin.on_submit(update_limits)
txt_ymax.on_submit(update_limits)

plt.show()
