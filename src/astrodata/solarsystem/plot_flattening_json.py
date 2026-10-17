import json
import numpy as np
import matplotlib.pyplot as plt

with open('sizes.json', 'r', encoding='utf-8') as file:
    bodies = json.load(file)

# bodies = json.loads(data_json)
body_names = list(bodies.keys())
total_bodies = len(body_names)

# 2. Настройка сетки (по 5 элементов в строке)
cols = 5
rows = (total_bodies + cols - 1) // cols  # Округление вверх

# Создаем общее полотно для графиков
fig, axs = plt.subplots(rows, cols, figsize=(18, 4 * rows))
axs = axs.flatten()  # Превращаем матрицу осей в плоский массив для удобства

# Углы для построения окружностей и эллипсов (от 0 до 2*pi)
theta = np.linspace(0, 2 * np.pi, 300)

# 3. Отрисовка каждого небесного тела
for i, name in enumerate(body_names):
    ax = axs[i]
    info = bodies[name]

    a = info["eq_r"]     # Большая полуось (экваториальный радиус)
    b = info["po_r"]     # Малая полуось (полярный радиус)
    r_mean = info["mean_r"]
    f = info["flatt"]

    # Координаты реальной формы (эллипс)
    x_ellipse = a * np.cos(theta)
    y_ellipse = b * np.sin(theta)

    # Координаты идеального шара для сравнения (сфера)
    x_sphere = r_mean * np.cos(theta)
    y_sphere = r_mean * np.sin(theta)

    # Строим графики
    ax.plot(x_ellipse, y_ellipse, label="Форма тела", color="royalblue", lw=2.5)
    ax.plot(x_sphere, y_sphere, label="Идеальный шар", color="crimson", linestyle="--", lw=1.2)
    ax.fill(x_ellipse, y_ellipse, color="royalblue", alpha=0.1)  # Легкая заливка цветом

    # Настройка внешнего вида графика
    ax.set_title(f"{name}\n(f = {f:.4f})", fontsize=12, fontweight='bold')
    ax.set_aspect('equal', 'box')  # Важно: сохраняем пропорции осей 1:1, чтобы не искажать форму
    ax.grid(True, linestyle=":", alpha=0.5)

    # Подписи радиусов в текстовом блоке внутри подграфика
    text_info = f"Eq R: {a} км\nPo R: {b} км\nMean R: {r_mean} км"
    ax.text(0.05, 0.05, text_info, transform=ax.transAxes, fontsize=8,
            verticalalignment='bottom', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

# 4. Скрываем пустые ячейки в сетке, если они остались
for j in range(total_bodies, len(axs)):
    fig.delaxes(axs[j])

# fig.subplots_adjust(0.048, 0.06, 0.99, 0.97)

# Добавляем общую легенду и выравниваем элементы
handles, labels = axs[0].get_legend_handles_labels()
# fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 0.98), ncol=2, fontsize=11)
fig.legend(handles, labels, loc='lower right', bbox_to_anchor=(0.5, 0.98), ncol=2, fontsize=11)

# plt.suptitle("Сравнение формы небесных тел (Меридиональное сечение)", fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()

# Отображение результата
# plt.show()
plt.savefig("flateness.png", dpi=240)
