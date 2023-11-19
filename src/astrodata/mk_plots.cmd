cd stars/
python plot_sne_transients_stats.py -t
python plot_localized_grbs_stats.py -st
python plot_variable_stars_counts.py -t
cd ../solarsystem/
python plot_neos_population_graph.py -t
python plot_mpcorb_hist.py -t
python plot_close_approaches.py
cd ../manned/
python plot_manned_flights_rides_evas_graph.py -reafct
python plot_space_population_graph.py -fapst
cd ../launches/
python plot_launches_orb_suborb_graph.py -vofmdrt
python plot_launches_orb_suborb_graph.py -vlofmsrt
python plot_launches_orb_suborb_graph.py -vlofmsrt -e 80
