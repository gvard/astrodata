# Статистика пилотируемых космических полетов

[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![ru](https://img.shields.io/badge/lang-ru-green.svg)](README-ru.md)

* Население космоса
![Население космоса](../../../plots/manned/spacepop-steps-ru.png "Население космоса")
![Время, проведенное людьми в космосе](../../../plots/manned/spacepop-spent-steps-filled-ru.png "Время, проведенное людьми в космосе")
Данные: [J. McDowell, planet4589.org](https://planet4589.org/space/astro/web/pop.html)
* Пилотируемые космические миссии, количество космонавтов и посещений космоса
![Присутствие человека в космосе](../../../plots/manned/mannedflights-astronauts-rides-evas-ru.png "Присутствие человека в космосе")
Данные: [J. McDowell, planet4589.org](https://planet4589.org/space/astro/web/)
* Внекорабельная деятельность (ВКД)
![Количество выходов в открытый космос и полное время внекорабельной деятельности (ВКД)](../../../plots/manned/evas-total-time-counts-ru.png "Количество выходов в открытый космос и полное время внекорабельной деятельности (ВКД)")
![Количество выходов в открытый космос (ВКД)](../../../plots/manned/evas-total-counts.svg "Количество выходов в открытый космос (ВКД)")
![Суммарное время всех выходов в открытый космос (внекорабельной деятельности, ВКД)](../../../plots/manned/evas-total-time.svg "Суммарное время всех выходов в открытый космос (внекорабельной деятельности, ВКД)")
Данные: [J. McDowell, planet4589.org](https://planet4589.org/space/astro/web/),
[описание и определения терминов](https://planet4589.org/space/astro/web/evas.html).  
Обратите внимание: ВКД (выход в открытый космос) в этих данных определяется как деятельность, выполняемая в условиях вакуума (давление окружающей среды менее 50 мбар или 5 кПа), защищенная только скафандром.

## Зависимости

* [Matplotlib](https://matplotlib.org/)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [на русском языке](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/)
* [Scour - an SVG Optimizer / Cleaner](https://github.com/scour-project/scour)

Визуализация данных по пилотируемым полетам [в этом каталоге](../../src/astrodata/manned/)
