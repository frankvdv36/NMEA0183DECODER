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

Het programma maakt 2 files aan. 'GPSdata.csv' en bevat respectivelijk 'datum, time, latitude, longitude, altitude, snelheid, richting en aantal sat'
de andere file 'coordinates.csv' bevat enkel 'latitude, longitude'. Met deze laatste kan een plot gemaakt worden op een kaart.

DEEL2.


















