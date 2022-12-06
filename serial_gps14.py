# Werkt volledig: vult na een paar seconden de variabelen in tenzij het signaal niet geldig is
# Deze versie zorgt dat zowel GNxxx als GPxxx files kunnen gelezen worden. serial_gps9bis.py 
# Aangepast om met epoch tijd iedere minut een file met de data weg te schrijven
# OPGELET: zet eerst serial interface aan. 'sudo raspi-config', nr3 'interface options' en bij 'Serial port' zet UIT 'login shell' en AAN 'port hardware'
# 'serial_gps12.py' naar 'serial_gps13.py'  Aangepast file: 'GPSdata.csv' nieuw 'coordinates.csv'
# geen spacies tussen data columns enkel gescheiden door een comma ','= 'csv' file
# frequentie, path1 en path2 naar boven gebracht
# autostart: 'sudo nano /etc/rc.local' deze lijn aanbrengen 'sudo python /home/pi/Python3/LoraGPS/start.py'
# check of het programma loopt: 'ps aux | grep /home/pi/Python3/LoraGPS/start.py'
# Stoppen van de recorder via GIO   https://www.deviceplus.com/raspberry-pi/using-raspberry-pi-gpio-pins-with-the-rpi-gpio-python-library/

import serial                   # raspi-config serial ON. Zie hierboven lijn 4
import time
from subprocess import call     # save shut down 
import RPi.GPIO as GPIO

