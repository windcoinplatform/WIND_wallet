from threading import Thread, Lock
import logging
import webview
from time import sleep
from TurtleNetwork import run_server, PORT

server_lock = Lock()

logger = logging.getLogger(__name__)


def url_ok(url, port):
    # Use httplib on Python 2
    from http.client import HTTPConnection

    try:
        conn = HTTPConnection(url, port)
        conn.request('GET', '/login')
        r = conn.getresponse()
        return r.status == 200
    except:
        logger.exception('Server not started')
        return False


def create_webview():
    return webview.create_window('T3-ALPHA(NON PRODUCTION) - Turtle Network Wallet', 'http://127.0.0.1:' + str(PORT),
                                 text_select=True,
                                 confirm_close=True, min_size=(1024, 600))


def set_up():
    logger.debug('Starting server')
    t = Thread(target=run_server)
    t.daemon = True
    t.start()
    logger.debug('Checking server')

    while not url_ok('127.0.0.1', PORT):
        sleep(1)

    logger.debug('Server started')
    logger.debug('Binding on port ' + str(PORT))
    create_webview()
    webview.start(debug=True, gui='qt')


if __name__ == '__main__':
    set_up()
