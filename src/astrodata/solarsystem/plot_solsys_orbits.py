"""AI (mostly) generated script for plotting orbits of solar system bodies"""

import matplotlib.pyplot as plt
import numpy as np


def solve_kepler(M, e, tol=1e-8):
    """Решение уравнения Кеплера для эксцентрической аномалии E."""
    E = M if e < 0.8 else np.pi
    while True:
        E_new = M + e * np.sin(E)
        if abs(E_new - E) < tol:
            return E_new
        E = E_new

def orbital_position(a, e, i, omega, Omega, M):
    """Вычисление позиции астероида на основе 6 параметров орбиты."""
    # Преобразование градусов в радианы
    i_rad = np.radians(i)
    omega_rad = np.radians(omega)
    Omega_rad = np.radians(Omega)
    M_rad = np.radians(M)
    
    # Решение уравнения Кеплера
    E = solve_kepler(M_rad, e)
    # Истинная аномалия
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    # Расстояние от фокуса
    r = a * (1 - e**2) / (1 + e * np.cos(nu))
    
    # Координаты в орбитальной плоскости
    x_orb = r * np.cos(nu)
    y_orb = r * np.sin(nu)
    z_orb = 0
    
    # Преобразование в эклиптическую систему координат
    cos_Omega = np.cos(Omega_rad)
    sin_Omega = np.sin(Omega_rad)
    cos_i = np.cos(i_rad)
    sin_i = np.sin(i_rad)
    cos_omega = np.cos(omega_rad)
    sin_omega = np.sin(omega_rad)
    
    x = x_orb * (cos_Omega * cos_omega - sin_Omega * sin_omega * cos_i) - y_orb * (cos_Omega * sin_omega + sin_Omega * cos_omega * cos_i)
    y = x_orb * (sin_Omega * cos_omega + cos_Omega * sin_omega * cos_i) + y_orb * (-sin_Omega * sin_omega + cos_Omega * cos_omega * cos_i)
    z = x_orb * (sin_i * sin_omega) + y_orb * (sin_i * cos_omega)
    
    return x, y, z

def plot_orbit(ax, a, e, i, omega, Omega, plane='xy', num_points=100, lw=1.5, color='b', label='Orbit'):
    """Построение орбиты астероида в заданной плоскости (xy, xz) или 3D."""
    # Преобразование градусов в радианы
    i_rad = np.radians(i)
    omega_rad = np.radians(omega)
    Omega_rad = np.radians(Omega)
    
    nu_vals = np.linspace(0, 2 * np.pi, num_points)
    x_vals = []
    y_vals = []
    z_vals = []
    
    for nu in nu_vals:
        r = a * (1 - e**2) / (1 + e * np.cos(nu))
        x_orb = r * np.cos(nu)
        y_orb = r * np.sin(nu)
        
        # Преобразование координат
        cos_Omega = np.cos(Omega_rad)
        sin_Omega = np.sin(Omega_rad)
        cos_i = np.cos(i_rad)
        sin_i = np.sin(i_rad)
        cos_omega = np.cos(omega_rad)
        sin_omega = np.sin(omega_rad)
        
        x = x_orb * (cos_Omega * cos_omega - sin_Omega * sin_omega * cos_i) - y_orb * (cos_Omega * sin_omega + sin_Omega * cos_omega * cos_i)
        y = x_orb * (sin_Omega * cos_omega + cos_Omega * sin_omega * cos_i) + y_orb * (-sin_Omega * sin_omega + cos_Omega * cos_omega * cos_i)
        z = x_orb * (sin_i * sin_omega) + y_orb * (sin_i * cos_omega)
        
        x_vals.append(x)
        y_vals.append(y)
        z_vals.append(z)
    
    if hasattr(ax, 'plot3D'):  # 3D график
        ax.plot3D(x_vals, y_vals, z_vals, color=color, label=label, lw=lw)
    else:  # 2D график
        if plane == 'xy':
            ax.plot(x_vals, y_vals, color=color, label=label, lw=lw)
        elif plane == 'xz':
            ax.plot(x_vals, z_vals, color=color, label=label, lw=lw)

