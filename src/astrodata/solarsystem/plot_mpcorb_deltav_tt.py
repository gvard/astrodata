import gzip
import struct
from argparse import ArgumentParser
from collections.abc import Generator
from datetime import UTC, datetime
from pathlib import Path
from typing import ClassVar, Final

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

from deltav import (
    DVArray2,
    DVArray3,
    Travel2Array,
    Travel3Array,
    best,
)
from plot_config import PLOT_PRESETS
from plot_sso_supply import PL, VISITED, plot_vert_pla


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
        ("U", 2, "i4"),
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
        self.use_columns = use_columns

        # dtype строится строго по порядку из use_columns,
        # чтобы np.fromiter правильно сопоставлял генерируемые кортежи
        layout_dict_types = {name: npy_type for name, _, npy_type in self.FULL_LAYOUT}
        self.dtype = np.dtype(
            [
                (name, layout_dict_types[name])
                for name in use_columns
                if name in layout_dict_types
            ]
        )

        # Распаковщик всегда читает все колонки подряд из строки по спецификации MPC
        fmt_parts = [f"{width}s" for _, width, _ in self.FULL_LAYOUT]
        self._struct_unpacker = struct.Struct("".join(fmt_parts)).unpack_from

        # Запоминаем имена всех колонок, чтобы делать из распакованного кортежа словарь
        self._all_column_names = [name for name, _, _ in self.FULL_LAYOUT]

    def parse(self, file_path: Path) -> np.ndarray:
        """Полный проход по файлу с динамическим обновлением орбит крупных ТНО."""
        from collections import defaultdict

        mpc_lookup = defaultdict(list)

        for body in PL.values():
            if body.mpc_id:
                mpc_lookup[body.mpc_id].append(body)

        for body in VISITED.values():
            if body.mpc_id:
                mpc_lookup[body.mpc_id].append(body)

        def _line_generator() -> Generator[tuple, None, None]:
            with gzip.open(file_path, "rb") as f:
                for _ in range(43):
                    f.readline()

                for line in f:
                    if not line.strip() or line.startswith(b"#"):
                        continue
                    try:
                        # Распаковываем абсолютно все колонки в сыром виде
                        raw_parts = self._struct_unpacker(line)

                        # Создаем словарь {ИмяКолонки: Значение} для удобного обращения по имени
                        row_dict = {
                            name: part.decode("utf-8", errors="ignore").strip()
                            for name, part in zip(self._all_column_names, raw_parts, strict=True)
                        }

                        # Безопасная обработка колонки "U" по её имени, а не по индексу
                        u_val = row_dict.get("U", "")
                        row_dict["U"] = int(u_val) if u_val.isdigit() else -1

                        # Динамическое обновление PL и VISITED
                        line_desig = line[166:194].decode("utf-8", errors="ignore").strip()
                        if line_desig in mpc_lookup:
                            line_a = float(line[91:105].decode("utf-8", errors="ignore").strip())
                            # Перебираем все связанные объекты (и в PL, и в VISITED) и обновляем им "a"
                            for body in mpc_lookup[line_desig]:
                                body.a = line_a

                        # Собираем финальный кортеж строго в том порядке, который задан в use_columns
                        yield tuple(row_dict[col] for col in self.use_columns)

                    except (struct.error, ValueError, UnicodeDecodeError):
                        continue

        return np.fromiter(_line_generator(), dtype=self.dtype)


def do_calcs(data_matrix: np.ndarray, alim: float = 5.0) -> np.ndarray:
    """Computes delta-V budgets, times-of-flight, and optimizes the mission profile."""
    if VERBOSE:
        print("Calculating Trajectories & Delta-Vs...")

    Results = [DeltaVCalc(DVArray3, data_matrix),
               DeltaVCalc(DVArray2, data_matrix)]

    if VERBOSE:
        print("Calculating Travel Times...")

    TravelTimes = np.asarray(
        (
            np.apply_along_axis(Travel3Array, 1, data_matrix),
            np.apply_along_axis(Travel2Array, 1, data_matrix),
        )
    ).T

    if VERBOSE:
        print("Travel Time Calculations Complete")
        # print("Creating Output Datafile...")

    ResultTableTemp1 = npappend(data_matrix, Results[0])
    ResultTableTemp2 = npappend(ResultTableTemp1, TravelTimes[:, 0])
    ResultTableTemp3 = npappend(ResultTableTemp2, Results[1])
    ResultTable = npappend(ResultTableTemp3, TravelTimes[:, 1])

    # Задаем штраф: например, 5 м/с за каждый лишний день полёта
    if alim < 5.0:
        W_TOF_NASA = 5.0   # Для внутренней системы и пояса астероидов (до Юпитера)
    elif alim < 30.0:
        W_TOF_NASA = 0.5   # Для систем Сатурна, Урана и Нептуна
    else:
        W_TOF_NASA = 0.05  # Для Пояса Койпера и ТНО


    MinResult = np.apply_along_axis(best, 1, ResultTable, w_tof=W_TOF_NASA)
    FullResultTable = np.hstack((ResultTable, MinResult))

    return FullResultTable


