# Данные астрономии и космических исследований: сбор, анализ и визуализация

[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![ru](https://img.shields.io/badge/lang-ru-green.svg)](README-ru.md)

Больше кода, веб-страницы со статистикой и подробные описания на [gvard.github.io](https://gvard.github.io/)

## Объекты Солнечной системы

* Статистика околоземных объектов и потенциально опасных астероидов
![Статистика открытий околоземных объектов и потенциально опасных астероидов](./plots/solarsystem/neo_pha_graph-2002-ru.png "Статистика открытий околоземных объектов и потенциально опасных астероидов")
![Статистика открытий околоземных объектов с успешно предсказанными падениями на Землю](./plots/solarsystem/pha_graph_predicted_impacts-2002-ru.png "Статистика открытий околоземных объектов с успешно предсказанными падениями на Землю")
Источник данных: [NASA Center for NEO Studies and IAU Minor Planet Center](https://cneos.jpl.nasa.gov/stats/)
* Распределение тел Солнечной системы по среднему расстоянию до Солнца
![Распределение малых тел Солнечной системы по большой полуоси между Венерой и Юпитером (гистограмма из 8000 столбцов)](./plots/solarsystem/mpcorb-hist-a0.7-5.4-ru.png "Распределение малых тел Солнечной системы по большой полуоси между Венерой и Юпитером (гистограмма из 8000 столбцов)")
![Распределение малых тел Солнечной системы по большой полуоси между за Нептуном (гистограмма из 900 столбцов)](./plots/solarsystem/mpcorb-hist-a29-70-ru.png "Распределение малых тел Солнечной системы по большой полуоси между за Нептуном (гистограмма из 900 столбцов)")
Источник данных: [Центр Малых планет Международного астрономического союза, база данных The MPC Orbit (MPCORB) Database](https://minorplanetcenter.net/iau/MPCORB.html)

Все материалы по работе с данными Солнечной системы:
[иллюстрации](./plots/solarsystem/) и [код](./src/astrodata/solarsystem/)

## Наблюдения сверхновых и других транзиентов

* Динамика открытий сверхновых по годам
![Наблюдения сверхновых по годам](./plots/stars/sne_stats_bar_chart.svg "Наблюдения сверхновых по годам")
* Совокупное количество открытий сверхновых
![Совокупное количество открытий сверхновых](./plots/stars/sne_transients_total_number_log_plot.svg "Совокупное количество открытий сверхновых в логарифмическом масштабе")
Источник данных: [David Bishop, Latest Supernovae Archives](https://www.rochesterastronomy.org/snimages/archives.html);
[Статистика Transient Name Server](https://www.wis-tns.org/stats-maps).
[Данные в формате JSON](data/stars/sne-stats.json).
[html страница для их отображения с кодом на JavaScript](https://gvard.github.io/stars/snstats/)

* Динамика наблюдения транзиентов по годам, данные Transient Name Server
![Наблюдения транзиентов с Transient Name Server](./plots/stars/transient_stats_bar_chart.svg "Наблюдения транзиентов с Transient Name Server")
Источник данных: [статистика Transient Name Server](https://www.wis-tns.org/stats-maps)

## Наблюдения гамма-всплесков

![Количество гамма-всплесков, локализованных в первые часы и дни в пределах одного градуса](./plots/stars/grbs_total_number_plot.png "Количество гамма-всплесков, локализованных в первые часы и дни в пределах одного градуса")
![Динамика открытий гамма-всплесков, локализованных в первые часы и дни в пределах одного градуса: график с количеством оптических послесвечений](./plots/stars/grbs_stats_bar_chart.svg)
Источник данных: [Jochen Greiner; GRBs localized within a few hours to days to less than 1 degree](https://www.mpe.mpg.de/~jcg/grbgen.html), [данные в формате JSON](data/stars/grbs-localized-stats.json).
[html страница для их отображения с кодом на JavaScript](https://gvard.github.io/grb/stats/)

Все материалы по работе с данными о звездах:
[иллюстрации](./plots/stars/), [код](./src/astrodata/stars/) и [данные](./data/stars/)

## Пилотируемые космические полеты

* Население космоса
![Население космоса](./plots/manned/spacepop-steps-ru.png "Население космоса")
![Время, проведенное людьми в космосе](./plots/manned/spacepop-spent-steps-filled-ru.png "Время, проведенное людьми в космосе")
Источник данных: [J. McDowell, planet4589.org](https://planet4589.org/space/astro/web/pop.html)
* Пилотируемые космические миссии, количество космонавтов и посещений космоса
![Присутствие человека в космосе](./plots/manned/mannedflights-astronauts-rides-evas-ru.png "Присутствие человека в космосе")
![Количество выходов в открытый космос и полное время внекорабельной деятельности (ВКД)](./plots/manned/evas-total-time-counts-ru.png "Количество выходов в открытый космос и полное время внекорабельной деятельности (ВКД)")
Источник данных: [J. McDowell, planet4589.org](https://planet4589.org/space/astro/web/)

Все материалы по работе с данными о пилотируемых космических полетах: [иллюстрации](./plots/manned/) и [код](./src/astrodata/manned/)

## Запуски в космос

* Динамика орбитальных и суборбитальных запусков
![Орбитальные и суборбитальные запуски в космос с апогеем более 100 км](./plots/launches/launches-orb-suborb-100km-linfit-ru.png "Орбитальные и суборбитальные запуски в космос с апогеем более 100 км с линейной аппроксимацией. Красным отмечены неудачные попытки, зеленым - некаталогизированные граничные запуски")  
См. также
[Орбитальные и суборбитальные запуски в космос с апогеем более 80 км с линейной аппроксимацией](./plots/launches/launches-orb-suborb-80km-linfit-ru.png).  
Источник данных: [J. McDowell, planet4589.org](https://planet4589.org/space/gcat/web/launch/)
* Запуски в глубокий космос
![Динамика запусков в глубокий космос](./plots/launches/launches-orb-deep-linfit-ru.png "Рост числа запусков в глубокий космос с линейной аппроксимацией. Красным отмечены неудачные попытки, зеленым - некаталогизированные граничные запуски.")
Источник данных: [J. McDowell, planet4589.org, см. event catalogs, deepcat (Deep Space)](https://planet4589.org/space/gcat/web/cat/);
[The Deep Space Catalog: introduction and background, catalog description](https://www.planet4589.org/space/deepcat/).
Код: [скрипт на Python для построения этих графиков](./src/astrodata/launches/plot_launches_orb_suborb_graph.py).

Все материалы по работе с данными о запусках в космос [иллюстрации](./plots/launches/) и [код](./src/astrodata/launches/)

## Применена оптимизация изображений

* [Scour](https://github.com/scour-project/scour)
* [SVG Cleaner](https://github.com/RazrFalcon/svgcleaner)
* [OptiPNG](https://optipng.sourceforge.net/), см. [гайд по оптимизаци PNG](https://optipng.sourceforge.net/pngtech/optipng.html)
* [PNGOut](http://advsys.net/ken/utils.htm)
* [TinyPNG: оптимизация WebP, PNG, JPEG](https://tinypng.com/)
* [Jpegoptim](https://www.kokkonen.net/tjko/projects.html), [для Windows](https://github.com/XhmikosR/jpegoptim-windows)
* [JPEGoptim + OptiPNG + TinyPNG - оптимизация изображений](https://open-networks.ru/d/14-jpegoptim-optipng-tinypng-optimizaciya-izobrazenii)

## Лицензия

[![Лицензия медиаконтента: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg "Лицензия медиаконтента:  CC BY 4.0 (Creative Commons Attribution). Свяжитесь со мной для подробностей")](https://creativecommons.org/licenses/by/4.0/)
[![Лицензия программного обеспечения: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg "Лицензия программного обеспечения: GPL v3")](https://www.gnu.org/licenses/gpl-3.0)

Свяжитесь со мной для подробностей. Возможно изменение лицензии на более свободную для публикации на веб-ресурсах. Например, в проектах фонда Викимедиа.
