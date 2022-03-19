from base64 import decode
from io import StringIO
import urllib.request
import csv
import time
import prometheus_client
from prometheus_client import start_http_server, Summary
import logging


# set settings, you usually only need to modify the next two variables
loc = 'ENTER_ABBREVIATION' # the location you want to read the data out, download https://data.geo.admin.ch/ch.meteoschweiz.messnetz-automatisch/ch.meteoschweiz.messnetz-automatisch_en.csv and add the Abbreviation here
checkurl = 'ENTER_URL'

# change variables here only if the location changes or the structure
download = 'https://data.geo.admin.ch/ch.meteoschweiz.messwerte-aktuell/VQHA80.csv'
temp = 'tre200s0' # the column name where the temperature can be found
prec = 'rre150z0' # the column name where the precipitation can be found
humi = 'ure200s0' # the column name where the relative air humidity can be found
wspe = 'fu3010z0' # the column name where the wind speed can be found
press = 'prestas0' # the column name where the air pressure can be found
# logging settings
logging.basicConfig(filename='/var/log/meteo-exporter.log', encoding='utf-8', level=logging.INFO)

TEMPERATURE_GAUGE = prometheus_client.Gauge("temperature_celcius", "Temperature in Celcius")
PRECIPITATION_GAUGE = prometheus_client.Gauge("precipitation_millimeter", "Precipitation in millimeter")
HUMIDITY_GAUGE = prometheus_client.Gauge("humidity_percent", "Humidity percentage")
WINDSPEED_GAUGE = prometheus_client.Gauge("windspeed_kmh", "Wind speed in km/h")
AIRPRESSURE_GAUGE = prometheus_client.Gauge("airpressure_hpa", "Air pressure in hPa")

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8001)
    while True:
        try:
            urllib.request.urlopen(checkurl)
        except:
            logging.info('No internet connection, wait for 15 minutes.')
            time.sleep(900)
        else:
            logging.info('Internet connection present, continue with calling API.')
            data = urllib.request.urlopen(download).read().decode('UTF-8')
            dataFile = StringIO(data)
            csvReader = csv.DictReader(dataFile, delimiter=';')
            for row in csvReader:
                if row['Station/Location'] == loc:
                    tempp = row.get(temp)
                    precp = row.get(prec)
                    humip = row.get(humi)
                    wspep = row.get(wspe)
                    pressp = row.get(press)
                    break
            TEMPERATURE_GAUGE.set(tempp)
            PRECIPITATION_GAUGE.set(precp)
            HUMIDITY_GAUGE.set(humip)
            WINDSPEED_GAUGE.set(wspep)
            AIRPRESSURE_GAUGE.set(pressp)
        finally:
            time.sleep(900)
