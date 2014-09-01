#!/usr/bin/env python

"""
Bottle-based URL Shortener service
"""

import sys
from shortener import URLKeeper
from bottle import route, run, request, redirect, abort, static_file, jinja2_view as view
from datetime import datetime as dt

KEEPER = None
BASE_URL = None
KEY_LENGTH = None

@route('/static/<path:path>')
def static(path):
    return static_file(path, root='./static/')

@route('/')
@view('index.jinja2')
def index():
    return {'num_entries': KEEPER.num_entries(), 'base_url': BASE_URL}

@route('/clear')
def clear():
    """ Delete all entries in the DB """
    KEEPER.delete_all_entries()

@route('/stats')
def statistics():
    data = KEEPER.get_all_entries()
    return {'num_entries': len(data), 'data': data}

@route('/<id>')
def urls(id):
    """Redirects to the original URL"""
    original_url = KEEPER.get_long_url(id)
    if original_url is None:
        abort(404, "Sorry, unknown URL.")
    KEEPER.increment_hits(id)
    redirect(original_url)

@route('/shorten', method='GET')
def shorten_url():
    url = request.GET.get('url', None).strip()
    requesting = request.GET.get('requesting', None).strip()
    ip = request.remote_addr
    now = dt.utcnow().isoformat()
    if not url:
        return {'success': False, 'error': 'Need a URL'}

    if not KEEPER.valid_long_url(url):
        return {'success': False, 'error': 'The URL needs to start with http:// or https://'}

    if requesting and KEEPER.get_long_url(requesting) is not None:
        return {'success': False, 'error': 'The requested short URL "{}" is already assigned.'.format(requesting)}

    # let's create (and store) the shortened url
    context = {'ip': ip, 'dt': now}
    try:
        short_id = KEEPER.create_short_url(url, short_url_id_request=requesting, context=context, key_length=KEY_LENGTH)
        return {'success': True, 'result': short_url_from_key(short_id)}
    except NameError as e:
        return {'success': False, 'error': 'Could not create short URL: {}.'.format(e)}

def short_url_from_key(key):
    return BASE_URL + key

def main():
    global KEEPER, BASE_URL, KEY_LENGTH

    import argparse
    import socket
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--key-length', default=4, type=int, help='The default number of letters for your short URLs.')
    parser.add_argument('--plugin', help='The data persistance plugin URL, such as "redis://localhost:6379/0" or "filedict://db.shorturls.sqlite3"')
    parser.add_argument('--server-adapter', default='cherrypy', help='Which server to run this web app on. (If you only want IPv4, you may use "wsgiref").')
    parser.add_argument('--base-url', default='http://{}/'.format(socket.gethostname()), help='The base URL of this service.')
    parser.add_argument('--host', default='::', help='The host/IP to bind the server to. Use "0.0.0.0" if you want IPv4 only.')
    parser.add_argument('--port', default=8080, type=int, help='The port the server should listen at. Default: 8080.')
    parser.add_argument('--debug', action='store_true', help='Enable debugging mode.')

    args = parser.parse_args()

    BASE_URL = args.base_url
    KEY_LENGTH = args.key_length
    if not args.plugin:
        KEEPER = URLKeeper()
    elif args.plugin.lower().startswith('filedict://'):
        try:
            from plugins import ContainerPlugin
            from filedict import FileDict
        except ImportError:
            parser.error('There is a problem: Get FileDict from "https://github.com/pklaus/filedict/blob/threadsafe/filedict.py" '
                  'and put it into the folder of this script. Exiting now.')
        class FileDictContainer(FileDict, ContainerPlugin):
            pass
        KEEPER = URLKeeper(container=FileDictContainer(filename=args.plugin.replace('filedict://','')))
    
    elif args.plugin.lower().startswith('redis://'):
        try:
            from plugins.redis_plugin import RedisContainer
        except ImportError:
            parser.error('You need redis-py to use this plugin. Get it with `pip install redis`.')
        KEEPER = URLKeeper(container=RedisContainer.from_url(args.plugin))

    run(server=args.server_adapter, host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()

