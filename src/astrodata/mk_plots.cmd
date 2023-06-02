cd stars/
python plot_sne_transients_stats.py
python plot_localized_grbs_stats.py
python plot_variable_stars_count_graph.py
python mk_vsx_count_graph.py
cd ../solarsystem/
python plot_neos_population_graph.py
python plot_mpcorb_hist.py
python mk_solsys_stats_page.py
cd ../manned/
python plot_manned_flights_rides_evas_graph.py -reafc
python plot_space_population_graph.py -faps
cd ../launches/
python plot_launches_orb_suborb_graph.py -vofmd
python plot_launches_orb_suborb_graph.py -vlofms
