# Space launches

[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![ru](https://img.shields.io/badge/lang-ru-green.svg)](README-ru.md)

* Orbital and suborbital launches counts
![Orbital and suborbital (apogee >100km) launches counts](./launches-orb-suborb-100km-linfit.png "Orbital and suborbital (apogee <100km) launches counts with linear regression fits. Special list of marginal (orbital-energy) launches and Orbital Launch Failures are also included")
![Orbital and suborbital (apogee >80km) launches counts](./launches-orb-suborb-80km-linfit.png "Orbital and suborbital (apogee <80km) launches counts with linear regression fits. Special list of marginal (orbital-energy) launches and Orbital Launch Failures are also included")
Data source: [J. McDowell, planet4589.org](https://planet4589.org/space/gcat/web/launch/ldes.html)

* Deep Space Launches
![Deep space launches counts](./launches-orb-deep-linfit.png "Deep space launches counts with linear regression fits. Special list of marginal (orbital-energy) launches and Orbital Launch Failures are also included")
Data source: [J. McDowell, planet4589.org; see event catalogs, deepcat (Deep Space)](https://planet4589.org/space/gcat/web/cat/);
[The Deep Space Catalog: introduction and Background, catalog description](https://www.planet4589.org/space/deepcat/).
Code: [python script with data for plotting this charts](../../src/astrodata/launches/plot_launches_orb_suborb_graph.py)

## Image optimization applied

* [Scour](https://github.com/scour-project/scour)
* [TinyPNG: WebP, PNG, JPEG optimization](https://tinypng.com/)

For all launches related code see [this directory](../../src/astrodata/launches/)
