"""Application exporter"""

import os
import time
from prometheus_client import start_http_server, Gauge, Enum, Info
import logging
import requests

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARN")

PROMETHEUS_PREFIX = os.getenv("PROMETHEUS_PREFIX", "openweathermap")
PROMETHEUS_PORT   = int(os.getenv("PROMETHEUS_PORT", "9003"))

IP                       = os.getenv("IP", "")
polling_interval_seconds = int(os.getenv("POLLING_INTERVAL_SECONDS", "60"))

LOGFORMAT = '%(asctime)-15s %(message)s'

logging.basicConfig(level=LOG_LEVEL, format=LOGFORMAT)
LOG = logging.getLogger("openweathermap-export")

class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, PROMETHEUS_PREFIX='', APIKEY='', WEATHER_COUNTRY='NL', WEATHER_LANGUAGE='NL', polling_interval_seconds=5):

        if PROMETHEUS_PREFIX != '':
            PROMETHEUS_PREFIX = PROMETHEUS_PREFIX + "_"

        self.PROMETHEUS_PREFIX = PROMETHEUS_PREFIX
        self.IP = IP
        self.polling_interval_seconds = polling_interval_seconds

        # Prometheus metrics to collect
        self.status = Info(PROMETHEUS_PREFIX + 'status', 'status')
        self.wind_speed = Gauge(PROMETHEUS_PREFIX + 'wind_speed', 'wind_speed')
        
    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """

        try:
            response = requests.get("http://" + self.IP +":82/watermeter/api/read")
            response.raise_for_status()
            LOG.info("The request was a success!")
            LOG.info(response.text())
            LOG.info(response.json())            
        except requests.exceptions.HTTPError as error:
            LOG.error(error)

        #self.location.info( { 'location': location } )

        LOG.info("Update prometheus")

def main():
    """Main entry point"""

    if IP != "":
        app_metrics = AppMetrics(
            PROMETHEUS_PREFIX=PROMETHEUS_PREFIX,
            APIKEY=IP,
            polling_interval_seconds=polling_interval_seconds
        )
        start_http_server(PROMETHEUS_PORT)
        LOG.info("start prometheus port: %s", PROMETHEUS_PORT)
        app_metrics.run_metrics_loop()
    else:
        LOG.error("IP is invalid")

if __name__ == "__main__":
    main()