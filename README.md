# swiss-meteo-prometheus-exporter
A prometheus exporter for the swiss meteo data.


Source of data: [opendata.swiss](https://opendata.swiss/en/dataset/automatische-wetterstationen-aktuelle-messwerte/resource/e237df80-33a6-4bf9-bfc8-b9477e83a3e0)

## Installation
Only steps for Debian are provided, for other distros or OS they might differ.
1. `sudo apt install python pip`
2. `mkdir /opt/meteo-exporter`
3. `touch /var/log/meteo-exporter.log`
4. `cp server.py /opt/meteo-exporter/`
5. `cp meteo-exporter.service /etc/systemd/system/`
6. `sudo systemctl enable meteo-exporter`
7. Install [client_python](https://github.com/prometheus/client_python) in your preferrred way
8. Edit /opt/meteo-exporter/server.py with your favorite editor and change the variables as indicated
9. `sudo systemctl start meteo-exporter`
