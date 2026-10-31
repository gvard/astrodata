"""Python script for plotting histograms with the distribution of
Solar system objects along the semimajor axis.
Data source: https://www.minorplanetcenter.net/iau/MPCORB.html
"""

from datetime import datetime
import locale
import sys
from argparse import ArgumentParser

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Компоненты для интеграции Matplotlib в PyQt5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, \
    QSizePolicy
from PyQt5.QtCore import Qt


from plot_sso_supply import plot_vert_pla, plot_vert_resonances


parser = ArgumentParser(description="Graph plotter script with distribution of Solar system objects")
parser.add_argument("-t", "--translate", action="store_false",
                    help="translate all inscriptions into English")

args = parser.parse_args()

LOC = "en_US"
if args.translate:
    LOC = "ru_RU"

try:
    locale.setlocale(locale.LC_ALL, LOC)
except locale.Error:
    pass

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

# Параметры для графика
a1, a2, b1, b2, bins, xmal, plot_tno, objs_nam = (0.7, 5.4, 0, 4000, 5900, 0.5, False, "малых планет")
# Фильтруем данные перед отрисовкой
filtered_mask = (DATA["a"] >= 0.1) & (DATA["a"] <= 10)
# a1, a2, b1, b2, bins, xmal, plot_tno, objs_nam = (29, 70, 0, 56, 3900, 5, True, "транснептуновых объектов")
# filtered_mask = (DATA["a"] >= 4) & (DATA["a"] <= 140)

Filtered = DATA[filtered_mask]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Распределение объектов Солнечной системы")
        self.resize(1600, 1080)

        # Главный контейнер и вертикальный слой
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)  # Минимальные отступы от краев окна
        main_layout.setSpacing(4)  # Минимальный зазор между панелями и графиком

        # Создаем фигуру без жесткого указания figsize
        self.fig, self.ax = plt.subplots()

        # Настраиваем внутренние отступы самого графика, чтобы он занимал максимум места на холсте
        self.fig.subplots_adjust(bottom=0.055, left=0.045, right=0.99, top=0.97)

        self.canvas = FigureCanvas(self.fig)

        # Указываем холсту расширяться во все стороны и заполнять всё доступное пространство
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Кнопки Matplotlib (верхняя панель)
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Панель инструментов должна занимать минимум места по вертикали
        self.toolbar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        # Добавляем элементы на главный слой
        main_layout.addWidget(self.toolbar)
        # Параметр stretch=1 заставляет холст графика забирать всё свободное место,
        # сжимая остальные панели до их минимальных размеров
        main_layout.addWidget(self.canvas, stretch=1)

        # print(bins)
        self.n, self.bins_edges, self.patches = self.ax.hist(Filtered["a"], bins=bins)

        plot_vert_pla(b1, b2)
        plot_vert_resonances(b1, b2, plot_tno=plot_tno)

        # Устанавливаем начальные лимиты, сетку и заголовки
        self.ax.xaxis.set_major_locator(MultipleLocator(xmal))
        self.ax.xaxis.set_minor_locator(AutoMinorLocator())
        self.ax.yaxis.set_minor_locator(AutoMinorLocator())
        self.ax.set_xlim(a1, a2)
        self.ax.set_ylim(b1, b2)
        self.ax.set_title(f"Распределение {len(Filtered)} {objs_nam} по большой полуоси. "
                          + f"{MONTH} {YEAR} года", fontsize=16)
        self.ax.set_xlabel("Большая полуось орбиты, а.е.", fontsize=16)
        self.ax.set_ylabel("Количество объектов", fontsize=16)

        # Создание панели управления снизу (GUI)
        controls_widget = QWidget()
        # Панель с полями ввода жестко фиксирует свою высоту по содержимому и не растет вверх
        controls_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        controls_layout = QHBoxLayout(controls_widget)
        controls_layout.setContentsMargins(0, 5, 0, 5)  # Ужимаем отступы внутри панели
        controls_layout.setSpacing(15)
        controls_layout.setAlignment(Qt.AlignCenter)

        # Инициализируем текстовые поля ввода с начальными значениями
        self.txt_xmin = self.create_input_field("X min:", str(a1), controls_layout)
        self.txt_xmax = self.create_input_field("X max:", str(a2), controls_layout)
        self.txt_ymin = self.create_input_field("Y min:", str(b1), controls_layout)
        self.txt_ymax = self.create_input_field("Y max:", str(b2), controls_layout)

        # Добавляем виджет управления на главный слой
        main_layout.addWidget(controls_widget)

        # Первичный вывод готового изображения на экран
        self.canvas.draw()

    def create_input_field(self, label_text, initial_value, layout):
        """Вспомогательный метод для генерации текстовых полей"""
        label = QLabel(label_text)
        font = label.font()
        font.setPointSize(10)
        label.setFont(font)

        line_edit = QLineEdit(initial_value)
        line_edit.setFixedWidth(100)
        line_edit.setFont(font)

        # Привязываем обработчик к нажатию клавиши Enter внутри поля
        line_edit.returnPressed.connect(self.update_limits)

        layout.addWidget(label)
        layout.addWidget(line_edit)
        return line_edit

    def update_limits(self):
        """Изменяет границы осей координат"""
        try:
            xmin = float(self.txt_xmin.text())
            xmax = float(self.txt_xmax.text())
            ymin = float(self.txt_ymin.text())
            ymax = float(self.txt_ymax.text())

            # Обновляем границы осей
            self.ax.set_xlim(xmin, xmax)
            self.ax.set_ylim(ymin, ymax)

            # Перерисовываем масштаб
            self.canvas.draw_idle()
        except ValueError:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
