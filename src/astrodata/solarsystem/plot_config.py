from dataclasses import dataclass
from typing import Literal

MARS_LOW_ORBIT_DV: int = 5776
# MOON_LOW_ORBIT_DV: int = 3959
MARS_TRIP_TT: int = 244

@dataclass(frozen=True, slots=True)
class PlotModeConfig:
    mode: Literal["deltav", "tt"]
    xlim: tuple[float, float]
    ylim: tuple[float, float]
    ylabel: str
    threshold_value: float
    x_maj_loc: float = 0.1
    legend_loc: str = "upper right"

PLOT_PRESETS: dict[tuple[Literal["deltav", "tt"], float, float], PlotModeConfig] = {
    ("deltav", 0.59, 2.9): PlotModeConfig(
        mode="deltav",
        xlim=(0.592, 2.928),
        ylim=(3260, 33000),
        ylabel="Δv, м/с",
        threshold_value=MARS_LOW_ORBIT_DV,
    ),
    ("tt", 0.59, 2.9): PlotModeConfig(
        mode="tt",
        xlim=(0.592, 2.928),
        ylim=(138, 790),
        legend_loc = "lower right",
        ylabel="Время полета, дни",
        threshold_value=MARS_TRIP_TT,
    ),
    ("deltav", 0.59, 5.3): PlotModeConfig(
        mode="deltav",
        xlim=(0.592, 5.299),
        ylim=(3260, 33000),
        x_maj_loc=0.2,
        legend_loc="upper center",
        ylabel="Δv, м/с",
        threshold_value=MARS_LOW_ORBIT_DV,
    ),
    ("tt", 0.59, 5.3): PlotModeConfig(
        mode="tt",
        xlim=(0.592, 5.299),
        ylim=(138, 1520),
        x_maj_loc=0.2,
        legend_loc="upper center",
        ylabel="Время полета, дни",
        threshold_value=MARS_TRIP_TT,
    ),
}
