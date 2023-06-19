"""Script for plotting a bar chart with types of variable stars
in the General Catalog of Variable Stars (GCVS).
Data source: https://cdsarc.cds.unistra.fr/ftp/B/gcvs/vartype.txt
"""

import os

from scour import scour
# Подключаем внешние библиотеки для создания иллюстраций и работы с данными.
# Для их установки запустить консоль (например, PowerShell) и выполнить команду
# pip install matplotlib pandas
import matplotlib.pyplot as plt
import pandas as pd


def optimize_svg(tmp_path, path):
    """Optimize svg file using scour"""
    with open(tmp_path, 'rb') as inputfile, open(path, 'wb') as outputfile:
        options = scour.generateDefaultOptions()
        options.enable_viewboxing = True
        options.strip_comments = True
        options.strip_ids = True
        options.remove_metadata = True
        options.shorten_ids = True
        options.indent_type = 'none'
        options.newlines = False
        scour.start(options, inputfile, outputfile)


# Устанавливаем переменную с минимальным количеством переменных звезд,
# чтобы отделить типы, которые будут добавлены в выборку. Остальные будут отброшены.
LIM_NUM = 125
# Читаем файл из директории Общего каталога переменных звезд (ОКПЗ), содержащий
# перепись типов переменных звезд. Указываем диапазон номеров строк с данными.

with open('../../../data/gcvs/gcvs_vartype.txt', encoding='ascii') as gcvs_types:
    data = gcvs_types.readlines()[960:1491]

# Создаем одно множество и 1 пустой словарь
types = set()
total_num = 0
types_dct = {}

# В цикле делим каждую строку по символу вертикальной черты '|',
# берем 3-е значение из результата деления выше и конвертируем взятые символы в целое число.
# берем 2-е значение из результата деления выше и обрезаем пробелы слева и справа.
# Добавляем их в списки и словарь.
for line in data:
    val = line.split('|')
    num = int(val[2])
    typ = val[1].strip()
    types.add(typ.strip(':'))
    total_num += num
    # Если двоеточия нет в названии типа и тип еще не в словаре и количество звезд больше предела,
    if ":" not in typ and typ not in types_dct and num > LIM_NUM:
        # тогда добавь значения в список и в словарь.
        types_dct[typ] = num
    # Иначе если двоеточие в названии типа и тип без двоеточия уже есть в словаре,
    elif ":" in typ and typ.strip(':') in types_dct:
        # прибавь количество переменных типа с двоеточием к количеству переменных
        # того же типа без двоеточия в словарь.
        types_dct[typ.strip(':')] += num

# Сортировка массива данных в виде словаря по значениям.
# То есть, в словаре сначала будут идти типы с наименьшим количеством переменных
types_dct = dict(sorted(types_dct.items(), key=lambda x: x[1]))

# Создаем массив данных, состоящий из списка количества звезд определенных типов
vartype_names = types_dct.keys()
data = {'Количество переменных звезд в ОКПЗ': types_dct.values()}
df = pd.DataFrame(data, index=vartype_names)
# Печатаем список названий всех типов, вошедших в выборку, их количество
# и полное количество типов в статистике
print('Типы выборки:', list(vartype_names), 'их количество:', len(vartype_names),
    'всего типов в статистике:', len(types), f'всего звезд в каталоге: {total_num}')
# Строим столбчатую диаграмму размером 16 на 9, с шириной столбцов 88%,
# подписи развернуты на 45 градусов
ax = df.plot(kind='bar', figsize=(16, 9), width=0.88, rot=45)

# Подрезаем пустые поля со всех сторон, поджимая края рисунка к подписям осей
plt.subplots_adjust(left=0.04, bottom=0.09, right=0.985, top=0.955)
# Делаем подписи осей, размер шрифта 14 пунктов, снова подрезаем пустое пространство
plt.xlabel('Типы переменных звезд', fontsize=14, labelpad=0)
plt.ylabel('Количество переменных звезд', fontsize=14, labelpad=0)
# Делаем подпись рисунка с указанием месяца и года данных статистики, размер шрифта 16 пунктов
plt.title('Распределение по типам переменных звезд в ОКПЗ. Декабрь 2016 года', fontsize=16)
# Рисуем легенду графика в верхнем левом углу
plt.legend(fontsize=14, loc='upper left')
# У каждого столбца (bar) сверху пишем числовое значение
ax.bar_label(ax.containers[-1])

# Сохраняем рисунок в векторном формате svg, его можно открыть в браузере, а также
# Добавить на слайд PowerPoint. А можно сохранить в png, jpg или ином формате
# с указанием разрешения в точках на дюйм, dpi.

FILE_EXT = 'svg'
PLT_PTH = '../../../plots/stars/gcvs_types_distribution-combined-sorted'
tmp_pth = f'{PLT_PTH}_.{FILE_EXT}'
pth = f'{PLT_PTH}.{FILE_EXT}'
plt.savefig(tmp_pth, dpi=240)
if FILE_EXT == 'svg':
    optimize_svg(tmp_pth, pth)
    os.remove(tmp_pth)
