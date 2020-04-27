import time

from prometheus_client import Gauge


class Web:
    def __init__(self, web='', timeout=10):
        if web:
            web_params = web.split(",")
            self._name = web_params.pop(0).lower()
            self._url = web_params.pop(0).lower()
            self._kind = web_params.pop(0).lower()
            self._timeout = int(timeout)
            self._gauge_status = Gauge(self._name + '_url_up', '', ['url'])
            self._gauge_time = Gauge(self._name + '_url_response_ms', '', ['url'])

    def start_check(self):
        import threading
        run_thread = threading.Thread(target=self._check)
        run_thread.setDaemon(True)
        run_thread.start()

    def _check(self):
        import requests
        import http
        start_time = time.time()

        try:
            response = requests.request(self._kind, self._url, timeout=self._timeout)
            if response.status_code == http.HTTPStatus.OK:
                self._gauge_status.labels(self._url).set(1)
            elif response.status_code == http.HTTPStatus.SERVICE_UNAVAILABLE:
                self._gauge_status.labels(self._url).set(0)
        except TimeoutError as timeout:
            pass
        self._gauge_time.labels(self._url).set(time.time() - start_time)