def DeltaVCalc(DVArray, InputData):
    return np.apply_along_axis(DVArray, 1, InputData)


def npappend(data, arr):
    return np.append(data.T, [arr], axis=0).T


parser = ArgumentParser(description="Graph plotter script with distribution of Solar system objects")
parser.add_argument("-t", "--translate", action="store_true",
                    help="translate all inscriptions into Russian")

args = parser.parse_args()

VERBOSE: Final[bool] = True
PRINT_EXTREME: Final[bool] = True

# SORTIND = 5  # 5 for a, 10 for deltaV (dv), 11 for Travel Time (tt)
NUM_SKIP_HEAD: Final[int] = 43

months_ru = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
                7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}
months_en = {i: datetime(2000, i, 1).strftime("%B") for i in range(1, 13)}

today = datetime.now(UTC)
MONTH = months_ru[today.month] if args.translate else months_en[today.month]
YEAR = today.year

base_dir = Path(__file__).resolve().parent
data_dir = base_dir / "../../../data/solarsystem"
plots_dir = base_dir / "../../../plots/solarsystem"

data_file = data_dir / "MPCORB.DAT.gz"
if not data_file.exists():
    raise FileNotFoundError(f"Missing data file: {data_file}")

# MPCORB_URL = "http://www.minorplanetcenter.net/iau/MPCORB/MPCORB.DAT.gz"

if VERBOSE:
    print("Importing Data...")

USE_COLUMNS = ["Names", "U", "p2", "Peri", "i", "e", "a", "Desig"]
parser = MPCOrbParser(use_columns=USE_COLUMNS)
rawdata = parser.parse(data_file)

# alim = (0.592, 2.928)
alim = (0.592, 5.299)
requested_plots = [("deltav", 0.59, 2.9), ("tt", 0.59, 2.9), ("deltav", 0.59, 5.3), ("tt", 0.59, 5.3)]

Filtered = rawdata[
    (rawdata["U"] < 7)
]
Filtered = Filtered[Filtered["Names"] != "\n"]

a_shift = 0.0
Filtered = Filtered[
    (Filtered["a"] >= alim[0] - a_shift) &
    (Filtered["a"] <= alim[1] + a_shift)
]
print(f"Objects after filtering: {len(Filtered)}")

ind = np.argsort(Filtered["a"])
Filtered = Filtered[ind]

indices = np.where(Filtered["a"] >= alim[1] + 0.1)[0]
a1 = int(indices.min()) if indices.size > 0 else len(Filtered)
a0 = 0
data = Filtered["a"][a0:a1]

print(f"Data length when filtered {a0}:{a1}", len(data))

NAMES = np.array(Filtered[["Names", "U"]].tolist())
DATA = np.array(Filtered[["Peri", "i", "e", "a"]].tolist())

FullResultTable = do_calcs(DATA, alim=alim[1])

visited_mpc_ids = [body.mpc_id for body in VISITED.values() if body.mpc_id]
visited_mask_global = np.isin(Filtered["Desig"], visited_mpc_ids)
FullResultTable_visited = FullResultTable[visited_mask_global]
# Фильтруем, оставляя только те тела, которые попадают в текущий диапазон xlim
# Колонка 3 в FullResultTable — это большая полуось "a"
in_xlim_mask = (FullResultTable_visited[:, 3] >= alim[0]) & (
    FullResultTable_visited[:, 3] <= alim[1]
)
FullResultTable_visited = FullResultTable_visited[in_xlim_mask]

