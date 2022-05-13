from prometheus_client import start_http_server, Gauge

prometheus_port = 8082


def start_telemetry():
    start_http_server(prometheus_port)


# noinspection PyArgumentList
class Sensors():
    AT_REST_API_CALL = Gauge('at_rest_api_call', 'Number of API Calls to AT')

    @staticmethod
    def reset_counters():
        pass # Stop clearing counters for now
        # Sensors.AT_REST_API_CALL.set(0)

