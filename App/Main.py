import logging.handlers
import platform

import settings

#Setup Handler
syslog_handler = logging.handlers.SysLogHandler(address=(settings.syslog_server, settings.syslog_port))
console_handler = logging.StreamHandler()
syslog_handler.setFormatter(logging.Formatter("Web-App \n[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(funcName)s():%(lineno)s)"))
# This needs a new line break for Greylog to parse source
console_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(funcName)s():%(lineno)s)"))

## FIXME Add syslog for prod
# logging.basicConfig(level=logging.WARN, handlers=[console_handler, syslog_handler])
if platform.system() == 'Windows':
    logging.basicConfig(level=logging.DEBUG, handlers=[console_handler])
else:
    logging.basicConfig(level=logging.INFO, handlers=[console_handler,syslog_handler])

import libs.telemetry

from libs.api.flask_api_server import web_server
import waitress
if __name__ == '__main__':
    '''Program Start'''
    libs.telemetry.start_telemetry() # Start Prometheus Telemetry

    logging.info('STARTING API SERVER')
    app = web_server.generate_web_app()
    waitress.serve(app, listen='*:' + str(settings.web_server_port),cleanup_interval=60, channel_timeout=240)