if PRINT_EXTREME:
    def print_objects_table(title: str, table_matrix: np.ndarray, filtered_matrix: np.ndarray) -> None:
        """Prints a beautifully formatted text table of asteroid transit metrics."""
        print(f"\n=== {title} ===")
        header = f"{'Designation / Name':<24} | {'U':<1} | {'a, AU':<7} | {'e':<5} | {'i, deg':<6} | {'Best Δv, m/s':<12} | {'Best ToF, d.':<12} | {'Mode':<4}"
        print(header)
        print("-" * len(header))

        for row_res, row_filt in zip(table_matrix, filtered_matrix, strict=True):
            # Safe extraction of designations and names from MPC structured records
            obj_desig = row_filt["Desig"].strip()
            # obj_name = row_filt["Names"].strip()
            full_identity = f"{obj_desig}"

            # Orbit uncertainty parameter execution
            u_parameter = row_filt["U"]
            u_str = str(u_parameter) if u_parameter != -1 else "?"

            # Extract ballistic profiles safely from the target row segment
            a_val = row_res[3]
            e_val = row_res[2]
            i_val = row_res[1]
            best_dv = row_res[8]
            best_tof = row_res[9]
            mode_selected = int(row_res[10])

            print(f"{full_identity:<24} | {u_str:<1} | {a_val:<7.3f} | {e_val:<5.3f} | {i_val:<6.2f} | {best_dv:<12.1f} | {best_tof:<12.1f} | {mode_selected}ᴾ")

    # Preparation of Dataset Filters ---
    # Extract the full working subset matching the current semi-major axis bounding zone
    working_results = FullResultTable[a0:a1]
    working_filtered = Filtered[a0:a1]

    # Create a strict mask to select only highly reliable orbits (U parameter < 6)
    u_mask = working_filtered["U"] < 6
    res_u_cleared = working_results[u_mask]
    filt_u_cleared = working_filtered[u_mask]

    # Generation of Requested Sorted Subsets ---
    # Sort criteria definitions based on matrix positions: 8 is Delta-V, 9 is Travel Time
    idx_dv_asc = np.argsort(res_u_cleared[:, 8])
    idx_tt_asc = np.argsort(res_u_cleared[:, 9])

    NUM_EXTREMES: Final[int] = 25

    # 1) NUM_EXTREMES objects with the lowest delta V and U < 6
    print_objects_table(
        "25 OBJECTS: LOWEST DELTA-V (U < 6)",
        res_u_cleared[idx_dv_asc][:NUM_EXTREMES],
        filt_u_cleared[idx_dv_asc][:NUM_EXTREMES]
    )
    print("\n" + "=" * 60)

    # 2) NUM_EXTREMES objects with the highest delta V and U < 6
    print_objects_table(
        "25 OBJECTS: HIGHEST DELTA-V (U < 6)",
        res_u_cleared[idx_dv_asc][-NUM_EXTREMES:],
        filt_u_cleared[idx_dv_asc][-NUM_EXTREMES:]
    )
    print("\n" + "=" * 60)

    # 3) NUM_EXTREMES objects with the lowest travel time and U < 6
    print_objects_table(
        "25 OBJECTS: LEAST TRAVEL TIME (U < 6)",
        res_u_cleared[idx_tt_asc][:NUM_EXTREMES],
        filt_u_cleared[idx_tt_asc][:NUM_EXTREMES]
    )
    print("\n" + "=" * 60)

    # 4) NUM_EXTREMES objects with the highest travel time and U < 6
    print_objects_table(
        "25 OBJECTS: GREATEST TRAVEL TIME (U < 6)",
        res_u_cleared[idx_tt_asc][-NUM_EXTREMES:],
        filt_u_cleared[idx_tt_asc][-NUM_EXTREMES:]
    )
    print("\n" + "=" * 60 + "\n")

data = FullResultTable[a0:a1]
ind = np.argsort(data[:, 8])
data = data[ind]

# MOON_FLIGHT_DV_LOWEST: Final[int] = 3100
# MOON_FLIGHT_DV: Final[int] = 3140
MARS_FLIGHT_DV: Final[int] = 3600
MOON_LOW_ORBIT_DV: Final[int] = 3959
MARS_LOW_ORBIT_DV: Final[int] = 5776
MOON_LANDING_DV: Final[int] = 5897
MARS_TRIP_TT: Final[int] = 244
POLYAKOV_FLIGHT_DURATION: Final[float] = 437.749

