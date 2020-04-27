FROM python:3.7.3-slim

RUN useradd --create-home python
WORKDIR /home/python/web-status-checker

COPY requirements.txt .

RUN set -ex \
    && BUILD_DEPS="build-essential libpcre3-dev libpq-dev" \
    && apt-get update \
    && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install -r requirements.txt --no-cache-dir \
    && pip install --no-cache-dir uwsgi \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

RUN chown -R python:python /home/python/web-status-checker

USER python

COPY web_status_checker ./web_status_checker

ENV WEBS_TO_CHECK "Google,http://www.google.com,GET;Amazon,http://www.amazon.com,GET"
ENV INTERVAL_TO_CHECK_SECONDS "10"
ENV TIMEOUT "10"

ENV PATH=$PATH:/home/python
ENV PYTHONPATH=$PYTHONPATH:/home/python

ENV UWSGI_HTTP=:8080 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

EXPOSE 8080 8081 8182
CMD ["uwsgi","-s","/tmp/myapplication.sock","--show-config","--need-app","--manage-script-name","--mount","/=web_status_checker.main_application:app"]
