"""
A simple proxy server for Xiaomi Yi camera. Usage:
http://hostname:port
For example:
http://127.0.0.1:8090

Thanks to @gear11
"""
import requests
import logging
import vlc

from config import host, port, CHUNK_SIZE, CAMERA
from flask import Flask, request, Response
from led import Led
from six import _print
from werkzeug.serving import WSGIRequestHandler


app = Flask(__name__.split('.')[0])

host_url = 'http://%s:%s' % (host, port)

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(message)s')
LOG = logging.getLogger(__name__)

led = Led()


class CustomRequestHandler(WSGIRequestHandler):

    def connection_dropped(self, error, environ=None):
        _print('Dropped, but it is called at the end of the execution :(')


def split_url(url):
    """Splits the given URL into a tuple of (protocol, host, uri)"""
    proto, rest = url.split(':', 1)
    rest = rest[2:].split('/', 1)
    host, uri = (rest[0], rest[1]) if len(rest) == 2 else (rest[0], "")
    return (proto, host, uri)


def proxy_ref_info(request):
    """Parses out Referer info indicating the request is from a previously proxied page.
    For example, if:
        Referer: http://localhost:8080/p/google.com/search?q=foo
    then the result is:
        ("google.com", "search?q=foo")
    """
    ref = request.headers.get('referer')
    if ref:
        _, _, uri = split_url(ref)
        if uri.find("/") < 0:
            return None
        first, rest = uri.split("/", 1)
        if first in "pd":
            parts = rest.split("/", 1)
            r = (parts[0], parts[1]) if len(parts) == 2 else (parts[0], "")
            LOG.info("Referred by proxy host, uri: %s, %s", r[0], r[1])
            return r
    return None


def get_source_rsp(url):
        url = 'http://%s' % url
        LOG.info("Fetching %s", url)

        # Pass original Referer for subsequent resource requests
        proxy_ref = proxy_ref_info(request)
        headers = {"Referer": "http://%s/%s" % (proxy_ref[0], proxy_ref[1])} if proxy_ref else {}
        # Fetch the URL, and stream it back
        LOG.info("Fetching with headers: %s, %s", url, headers)
        return requests.get(url, stream=True, params=request.args, headers=headers)


def _do_proxy(url):
    r = get_source_rsp(url)
    LOG.info("Got %s response from %s" % (r.status_code, url))
    headers = dict(r.headers)

    def generate():
        for chunk in r.iter_content(CHUNK_SIZE):
            yield chunk
    return Response(generate(), headers=headers)


@app.route('/')
def home():
    """Render index.html page"""
    LOG.debug('Render index.html')
    return app.send_static_file('index.html')


@app.route('/motion')
def motion():
    url = '%s/motion' % CAMERA
    LOG.debug('Render motion')
    led.turn_off()
    return _do_proxy(url)


@app.route('/record/<day>/<video>')
def reproduce_video(day, video):
    url = '%s/record/%s/%s' % (CAMERA, day, video)
    LOG.debug('Reproduce video recorded, url = %s' % url)
    return _do_proxy(url)


@app.route('/record/<day>/')
def get_day_folder(day):
    LOG.debug('Reproduce day = %s' % day)
    if '/' in day:
        args = day.split('/')
        return reproduce_video(args[0], args[1])
    url = '%s/record/%s/' % (CAMERA, day)
    return _do_proxy(url)


@app.route('/record/')
def get_records():
    url = '%s/record/' % CAMERA
    LOG.debug('Record folder')
    return _do_proxy(url)


@app.route('/ch/<channel>')
def get_streams(channel):
    url = 'rtsp://%s:554/ch%s.h264' % (CAMERA, channel)
    LOG.debug('Stream video, url=%s' % url)
    p = vlc.MediaPlayer(url)
    p.play()
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(host=host, port=int(port), debug=True)