# Параметры орбиты для астероида 3 Юнона (на основе данных JPL, эпоха J2000.0)
a = 2.6707  # Большая полуось
e = 0.2589  # Эксцентриситет
i = 12.980  # Наклонение
omega = 248.07  # Аргумент перицентра
Omega = 169.87  # Долгота восходящего узла
M = 0.0  # Средняя аномалия

# Juno
obj = "Juno"
a, e, i = 2.6706696, 0.2559473, 12.98651
omega, Omega, M = 247.85974, 169.82992, 172.45490

# Gonggong
obj = "Gonggong"
a, e, i = 66.8950294, 0.5031767, 30.86640
omega, Omega, M = 206.64413, 336.84008, 111.38406

# Makemake
obj = "Makemake"
a, e, i = 45.4496910, 0.1619386, 29.03386
omega, Omega, M = 296.95325, 79.25978, 168.82362

co = 4


# Параметры орбиты для Земли (на основе данных JPL, эпоха J2000.0)
a_earth = 1  # Большая полуось
e_earth = 0.016710219  # Эксцентриситет
i_earth = 0  # Наклонение
omega_earth = 282.9404  # Аргумент перицентра
Omega_earth = 174.8736  # Долгота восходящего узла
M_earth = 0.0  # Средняя аномалия

# Параметры орбиты для Марса (на основе данных JPL, эпоха J2000.0)
a_mars = 1.523679  # Большая полуось
e_mars = 0.0935  # Эксцентриситет
i_mars = 1.850  # Наклонение
omega_mars = 286.50  # Аргумент перицентра
Omega_mars = 49.578  # Долгота восходящего узла
M_mars = 0.0  # Средняя аномалия

# Параметры орбиты для Юпитера (на основе данных JPL, эпоха J2000.0)
a_jupiter = 5.2044  # Большая полуось
e_jupiter = 0.0489  # Эксцентриситет
i_jupiter = 1.304  # Наклонение
omega_jupiter = 273.87  # Аргумент перицентра
Omega_jupiter = 100.464  # Долгота восходящего узла
M_jupiter = 0.0  # Средняя аномалия


# Параметры орбиты для Нептуна (на основе данных JPL, эпоха J2000.0)
a_neptune = 30.0699  # Большая полуось
e_neptune = 0.00858587  # Эксцентриситет
i_neptune = 1.76917  # Наклонение
omega_neptune = 256.228  # 63.717  # Аргумент перицентра
Omega_neptune = 131.721  # 328.874  # Долгота восходящего узла
M_neptune = 259.883  # Средняя аномалия


# Вычисление текущей позиции Юноны
x_ast, y_ast, z_ast = orbital_position(a, e, i, omega, Omega, M)

# Построение графиков

# Первый рисунок: XY и XZ проекции
plt.figure(figsize=(16, 8))  # (16, 9)

# Первый график: проекция на эклиптику (XY-плоскость)
plt.subplot(1, 2, 1)
ax1 = plt.gca()
plot_orbit(ax1, a, e, i, omega, Omega, plane='xy', color='gray', lw=2.5, label=f'{obj} Orbit')
plot_orbit(ax1, a_earth, e_earth, i_earth, omega_earth, Omega_earth, plane='xy', color='blue', label='Earth Orbit')
plot_orbit(ax1, a_mars, e_mars, i_mars, omega_mars, Omega_mars, plane='xy', color='red', label='Mars Orbit')
plot_orbit(ax1, a_jupiter, e_jupiter, i_jupiter, omega_jupiter, Omega_jupiter, plane='xy', color='brown', lw=4, label='Jupiter Orbit')
plot_orbit(ax1, a_neptune, e_neptune, i_neptune, omega_neptune, Omega_neptune, plane='xy', color='cyan', label='Neptune Orbit')
ax1.plot([0], [0], 'ro', markersize=4, label='Sun')
ax1.plot([x_ast], [y_ast], 'go', markersize=8, label=f'{obj} Position')
ax1.axhline(y=0, linestyle='--', color='gray', alpha=0.7, label='Ecliptic Plane (Z=0)')
ax1.axvline(x=0, linestyle='--', color='gray', alpha=0.7)
ax1.axis('equal')
ax1.set_xlabel('X (AU)')
ax1.set_ylabel('Y (AU)')
ax1.set_title(f'{obj} Orbit: XY Projection (Ecliptic Plane)')
ax1.legend()
ax1.grid(True)

