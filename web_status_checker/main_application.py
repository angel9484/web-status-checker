class MainApplication:
    @staticmethod
    def create_app():
        from web_status_checker.core.web_status_checker import WebStatusChecker
        from web_status_checker.web.web_application import WebApplication
        import os
        web_application = WebApplication()
        app = web_application.appmiddleware
        WebStatusChecker(os.getenv('INTERVAL_TO_CHECK_SECONDS'), os.getenv('WEBS_TO_CHECK'),
                         os.getenv('TIMEOUT')).start()
        return app


def create_app():
    return MainApplication().create_app()


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    run_simple("0.0.0.0", 5000, MainApplication().create_app(), use_reloader=True, use_debugger=True, use_evalex=True)
