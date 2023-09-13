# Space launches

[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![ru](https://img.shields.io/badge/lang-ru-green.svg)](README-ru.md)

* Orbital and suborbital launches counts
![Orbital and suborbital (apogee >100km) launches counts](../../../plots/launches/launches-orb-suborb-100km-linfit.png "Orbital and suborbital (apogee >100km) launches counts. Special list of marginal (orbital-energy) launches and Orbital Launch Failures are also included")
![Orbital and suborbital (apogee >80km) launches counts](../../../plots/launches/launches-orb-suborb-80km-linfit.png "Orbital and suborbital (apogee >80km) launches counts. Special list of marginal (orbital-energy) launches and Orbital Launch Failures are also included")
Data source: [J. McDowell, planet4589.org](https://planet4589.org/space/gcat/web/launch/ldes.html)

* Deep Space Launches
![Deep space launches counts](../../../plots/launches/launches-orb-deep-linfit.png "Deep space launches counts with linear regression fit. Special list of marginal (orbital-energy) launches and Orbital Launch Failures are also included")
Data source: [J. McDowell, planet4589.org; see event catalogs, deepcat (Deep Space)](https://planet4589.org/space/gcat/web/cat/);
[The Deep Space Catalog: introduction and Background, catalog description](https://www.planet4589.org/space/deepcat/).
Code: [python script with data for plotting this charts](./plot_launches_orb_suborb_graph.py)

## Dependencies

* [Matplotlib](https://matplotlib.org/)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [на русском языке](https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/)
* [Scour - an SVG Optimizer / Cleaner](https://github.com/scour-project/scour)

For all launches related images see [this directory](../../../plots/launches/)
