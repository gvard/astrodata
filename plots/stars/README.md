# Stars related plots

## Variable stars statistics

* Bar charts with numbers of variable stars types in the General Catalog of Variable Stars (GCVS).
![Numbers of most common variable stars types in the GCVS](./gcvs_types_distribution-combined-sorted.svg "Numbers of most common variable stars types in the GCVS")
[Data source: General Catalog of Variable Stars (Samus+, 2007-2017), vartype.txt](https://cdsarc.cds.unistra.fr/ftp/B/gcvs/vartype.txt)
[python script with data for plotting this charts](../../src/astrodata/stars/plot_gcvs_types_chart.py)
![Numbers of most common variable stars types in the current version of the GCVS](./gcvs_types_distribution-combined-sorted-latest+.png "Numbers of most common variable stars types in the current version of the GCVS with stars belongs to several types of variability")
[Data source: General Catalog of Variable Stars, latest version](http://www.sai.msu.su/gcvs/gcvs/gcvs5/gcvs5.txt),
[Jupyter Notebook for plotting this chart](../../src/astrodata/stars/plot_gcvs_types_chart_latest.ipynb)
![Numbers of most common variable stars types in the current version of the VSX](./vsx_types_distribution-combined-sorted-latest+.png "Numbers of most common variable stars types in the current version of the VSX with stars belongs to several types of variability")
[Data source: The International Variable Star Index (Watson+, 2006-2007)](https://cdsarc.cds.unistra.fr/viz-bin/cat/B/vsx),
[Jupyter Notebook for plotting this chart](../../src/astrodata/stars/plot_vsx_types_chart_latest.ipynb)
![Numbers of variable stars types discovered in Vorobyevy Gory](./vg_types_distribution-sorted-latest+.png "Numbers of variable stars types discovered in Vorobyevy Gory")
[Data source: Переменные звезды, открытые учениками ГБПОУ Воробьевы горы](https://caiko.mdp-project.ru/variability/)
![Numbers of most common variable stars types in the current versions of the GCVS and VSX](./var_types_distribution-gcvs-sorted.png "Numbers of most common variable stars types in the current versions of the GCVS and VSX")
![Numbers of most common variable stars types in the current versions of the VSX and GCVS](./var_types_distribution-vsx-sorted.png "Numbers of most common variable stars types in the current versions of the VSX and GCVS")
[Jupyter Notebook for plotting this charts](../../src/astrodata/stars/plot_variable_stars_types_grouped_chart.ipynb)
![Numbers of variable stars in the GCVS, from the first edition](./gcvs-variable-stars-count.svg "Numbers of variable stars in the GCVS, from the first edition")
![Numbers of variable stars, SNe and transients](./variable-stars-count-graph.svg "Numbers of variable stars (VSX and GCVS), SNe and transients")
[Data source: The International Variable Star Index (Watson+, 2006-2007)](https://cdsarc.u-strasbg.fr/ftp/B/vsx/ReadMe),
[python script with data for plotting this charts](../../src/astrodata/stars/plot_variable_stars_counts.py)

## Supernova observations

* History of supernovae observations by year
![Supernovae observations](./sne_stats_bar_chart.svg "Supernovae observations")
* Cumulative number of supernovae
![Cumulative number of supernovae](./sne_transients_total_number_log_plot.svg "Cumulative number of supernovae")
* History of transient observations by year from Transient Name Server
![Transient observations from Transient Name Server](./transient_stats_bar_chart.svg "Transient observations from Transient Name Server")
[Data sources: David Bishop, Latest Supernovae Archives](https://www.rochesterastronomy.org/snimages/archives.html),
[Transient Name Server stats](https://www.wis-tns.org/stats-maps),
[Central Bureau for Astronomical Telegrams List of SNe](http://www.cbat.eps.harvard.edu/lists/Supernovae.html).
[Python script with data for plotting this charts](../../src/astrodata/stars/plot_sne_transients_stats.py)

## Gamma-ray bursts observations

![Number of gamma-ray bursts which have been localized within a few hours to days to less than 1 degree](./grbs_total_number_plot.png "Number of gamma-ray bursts which have been localized within a few hours to days to less than 1 degree")
![Gamma-ray bursts localized within a few hours to days to less than 1 degree: chart with number of optical afterglows](./grbs_stats_bar_chart.svg "Gamma-ray bursts localized within a few hours to days to less than 1 degree: chart with number of optical afterglows")
[Data source: Jochen Greiner; GRBs localized within a few hours to days to less than 1 degree](https://www.mpe.mpg.de/~jcg/grbgen.html)
[Python script with data for plotting this charts](../../src/astrodata/stars/plot_localized_grbs_stats.py)

## Image optimization applied

* [Scour](https://github.com/scour-project/scour)
* [TinyPNG: WebP, PNG, JPEG optimization](https://tinypng.com/)

For all stars related code see [this directory](../../src/astrodata/stars/)
