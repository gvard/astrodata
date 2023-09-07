# Astronomy and space exploration data

Code for collecting and visualization of astronomical data

All code and description are avaliable at [gvard.github.io](https://gvard.github.io/)

## Solar System objects

* Near-Earth objects and Potentially Hazardous Asteroid statistics
![NEOs and PHAs cumulative statistics](./plots/solarsystem/neo_pha_graph-2002.svg)
![PHAs cumulative statistics with successfully predicted asteroid impacts](./plots/solarsystem/pha_graph_predicted_impacts-2002.svg)
[Data source: NASA Center for NEO Studies and IAU Minor Planet Center](https://cneos.jpl.nasa.gov/stats/)
* Distribution of Solar System bodies by average distance to Sun
![Distribution of minor planets by semi-major axis between Venus and Jupiter (histogram of 8000 bins)](./plots/solarsystem/asteroids-hist-a0.7-5.4.png)
![Distribution of minor planets by semi-major axis beyond Neptune (histogram of 900 bins)](./plots/solarsystem/asteroids-hist-a29-70.png)
[Data source: IAU Minor Planet Center, The MPC Orbit (MPCORB) Database](https://minorplanetcenter.net/iau/MPCORB.html)

See this links for all Solar System related [plots](./plots/solarsystem/) and [code](./src/astrodata/solarsystem/)

## Supernovae and other transients observations

* History of supernovae observations by year
![Supernovae observations](./plots/stars/sne_stats_bar_chart.svg)
* Cumulative number of supernovae
![Cumulative number of supernovae](./plots/stars/sne_transients_total_number_log_plot.svg)
[Data source: David Bishop, Latest Supernovae Archives](https://www.rochesterastronomy.org/snimages/archives.html);
[Transient Name Server stats](https://www.wis-tns.org/stats-maps).
[Data as JSON](data/stars/sne-stats.json).
[Displaying data in html page using JavaScript](https://gvard.github.io/stars/snstats/)

* History of transient observations by year from Transient Name Server
![Transient observations from Transient Name Server](./plots/stars/transient_stats_bar_chart.svg)
[Data source: Transient Name Server stats](https://www.wis-tns.org/stats-maps)

## Gamma-ray bursts observations

![Number of gamma-ray bursts which have been localized within a few hours to days to less than 1 degree](./plots/stars/grbs_total_number_plot.png)
![Gamma-ray bursts localized within a few hours to days to less than 1 degree: chart with number of optical afterglows](./plots/stars/grbs_stats_bar_chart.svg)
[Data source: Jochen Greiner; GRBs localized within a few hours to days to less than 1 degree](https://www.mpe.mpg.de/~jcg/grbgen.html), [data as JSON](data/stars/grbs-localized-stats.json).
[Displaying data in html page using JavaScript](https://gvard.github.io/grb/stats/)

See this links for all stars related [plots](./plots/stars/), [code](./src/astrodata/stars/) and [data](./data/stars/)

## Manned spaceflights

* Population of space
![Population of Space](./plots/manned/spacepop-steps.svg)
![Time Spent by Humans in Space](./plots/manned/spacepop-spent-step-filled.svg)
[Data source: J. McDowell, planet4589.org](https://planet4589.org/space/astro/web/pop.html)
* Human Spaceflight Missions, Astronauts, Rides
![Human presence in space](./plots/manned/mannedflights-astronauts-rides-evas.svg)
![Total duration and numbers of extravehicular activities](./plots/manned/evas-total-time-counts.svg)
[Data source: J. McDowell, planet4589.org](https://planet4589.org/space/astro/web/)

See this links for all manned spaceflights related [plots](./plots/manned/) and [code](./src/astrodata/manned/)

## Space launches

* Orbital and suborbital launches counts
![Orbital and suborbital launches counts](./plots/launches/launches-orb-suborb-100km.png)
[Data source: J. McDowell, planet4589.org](https://planet4589.org/space/gcat/web/launch/)
* Deep Space Launches
![Deep space launches counts](./plots/launches/launches-orb-deep.svg)
[Data source: J. McDowell, planet4589.org](https://planet4589.org/space/gcat/web/cat/)

See this links for all space launches related [plots](./plots/launches/) and [code](./src/astrodata/launches/)

## Image optimization applied

* [Scour](https://github.com/scour-project/scour)
* [SVG Cleaner](https://github.com/RazrFalcon/svgcleaner)
* [OptiPNG](https://optipng.sourceforge.net/), see [guide to PNG optimization](https://optipng.sourceforge.net/pngtech/optipng.html)
* [PNGOut](http://advsys.net/ken/utils.htm)
* [TinyPNG: WebP, PNG, JPEG optimization](https://tinypng.com/)
* [Jpegoptim](https://www.kokkonen.net/tjko/projects.html), [for Windows](https://github.com/XhmikosR/jpegoptim-windows)
* [JPEGoptim + OptiPNG + TinyPNG - оптимизация изображений](https://open-networks.ru/d/14-jpegoptim-optipng-tinypng-optimizaciya-izobrazenii)

## License

[![Media content license: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg "Media content license: CC BY 4.0. Feel free to contact me for details")](https://creativecommons.org/licenses/by/4.0/)
[![Software license: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg "Software license: GPL v3")](https://www.gnu.org/licenses/gpl-3.0)

Feel free to contact me for details. It is possible to change the license for posting on web resources (in Wikimedia projects for example).
