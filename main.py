# https://towardsdatascience.com/simple-gps-data-visualization-using-python-and-open-street-maps-50f992e9b676

'''
Bekijk de link hierboven hoe een map.png wordt aangemaakt.

map.png = mapHertsberge.png
		51.1176(lat min)
3.2561(long min)		3.3160(long max)
		51.0936(lat max)

(51.1176, 3.2561, 51.0936, 3.3160)

------------------------------------------------------------------------
Installatie op Raspberry PI

		python -m pip install numpy pandas matplotlib pillow
		
Werkt prima op de OS 64bit en OS 32bit.


Om het resultaat op een kaart, image, te zien zijn er 4 files nodig.

map.png
coordinates.csv
main.py
gps_class.py

De input van 'map.png' en 'coordinates.csv' wordt aangemaakt door 'serial_gpsXX.py' of later.

Bij het laten lopen van 'main.py' komt er een nieuwe map als resultaat 'resultMap.png' + een map '_pycache_'

'''

from gps_class import GPSVis

vis = GPSVis(data_path='coordinates.csv',
             map_path='map.png',  # Path to map downloaded from the OSM.
             points=(51.1176, 3.2561, 51.0936, 3.3160)) # Two coordinates of the map (upper left, lower right)

vis.create_image(color=(255, 0, 0), width=3)  # Set the color and the width of the GNSS tracks.

# vis.plot_map(output='save')	  # save image to 'resultMap.png'
vis.plot_map(output='plot')	  # plot image on screen

print()
