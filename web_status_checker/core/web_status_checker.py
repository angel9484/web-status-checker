import threading


class WebStatusChecker:
    def __init__(self, time_to_sleep_in_seconds=10, urls=None, timeout=10):
        self._running = False
        self.run_thread = threading.Thread(target=self._run)
        self.run_thread.setDaemon(True)
        self._time_to_sleep_in_seconds = int(time_to_sleep_in_seconds)
        self._webs = self._create_webs(urls, timeout)

    def start(self):
        if not self.run_thread.is_alive():
            self._running = True
            self.run_thread.start()

    def stop(self):
        self._running = False

    def _run(self):
        import time
        while self._running:
            for web in self._webs:
                web.start_check()
            time.sleep(self._time_to_sleep_in_seconds)

    @staticmethod
    def _create_webs(urls='', timeout=10):
        webs = []
        if urls:
            from web_status_checker.core.web import Web
            webs_string = urls.split(';')
            for web_string in webs_string:
                webs.append(Web(web_string, timeout))
        return webs