# Второй график: проекция в плоскость, перпендикулярную эклиптике (XZ-плоскость)
plt.subplot(1, 2, 2)
ax2 = plt.gca()
plot_orbit(ax2, a, e, i, omega, Omega, plane='xz', color='gray', lw=2.5, label=f'{obj} Orbit')
plot_orbit(ax2, a_earth, e_earth, i_earth, omega_earth, Omega_earth, plane='xz', color='blue', label='Earth Orbit')
plot_orbit(ax2, a_mars, e_mars, i_mars, omega_mars, Omega_mars, plane='xz', color='red', label='Mars Orbit')
plot_orbit(ax2, a_jupiter, e_jupiter, i_jupiter, omega_jupiter, Omega_jupiter, plane='xz', lw=4, color='brown', label='Jupiter Orbit')
plot_orbit(ax2, a_neptune, e_neptune, i_neptune, omega_neptune, Omega_neptune, plane='xz', color='cyan', label='Neptune Orbit')
ax2.plot([0], [0], 'ro', markersize=5, label='Sun')
ax2.plot([x_ast], [z_ast], 'go', markersize=8, label=f'{obj} Position')
ax2.axhline(y=0, linestyle='--', color='gray', alpha=0.7, label='Ecliptic Plane (Z=0)')
ax2.axis('equal')
ax2.set_xlabel('X (AU)')
ax2.set_ylabel('Z (AU)')
ax2.set_title(f'{obj} Orbit: XZ Projection (Perpendicular to Ecliptic)')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig(f"{obj}-orbit.png", dpi=160)

# Второй рисунок: 3D вид орбиты
plt.figure(figsize=(8, 6))
ax3 = plt.axes(projection='3d')
plot_orbit(ax3, a, e, i, omega, Omega, color='gray', lw=2, label=f'{obj} Orbit')
plot_orbit(ax3, a_earth, e_earth, i_earth, omega_earth, Omega_earth, color='blue', lw=0.8, label='Earth Orbit')
plot_orbit(ax3, a_mars, e_mars, i_mars, omega_mars, Omega_mars, color='red', lw=0.8, label='Mars Orbit')
plot_orbit(ax3, a_jupiter, e_jupiter, i_jupiter, omega_jupiter, Omega_jupiter, lw=2, color='brown', label='Jupiter Orbit')
plot_orbit(ax3, a_neptune, e_neptune, i_neptune, omega_neptune, Omega_neptune, color='cyan', lw=1.5, label='Neptune Orbit')
ax3.scatter(0, 0, 0, color='red', s=2, label='Sun')
ax3.scatter(x_ast, y_ast, z_ast, color='green', s=50, label=f'{obj} Position')
# Добавление плоскости эклиптики (Z=0)
x_range = np.linspace(-co*a_jupiter*(1+e_jupiter), co*a_jupiter*(1+e_jupiter), 10)
y_range = np.linspace(-co*a_jupiter*(1+e_jupiter), co*a_jupiter*(1+e_jupiter), 10)
X, Y = np.meshgrid(x_range, y_range)
Z = np.zeros_like(X)
ax3.plot_surface(X, Y, Z, color='gray', alpha=0.3, label='Ecliptic Plane (Z=0)')
ax3.set_xlabel('X (AU)')
ax3.set_ylabel('Y (AU)')
ax3.set_zlabel('Z (AU)')
ax3.set_title(f'{obj} Orbit: 3D View')
ax3.legend()  # loc="upper left"
# ax3.set_xlim(-6, 6)
# ax3.set_ylim(-6, 6)
# ax3.set_zlim(-6, 6)
ax3.set_box_aspect([1, 1, 1])  # Равные оси для корректного отображения

plt.tight_layout()
plt.savefig(f"{obj}-orbit-3d.png", dpi=265)
# plt.show()
