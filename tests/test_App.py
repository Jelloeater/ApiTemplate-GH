import sys
sys.path.append('./App')  # Needed to import module properly


import settings


## LOGGING SETUP START
#Setup Handler
syslog_server = '127.0.0.1'
syslog_port = 514
import logging.handlers
syslog_handler = logging.handlers.SysLogHandler(address=(syslog_server, syslog_port))
console_handler = logging.StreamHandler()
syslog_handler.setFormatter(logging.Formatter(
    settings.appname + " \n[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(funcName)s():%(lineno)s)"))
# This needs a new line break for Greylog to parse source
console_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)8s] --- %(message)s (%(filename)s:%(funcName)s():%(lineno)s)"))

# logging.basicConfig(level=logging.INFO, handlers=[console_handler, syslog_handler]
logging.basicConfig(level=logging.INFO, handlers=[console_handler])

## Add to Additional Arguments '-p no:logging -s' for PyTest
## LOGGING SETUP END


## GLOBALS FOR Webserver
import requests
class Test_Logging():
    def test_basic_log(self):
        logging.info('UNIT TEST START')



class API_Test_server():
    import threading
    class MakeTestServer(threading.Thread):
        def __init__(self):
            from libs.api import flask_api_server
            app = flask_api_server.web_server.generate_web_app()
            import threading
            threading.Thread.__init__(self)
            from werkzeug.serving import make_server
            self.srv = make_server('127.0.0.1', 5000, app)
            self.ctx = app.app_context()
            self.ctx.push()

        def run(self):
            logging.info('starting server')
            self.srv.serve_forever()

        def shutdown(self):
            self.srv.shutdown()


class Test_API_server():
    test_server = API_Test_server.MakeTestServer()
    BASE_URL = "http://localhost:5000/api/v1"

    @classmethod
    def setup_class(cls):
        cls.test_server.start()

    @classmethod
    def teardown_class(cls):
        cls.test_server.shutdown()

    def test_base_url(self):
        response = requests.get(self.BASE_URL + '/swagger.json')
        assert response.status_code == 200

    def test_hi(self):
        print("hi")
        assert True

