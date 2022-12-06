# NMEA0183DECODER met Raspberry PI
## Beschrijving
DEEL1. 

Decodeert de data afkomstig van een GPS-module naar een leesbare vorm. Deze data is gecodeerd volgens NMEA0183 protocol.

Iedere seconde stuurt de GPS een reeks lijnen naar buiten met data op een snelheid van 9600 baud.

De inhoud en samenstelling wordt uitgelegd in bijlage NMEA0183.pdf

Het programma neemt de data binnen via de serial0-bus op GPIO15 split deze en maakt de volgende variabelen: 

datum, time, latitude, longitude, altitude, snelheid, richting en aantal sat.

Er zijn gps-modules die enkel de US-satellieten ontvangen anderen ook de Chineese, Russische, Europese.

In het eerste geval begint de lijn met GPxxx in het andere geval GNxxx. Dit programma werkt met beidie type modules.

Het programma 'serial_gpsXX.py' maakt 2 files aan. 'GPSdata.csv' en bevat respectivelijk 'datum, time, latitude, longitude, altitude, snelheid, richting en aantal sat'
de andere file 'coordinates.csv' bevat enkel 'latitude, longitude'. De files worden iedere 60 seconden aangevuld.
Met de file 'coordinates.csv' kan een plot gemaakt worden op een kaart,zie DEEL2.
Om een propere shut down mogelijk te maken voorzien we een reedcontact tussen GPIO17 en GND. Als het tostel moet afgesloten worden op het einde van een trip wordt een magneet in de buurt gebracht en de raspberry schakelt uit.

DEEL2.

Met een afzonderlijk programma kunnen we de eerder opgenomen data ' coordinates.csv' zichtbaar maken op een kaart.
Om dit te laten werken zijn er 4 files nodig. Het programma die bestaat uit 2 files 'main.py' en 'gps_class.py'. Een kaart 'map.png' en de opgenomen coördinaten 'coordinates.csv'. Zorg dat deze 4 files in de zelfde map staan zodat ze tijdens het proces door het programma terug gevonden worden.

Bij het starten zal het programma 'main.py' de 'map.png' aanvullen met een plot v/d coördinaten te zien in 'resultMap.png' of een plot op het scherm.

Op basis van: https://towardsdatascience.com/simple-gps-data-visualization-using-python-and-open-street-maps-50f992e9b676
















