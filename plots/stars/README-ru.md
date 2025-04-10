# Звезды

[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![ru](https://img.shields.io/badge/lang-ru-green.svg)](README-ru.md)

## Переменные звезды

Bar charts with numbers of variable stars types in the General Catalog of Variable Stars (GCVS):
![Numbers of most common variable stars types in the current version of the GCVS](./gcvs_types_distribution-combined-sorted-latest+.png "Numbers of most common variable stars types in the current version of the GCVS with stars belongs to several types of variability")
Источник данных: [General Catalog of Variable Stars, latest version](http://www.sai.msu.su/gcvs/gcvs/gcvs5/gcvs5.txt),
Код: [Jupyter Notebook for plotting this chart](../../src/astrodata/stars/plot_gcvs_types_chart_latest.ipynb).

См. также [Numbers of most common variable stars types in the GCVS](./gcvs_types_distribution-combined-sorted.svg);
Источник данных: [General Catalog of Variable Stars (Samus+, 2007-2017), vartype.txt](https://cdsarc.cds.unistra.fr/ftp/B/gcvs/vartype.txt).
Код: [python script with data for plotting this charts](../../src/astrodata/stars/plot_gcvs_types_chart.py)

![Numbers of most common variable stars types in the current version of the VSX](./vsx_types_distribution-combined-sorted-latest+.png "Numbers of most common variable stars types in the current version of the VSX with stars belongs to several types of variability")
Источник данных: [The International Variable Star Index (Watson+, 2006-2007)](https://cdsarc.cds.unistra.fr/viz-bin/cat/B/vsx),
Код: [Jupyter Notebook for plotting this chart](../../src/astrodata/stars/plot_vsx_types_chart_latest.ipynb)
![Numbers of variable stars types discovered in Vorobyevy Gory](./vg_types_distribution-sorted-latest+.png "Numbers of variable stars types discovered in Vorobyevy Gory")
Источник данных: [Переменные звезды, открытые учениками ГБПОУ Воробьевы горы](https://caiko.mdp-project.ru/variability/)
![Numbers of most common variable stars types in the current versions of the GCVS and VSX](./var_types_distribution-gcvs-sorted.png "Numbers of most common variable stars types in the current versions of the GCVS and VSX")
![Numbers of most common variable stars types in the current versions of the VSX and GCVS](./var_types_distribution-vsx-sorted.png "Numbers of most common variable stars types in the current versions of the VSX and GCVS")
Код: [Jupyter Notebook for plotting this charts](../../src/astrodata/stars/plot_variable_stars_types_grouped_chart.ipynb)
![Numbers of variable stars in the GCVS, from the first edition](./gcvs-variable-stars-counts-ru.png "Numbers of variable stars in the GCVS, from the first edition")
![Numbers of variable stars, SNe and transients](./variable-stars-counts-ru.png "Numbers of variable stars (VSX and GCVS), SNe and transients")
Источник данных: [The International Variable Star Index (Watson+, 2006-2007)](https://cdsarc.u-strasbg.fr/ftp/B/vsx/ReadMe).
Код: [python script with data for plotting this charts](../../src/astrodata/stars/plot_variable_stars_counts.py)

## Звездные скопления Млечного пути

![Most common types of discovered variable stars in Milky Way clusters from the current version of the GCVS](./gcvs_types_distribution-xmatch-hunt2023-2s-combined-sorted-latest.png "Most common types of discovered variable stars in Milky Way clusters from the current version of the GCVS, cross-match with clusters members (Hunt+, 2023). Radius 2s")
См. также [results of cross-matching of clusters members with VSX variables](./vsx_types_distribution-xmatch-hunt2023-2s-combined-sorted-latest.png) and versions with other cross-matching radius.
![All known clusters in distance-age space](./clusters-dist-age-omg-annotated.png "All known open, globular clusters and moving groups in distance-age space with marked Pleiades, Hyades, Praesepe and Ruprecht 147")
Источник данных: [Improving the open cluster census. II. An all-sky cluster catalogue with Gaia DR3](https://ui.adsabs.harvard.edu/abs/2023A%26A...673A.114H/abstract),
[VizieR Online Data Catalog. Hunt+, 2023](https://cdsarc.cds.unistra.fr/viz-bin/cat/J/A+A/673/A114).
См. также [Ruprecht 147: The Oldest Nearby Open Cluster as a New Benchmark for Stellar Astrophysics](https://ui.adsabs.harvard.edu/abs/2013AJ....145..134C/abstract).
Код: [python script](../../src/astrodata/stars/plot_clusters_dist_age_distribution.py) and
[Jupyter Notebook](../../src/astrodata/stars/plot_clusters_dist_age_distribution.ipynb) for plotting this chart

## Сверхновые и другие транзиенты

* Динамика открытий сверхновых по годам
![Наблюдения сверхновых по годам](./sne_stats_bar_chart-ru.png "Наблюдения сверхновых по годам. Данные с Latest Supernovae Archives")
![Increasing number of supernova discoveries, years 2015-2023](./sne_discoveries_numbers-2015-2023.png "Increasing number of supernova discoveries, years 2015-2023. Data from the Latest Supernovae Archives")
Код: [python script with data for plotting this charts](../../src/astrodata/stars/plot_sne_discoveries_numbers.py)
* Совокупное количество открытий сверхновых
![Совокупное количество открытий сверхновых](./sne_transients_total_number_log_plot-ru.png "Совокупное количество открытий сверхновых в логарифмическом масштабе")
* History of transient observations by year from Transient Name Server
![Статистика Transient Name Server](./transient_stats_bar_chart-ru.png "Transient observations from Transient Name Server")
Источники данных: [David Bishop, Latest Supernovae Archives](https://www.rochesterastronomy.org/snimages/archives.html),
[Статистика Transient Name Server](https://www.wis-tns.org/stats-maps),
[Central Bureau for Astronomical Telegrams List of SNe](http://www.cbat.eps.harvard.edu/lists/Supernovae.html).
[Данные в формате JSON](../../data/stars/sne-stats.json).
Код: [python script with data for plotting this charts](../../src/astrodata/stars/plot_sne_transients_stats.py).
[html страница для отображения данных с кодом на JavaScript](https://gvard.github.io/stars/snstats/)

## Гамма-всплески

![Количество гамма-всплесков, локализованных в первые часы и дни в пределах одного градуса](./grbs_total_number_plot-ru.png "Количество гамма-всплесков, локализованных в первые часы и дни в пределах одного градуса")
![Динамика открытий гамма-всплесков, локализованных в первые часы и дни в пределах одного градуса: график с количеством оптических послесвечений](./grbs_stats_bar_chart-ru.png "Динамика открытий гамма-всплесков, локализованных в первые часы и дни в пределах одного градуса: график с количеством оптических послесвечений")
Источник данных: [Jochen Greiner; GRBs localized within a few hours to days to less than 1 degree](https://www.mpe.mpg.de/~jcg/grbgen.html),
[Данные в формате JSON](../../data/stars/grbs-localized-stats.json).  
Код: [python script with data for plotting this charts](../../src/astrodata/stars/plot_localized_grbs_stats.py).  
[html страница для отображения данных с кодом на JavaScript](https://gvard.github.io/grb/stats/)

## Применена оптимизация изображений

* [Scour](https://github.com/scour-project/scour)
* [TinyPNG: оптимизация WebP, PNG, JPEG](https://tinypng.com/)

Код для работы с данными по звездам [в этом каталоге](../../src/astrodata/stars/)