for mode, min_a, max_a in requested_plots:
    plot_cfg = PLOT_PRESETS.get((mode, min_a, max_a))
    if not plot_cfg:
        print(f"Конфигурация для {mode} при a={max_a} не найдена.")
        continue

    fig, ax = plt.subplots(figsize=(16, 9))
    fig.subplots_adjust(0.054, 0.06, 0.99, 0.97)  # 0.055, 0.048

    if plot_cfg.mode == "deltav":
        ax.xaxis.set_major_locator(MultipleLocator(plot_cfg.x_maj_loc))
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

        under_limit_idx = np.where(data[:, 8] <= plot_cfg.threshold_value)[0]
        c0 = int(under_limit_idx.max()) if under_limit_idx.size > 0 else 0
        plt.plot(data[:, 3], data[:, 8], ".", ms=2, color="#555")  # "grey"
        print("length of delta v data:", len(data[:, 3]), len(NAMES))

        plt.plot(data[:c0, 3], data[:c0, 8], ".k", ms=2)
        # plt.plot(plot_cfg.xlim, (MOON_FLIGHT_DV_LOWEST, MOON_FLIGHT_DV_LOWEST), "--m", lw=0.8)
        # plt.plot(plot_cfg.xlim, (MOON_FLIGHT_DV, MOON_FLIGHT_DV), "--m", lw=0.8)
        plt.plot(plot_cfg.xlim, (MOON_LOW_ORBIT_DV, MOON_LOW_ORBIT_DV), "--m")
        plt.plot(plot_cfg.xlim, (MOON_LANDING_DV, MOON_LANDING_DV), "--m", lw=0.8)
        plt.plot(plot_cfg.xlim, (MARS_FLIGHT_DV, MARS_FLIGHT_DV), "--r", lw=0.8)
        plt.plot(plot_cfg.xlim, (MARS_LOW_ORBIT_DV, MARS_LOW_ORBIT_DV), "--r")

        ax.text(
            0.6,
            MARS_LOW_ORBIT_DV + 220,
            "Δv для Марса",
            fontsize=13,
            bbox={
                "facecolor": "white",
                "alpha": 0.8,
                "edgecolor": "none",
                "pad": 0,
            },
        )
        ax.text(
            0.6,
            MOON_LOW_ORBIT_DV + 220,
            "Δv для Луны",
            fontsize=13,
            bbox={
                "facecolor": "white",
                "alpha": 0.8,
                "edgecolor": "none",
                "pad": 0,
            },
        )

        plt.plot(
            FullResultTable_visited[:, 3],
            FullResultTable_visited[:, 8],
            "*",
            ms=12,
            color="orangered",
            markeredgecolor="black",
            markeredgewidth=0.85,
            label="Астероиды – цели космических миссий",
            zorder=9,
        )

        for row in FullResultTable_visited:
            body_a = row[3]  # Большая полуось "a"
            body_dv = row[8]  # Характеристическая скорость "dv"

            # Находим соответствующий объект в VISITED по совпадению mpc_id
            # (или по значению "a", так как мы обновили их в MPCOrbParser)
            body_obj = next((b for b in VISITED.values() if b.a == body_a), None)
            if body_obj is None:
                continue

            dx: float = 0.013
            dy: float = 400
            text_color, bg_color = "black", "white"
            if (mode, min_a, max_a) in body_obj.plot_configs:
                body_cfg = body_obj.plot_configs[(mode, min_a, max_a)]
                dx, dy, text_color, bg_color = body_cfg.dx, body_cfg.dy, body_cfg.color, body_cfg.bg_color

            ax.text(
                body_a + dx,
                body_dv + dy,
                body_obj.runame,
                color=text_color,
                fontsize=11,
                va="center",
                bbox={
                    "facecolor": bg_color,
                    "alpha": 0.83,
                    "edgecolor": "none",
                    "pad": 0.0,
                },
            )

        plt.ylabel(plot_cfg.ylabel, fontsize=14)
        desc = "характеристической скорости"
        print("Filtered by 9", c0)
        plt.title(
            f"Характеристическая скорость орбитального маневра для {len(data[:c0, 9])} из {len(data[:, 3])} астероидов. {MONTH} {YEAR} года",
            fontsize=15,
        )
        plt.legend(loc=plot_cfg.legend_loc)

    elif plot_cfg.mode == "tt":
        ax.xaxis.set_major_locator(MultipleLocator(plot_cfg.x_maj_loc))
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

        # Автоматические подписи с индивидуальными поправками (Time of Flight)
        for row in FullResultTable_visited:
            body_a, body_val = row[3], row[9]  # Извлекаем "a" и "tt"
            body_obj = next((b for b in VISITED.values() if b.a == body_a), None)
            if body_obj is None:
                continue

            # Задаем значения по умолчанию для текущего режима (например, mode = "deltav")
            dx, dy = 0.01, 20
            text_color, bg_color = "black", "white"

            # Ищем конфигурацию внутри объекта небесного тела
            if (mode, min_a, max_a) in body_obj.plot_configs:
                body_cfg = body_obj.plot_configs[(mode, min_a, max_a)]
                dx, dy, text_color, bg_color = body_cfg.dx, body_cfg.dy, body_cfg.color, body_cfg.bg_color

            ax.text(
                body_a + dx,
                body_val + dy,
                body_obj.runame,
                color=text_color,
                fontsize=11,
                va="center",
                bbox={
                    "facecolor": bg_color,
                    "alpha": 0.83,
                    "edgecolor": "none",
                    "pad": 0.0,
                },
            )

        greys = data[data[:, 9] <= plot_cfg.threshold_value]
        plt.plot(data[:, 3], data[:, 9], ".", ms=2, color="#555")
        plt.plot(greys[:, 3], greys[:, 9], ".k", ms=2)
        plt.plot(
            FullResultTable_visited[:, 3],
            FullResultTable_visited[:, 9],
            "*",
            ms=12,
            color="orangered",
            markeredgecolor="black",
            markeredgewidth=0.85,
            label="Астероиды – цели космических миссий",
            zorder=9,
        )
        print(f"only if tt < {MARS_TRIP_TT} d: {len(greys)}, len: {len(data[:, 3])}")
        plt.ylabel(plot_cfg.ylabel, fontsize=14)
        desc = "времени полета"
        plt.title(
            f"Время полета для {len(greys)} из {len(data[:, 3])} астероидов. {MONTH} {YEAR} года",
            fontsize=15,
        )

        ax.text(
            0.6,
            POLYAKOV_FLIGHT_DURATION + 6,
            "Рекорд длительности космического полета",
            fontsize=13,
            bbox={
                "facecolor": "white",
                "alpha": 0.7,
                "edgecolor": "none",
                "pad": 0,
            },
        )
        ax.text(
            0.6,
            POLYAKOV_FLIGHT_DURATION / 2 + 6,
            "Полет с возвратом",
            fontsize=13,
            bbox={
                "facecolor": "white",
                "alpha": 0.7,
                "edgecolor": "none",
                "pad": 0,
            },
        )
        ax.text(
            0.6,
            MARS_TRIP_TT + 6,
            "Полет на Марс",
            fontsize=13,
            bbox={
                "facecolor": "white",
                "alpha": 0.7,
                "edgecolor": "none",
                "pad": 0,
            },
        )
        plt.plot(plot_cfg.xlim, (MARS_TRIP_TT, MARS_TRIP_TT), "--m")
        plt.plot(plot_cfg.xlim, (POLYAKOV_FLIGHT_DURATION / 2, POLYAKOV_FLIGHT_DURATION / 2), "--m", lw=1)
        plt.plot(plot_cfg.xlim, (POLYAKOV_FLIGHT_DURATION, POLYAKOV_FLIGHT_DURATION), "--m", lw=0.8)
        plt.legend(loc=plot_cfg.legend_loc)

    print(mode, "xlim", plot_cfg.xlim, "ylim", plot_cfg.ylim)

    plot_vert_pla(ax, plot_cfg.xlim, plot_cfg.ylim, xoff=0.009, show_inner_asteroids=False)

    plt.xlim(plot_cfg.xlim)
    plt.ylim(plot_cfg.ylim)
    plt.xlabel("Большая полуось орбиты, а.е.", fontsize=14)
    lang_suffix = "-ru" if args.translate else ""
    plt.savefig(
        plots_dir / f"mpcprb-{mode}-a{round(plot_cfg.xlim[0], 1)}-{round(plot_cfg.xlim[1], 1)}{lang_suffix}-.png",
        dpi=160,
    )
    plt.close(fig)
