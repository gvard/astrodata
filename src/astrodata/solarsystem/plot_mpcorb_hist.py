"""Python script for plotting histograms with the distribution of
Solar system objects along the semimajor axis.
Data source: https://www.minorplanetcenter.net/iau/MPCORB.html
"""

import gzip
import struct
from argparse import ArgumentParser
from collections.abc import Generator
from datetime import UTC, datetime
from pathlib import Path
from typing import ClassVar

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

from plot_sso_supply import plot_vert_pla, plot_vert_resonances


class MPCOrbParser:
    FULL_LAYOUT: ClassVar[tuple[tuple[str, int, str], ...]] = (
        ("Names", 7, "U7"),
        ("H", 6, "f8"),
        ("G", 7, "f8"),
        ("Ep", 5, "U5"),
        ("M", 10, "f8"),
        ("Peri", 11, "f8"),
        ("Node", 11, "f8"),
        ("i", 11, "f8"),
        ("e", 11, "f8"),
        ("n", 12, "f8"),
        ("a", 14, "f8"),
        ("U", 2, "U1"),
        ("Ref", 10, "U10"),
        ("Obs", 6, "i4"),
        ("Opp", 4, "i4"),
        ("Arc", 10, "U9"),
        ("rms", 5, "f8"),
        ("p1", 4, "U3"),
        ("p2", 4, "U3"),
        ("Com", 11, "U10"),
        ("Flags", 5, "U4"),
        ("Desig", 28, "U27"),
        ("Last", 9, "i4"),
    )

    def __init__(self, use_columns: list[str]):
        """
        Инициализация парсера под конкретный набор колонок.
        Динамически собирает Си-строку формата для struct.unpack.
        """
        self.use_columns = use_columns

        # Генерируем маску типов данных только для запрашиваемых колонок
        self.dtype = np.dtype(
            [
                (name, npy_type)
                for name, _, npy_type in self.FULL_LAYOUT
                if name in use_columns
            ]
        )

        # Строим форматную строку для struct
        # "s" - читать байты, "x" - пропустить байты (skip)
        fmt_parts = []
        for name, width, _ in self.FULL_LAYOUT:
            if name in use_columns:
                fmt_parts.append(f"{width}s")
            else:
                fmt_parts.append(f"{width}x")

        self._struct_unpacker = struct.Struct("".join(fmt_parts)).unpack_from

    def parse(self, file_path: Path) -> np.ndarray:
        """Проход по файлу. Парсит только выбранные столбцы."""

        def _line_generator() -> Generator[tuple, None, None]:
            with gzip.open(file_path, "rb") as f:
                # Пропускаем первые 43 строки заголовка
                for _ in range(43):
                    f.readline()

                for line in f:
                    # Игнорируем пустые строки и комментарии
                    if not line.strip() or line.startswith(b"#"):
                        continue
                    try:
                        # Распаковка выбранных столбцов в байты
                        raw_parts = self._struct_unpacker(line)
                        # Декодируем и очищаем от пробелов только то, что запрошено
                        yield tuple(
                            part.decode("utf-8", errors="ignore").strip()
                            for part in raw_parts
                        )
                    except (struct.error, UnicodeDecodeError):
                        continue

        # fromiter собирает массив NumPy напрямую из Си-генератора
        return np.fromiter(_line_generator(), dtype=self.dtype)


parser = ArgumentParser(description="Graph plotter script with distribution of Solar system objects")
parser.add_argument("-t", "--translate", action="store_true",
                    help="translate all inscriptions into Russian")

args = parser.parse_args()

months_ru = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
                7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}
months_en = {i: datetime(2000, i, 1).strftime("%B") for i in range(1, 13)}

today = datetime.now(UTC)
month_str = months_ru[today.month] if args.translate else months_en[today.month]
year = today.year

base_dir = Path(__file__).resolve().parent
data_dir = base_dir / "../../../data/solarsystem"
plots_dir = base_dir / "../../../plots/solarsystem"

data_file = data_dir / "MPCORB.DAT.gz"
if not data_file.exists():
    raise FileNotFoundError(f"Missing data file: {data_file}")

USE_COLUMNS = ["a"]

parser = MPCOrbParser(use_columns=USE_COLUMNS)
data = parser.parse(data_file)

plot_configs = [
    (0.7, 5.4, 0, 6080, 1900, 0.5, False, "малых планет" if args.translate else "minor planets"),
    (29, 70, 0, 71, 900, 5.0, True, "транснептуновых объектов" if args.translate else "TNOs")
]

for a1, a2, b1, b2, bins, xmal, plot_tno, objs_nam in plot_configs:
    filtered_data = data[(data["a"] >= a1) & (data["a"] <= a2)]

    fig, ax = plt.subplots(figsize=(16, 9))
    fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)

    ax.xaxis.set_major_locator(MultipleLocator(xmal))
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    plt.hist(filtered_data["a"], bins=bins)

    plot_vert_pla(b1, b2, show_inner_asteroids=not plot_tno)
    plot_vert_resonances(b1, b2, plot_tno=plot_tno)

    plt.xlim(a1, a2)
    plt.ylim(b1, b2)

    if args.translate:
        plt.title(f"Распределение {len(filtered_data)} {objs_nam} по большой полуоси. {month_str} {year} года", fontsize=15)
        plt.xlabel("Большая полуось орбиты, а.е.", fontsize=14)
        plt.ylabel("Количество объектов", fontsize=14)
    else:
        plt.title(f"Distribution of {len(filtered_data)} {objs_nam} by semi-major axis. {month_str} {year}", fontsize=15)
        plt.xlabel("Semi-major axis, au", fontsize=14)
        plt.ylabel("Number of objects", fontsize=14)

    lang_suffix = "-ru" if args.translate else ""
    save_path = plots_dir / f"mpcorb-hist-a{a1}-{a2}{lang_suffix}.png"
    plt.savefig(save_path, dpi=160)
    plt.close(fig)
