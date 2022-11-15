# NMEA0183DECODER met Raspberry PI
## Beschrijving
Decodeert de data afkomstig van een GPS-module naar een leesbare vorm. Deze data is gecodeerd volgens NMEA0183 protocol.

Iedere seconde wordt een reeks lijnen naar buiten gestuurd via de serial0-bus op een snelheid van 9600 baud.

De inhoud en samenstelling wordt uitgelegd in bijlage NMEA0183.pdf

Het programma neemt de data binnen via de serial0-bus op GPIO15 split deze en maakt de volgende variabelen: 

datum, time, latitude, longitude, altitude, snelheid, richting en aantal sat.

Er zijn gps-modules die enkel de US-satellieten ontvangen anderen ook de Chineese, Russische, Europese.

In het eerste geval begint de lijn met GPxxx in het andere geval GNxxx. Dit programma werkt met beidie type modules.