# Stop Python programma op een propere wijze. reedcontact tussen GPIO17 en GND. Magneet tegen reedcontact = shut down
GPIO.setmode(GPIO.BCM)          # BCM = GPIO nummers / BOARD = PIN nummers
stopRPI = 17                    # GPIO 17            / PIN 11    
GPIO.setup(stopRPI, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # GPIO input met pull-up

SERIAL_PORT = "/dev/serial0"
running = True
global vlag
nowOld = 0
now = 0
frequentie = 60     # Ritme van data wegschrijven in seconden
path1 = "/home/pi/Python3/LoraGPS/GPSdata.csv"
path2 = "/home/pi/Python3/LoraGPS/coordinates.csv"
vlag = 1            # GPS signaal: 1 = Void (niet geldig), 0 is Active (geldig)
datum = 0
tijd = 0
latitude = 0
longitude = 0
snelheid = 0
richting = 999      # 999 aanduiding dat er geen richting aangegeven is
altitude = 0
sat = 0
#-----------------------------------------------------------------------
# Conversie naar DD.MMMMMM

# In the NMEA message, the position gets transmitted as:
# DDMM.MMMMM, where DD denotes the degrees and MM.MMMMM denotes
# the minutes. However, I want to convert this format to the following:
# DD.MMMM. This method converts a transmitted string to the desired format

def dm(x):      # https://stackoverflow.com/questions/40690927/converting-dd-mm-mmm-to-dd-ddddd-latitude-longitude-in-python-3
    degrees = int(x) // 100
    minutes = x - 100*degrees

    return degrees, minutes

def decimal_degrees(degrees, minutes):
    return degrees + minutes/60 

#-----------------------------------------------------------------------
# GxRMC bevat time ,date, longitude en latitude

# This method reads the data from the serial port, the GPS dongle is attached to,
# and then parses the NMEA messages it transmits.
# gps is the serial port, that's used to communicate with the GPS adapter

def getPositionData(gps):         # longitude, latitude, tijd, datum
        
    data = gps.readline()
    # print (data)                # We zien de data voorbij komen
    message = data[3:6]           # de eerste karakters tellen niet mee (b')
    # print (message)             # We zien de eerste 6 karakters
    
    if (message == b'RMC'):    # b'$GNRMC' komt dus overeen met $GNRMC # Beschikbaar: date, time, lati, longi, speed knots, richting 
        # print (data)              # print de volledige regel
        parts = data.split(b',')  # b',' b moet er boor om te melden dat het gaat over BYTES
                
        if parts[2] == b'V':   # V = Void  A = active
            # V = Warning, most likely, there are no satellites in view...
            global vlag
            vlag = 1              # 1 = Void, 0 is Active
            print ("GPS receiver warning")
            
        else:
            vlag = 0              # 1 = Void, 0 is Active
            # Get the position data that was transmitted with the GNRMC message
            # In this example, I'm only interested in the longitude and latitude
            # for other values, that can be read, refer to: http://aprs.gids.nl/nmea/#rmc
            global datum, tijd, latitude, longitude, nu
            
            tijd = (parts[1])
            tijd = float(tijd)
            tijd = f'{tijd:.0f}'    # geen getallen na de komma
            nu = float(tijd)
            #print ('tijd',tijd)
            datum = (parts[9])
            datum = float(datum)
            datum = f'{datum:.0f}'    # geen getallen na de komma  
            # print (datum)
            # print (parts[3])        # b'5106.14895' dit fomaat in bytes is niet te gebruiken
            latitude = float(parts[3])  # 5106.14943 in float formaat DDMM.MMMMM
            # print (latitude)
            latitude = (decimal_degrees(*dm(latitude))) # 51.10249050000001 in formaat DD.DDDDDD
            latitude =  f'{latitude:.6f}'               # 6 cijfers na de komma
            # print ("latitude = " + latitude)
            
            # print (parts[5])        # b'00316.19358' dit fomaat in bytes is niet te gebruiken
            longitude = float(parts[5])  # 00316.19358 in float formaat DDMM.MMMMM
            # print (longitude)
            longitude = (decimal_degrees(*dm(longitude))) # 3.269886 in formaat DD.DDDDDD
            longitude =  f'{longitude:.6f}'               # 6 cijfers na de komma
            #print ('\n', " datum = " + str(datum)," tijd = " + str(tijd), " lat = " + str(latitude)," lon = "  + str(longitude), '\n')
                
#-----------------------------------------------------------------------
# GxVTG bevat Speed en Track

def getSpeed(gps):
    
    data = gps.readline()
    message = data[3:6]           # de eerste karakters tellen niet mee (b')
    # print (message)             # We zien de eerste 6 karakters
    
    if (message == b'VTG'):    # b'$GNTVG' komt dus overeen met $GNTVG  Beschikbaar: Speed km/h en richting
        # print (data)              # print de volledige regel
        parts = data.split(b',')  # b',' b moet er boor om te melden dat het gaat over BYTES
        global snelheid, richting
        snelheid = float(parts[7])       # http://aprs.gids.nl/nmea/#rmc   
        snelheid = round(snelheid)
        richting = (parts[1])
        if (richting == b''):     # als niet ingevuld is wordt het een 999
            richting = 999
        else:                     # anders getal overnemen
            richting = float(richting)
            richting = round(richting)
        #print ('\n', 'Snelheid = ',snelheid, ' Richting = ', richting, '\n')
     
#-----------------------------------------------------------------------
# GxGGA bevat Altitude en Sat
            
def getAltitude(gps):   
    
    data = gps.readline()
    message = data[3:6]           # de eerste karakters tellen niet mee (b')
    # print (message)             # We zien de eerste 6 karakters
               
    if (message == b'GGA'):    # b'$GNGGA' komt dus overeen met $GNGGA  Beschikbaar: Altitude, sat's, time, lati en longi
        # print (data)              # print de volledige regel
        parts = data.split(b',')  # b',' b moet er boor om te melden dat het gaat over BYTES
        global altitude, sat
        altitude = float(parts[9])       # http://aprs.gids.nl/nmea/#rmc   
        altitude = round(altitude)
        sat = (parts[7])
        sat = float(sat)          # geheel getal
        sat = round(sat)
        #print ('\n', 'Aantal Sat= ',sat,' Altitude = ', altitude, '\n')     # if vlag == 1:

#-----------------------------------------------------------------------
# SCHRIJF STRING OP SD-KAART

def fileW(filedata, filecoordinates): # schrijf de meegegeven data op SD kaart
    
    fo = open(path1, "a") # open file volgens pad, indien onbestaand maak aan
    fo.write (filedata) # Er wordt geschreven in opgegeven pad en voeg nieuwe data toe
    fo.close()          # Close opend file
    fo = open(path2, "a") # open file volgens pad, indien onbestaand maak aan
    fo.write (filecoordinates) # Er wordt geschreven in opgegeven pad en voeg nieuwe data toe
    fo.close()          # Close opend file

         
# START PROGRAMMA ------------------------------------------------------

print ("Application started!")
gps = serial.Serial(SERIAL_PORT, baudrate = 9600, timeout = 0.5)

while running:
    try:                          # check reedcontact High = running / Low = shut down
        getPositionData(gps)      #  longitude, latitude, tijd, datum    
        #print ('\n', " datum = " + str(datum)," tijd = " + str(tijd), " lat = " + str(latitude)," lon = "  + str(longitude), '\n')
        
    except KeyboardInterrupt:     # Ctrl + C
        running = False
        gps.close()
        print ("Application closed!")
    try:
        if (GPIO.input(stopRPI) == False):
            call("sudo nohup shutdown -h now", shell=True)
        else:
            pass
    except:
        # You should do some error handling here...
        print ("Application error 1!")
    try:
        if (vlag == 0):     # 1 = Void, 0 is Active
            getSpeed(gps)   # snelheid en richting als vlag = 0 = geldig signaal
        else:
            pass
    except:
        # You should do some error handling here...
        print ("Application error 2!")    
    try:
        if (vlag == 0):     # 1 = Void, 0 is Active
            getAltitude(gps)# altitude en aantal sat als vlag = 0 = geldig signaal
        else:
            pass
    except:
        # You should do some error handling here...
        print ("Application error 3!")
        
    if (vlag == 0):                         # deze en volgende regels zijn niet echt nodig als er getest wordt op de vlag
        now = round (time.time())           # GETAL sedert 1/1/1970, maak een geheel getal in sec.
        # print ('now', now)
        if now >= nowOld + frequentie:      # ritme waarmee 2 files worden wegeschreven
            filedata = "{0},{1},{2},{3},{4},{5},{6}\n".format(datum, tijd, latitude, longitude, snelheid, richting, altitude, sat)    
            filecoordinates = "{0},{1}\n".format(latitude, longitude)    
            fileW(filedata, filecoordinates)
            nowOld = now                    # reset de tijd
        else:
            print (datum, tijd, latitude, longitude, snelheid, richting, altitude, sat)
    else:
        print ('Void: vlag = 1')
        datum = 0
        tijd = 0
        latitude = 0
        longitude = 0
        snelheid = 0
        richting = 999
        altitude = 0
        sat = 0
        
# EINDE ================================================================
    
