# Запуски в космос

[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![ru](https://img.shields.io/badge/lang-ru-green.svg)](README-ru.md)

* Рост числа запусков в космос
![Орбитальные и суборбитальные запуски в космос с апогеем более 100 км](../../../plots/launches/launches-orb-suborb-100km-linfit-ru.png "Орбитальные и суборбитальные запуски в космос с апогеем более 100 км с линейной аппроксимацией. Красным отмечены неудачные попытки, зеленым - некаталогизированные граничные запуски")
![Орбитальные и суборбитальные запуски в космос с апогеем более 80 км](../../../plots/launches/launches-orb-suborb-80km-linfit-ru.png "Орбитальные и суборбитальные запуски в космос с апогеем более 80 км с линейной аппроксимацией. Красным отмечены неудачные попытки, зеленым - некаталогизированные граничные запуски")
Data source: [J. McDowell, planet4589.org](https://planet4589.org/space/gcat/web/launch/ldes.html)

* Рост числа запусков в глубокий космос
![Рост числа запусков в глубокий космос](../../../plots/launches/launches-orb-deep-linfit-ru.png "Рост числа запусков в глубокий космос с линейной аппроксимацией. Красным отмечены неудачные попытки, зеленым - некаталогизированные граничные запуски")
Data source: [J. McDowell, planet4589.org; см. event catalogs, deepcat (Deep Space)](https://planet4589.org/space/gcat/web/cat/);
[The Deep Space Catalog: introduction and Background, catalog description](https://www.planet4589.org/space/deepcat/).
Код: [скрипт на Python для построения этих графиков](./plot_launches_orb_suborb_graph.py)

## Зависимости

* [Matplotlib](https://matplotlib.org/)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [на русском языке](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/)
* [Scour - an SVG Optimizer / Cleaner](https://github.com/scour-project/scour)

Все иллюстрации по теме запуски в космос - в [этом каталоге](../../../plots/launches/)
