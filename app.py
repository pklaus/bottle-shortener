#!/usr/bin/env python

"""
Bottle-based URL Shortener service
"""

import sys
from shortener import URLKeeper
from bottle import route, run, request, redirect, abort

KEEPER = None

@route('/')
def index():
    return 'I am the URL Shortener! I currently have %i shortened URLs in my books.' % KEEPER.num_entries()

@route('/stats')
def statistics():
    data = KEEPER.get_all_urls()
    return {'num_entries': len(data), 'data': data}

@route('/go/:id')
def urls(id):
    """Redirects to the original URL"""
    original_url = KEEPER.get_long_url(id)
    if original_url is None:
        abort(404, "Sorry, unknown URL.")
    redirect(original_url)

@route('/shorten', method='GET')
def shorten_url():
    url = request.GET.get('url', '').strip()
    if url == '':
        return {'error': 'Need an url', 'result': ''}

    if not KEEPER.valid_long_url(url):
        return {'error': 'The URL needs to start with http:// or https://', 'result': ''}

    # let's create (and store) the shortened url
    short_url = KEEPER.create_short_url(url)
    return {'error': '', 'result': request.urlparts[0] + '://' + request.urlparts[1] + '/go/' + short_url}


def main():
    global KEEPER

    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plugin', help='The data persistance plugin URL, such as "redis://localhost:6379/0" or "filedict://db.shorturls.sqlite3"')
    parser.add_argument('--server-adapter', default='cherrypy', help='Which server to run this web app on. (If you only want IPv4, you may use "wsgiref").')
    parser.add_argument('--host', default='::', help='The host/IP to bind the server to. Use "0.0.0.0" if you want IPv4 only.')
    parser.add_argument('--port', default=8080, type=int, help='The port the server should listen at. Default: 8080.')
    parser.add_argument('--debug', action='store_true', help='Enable debugging mode.')

    args = parser.parse_args()

    if not args.plugin:
        KEEPER = URLKeeper()
    elif args.plugin.lower().startswith('filedict://'):
        try:
            from filedict import FileDict
        except ImportError:
            parser.error('There is a problem: Get FileDict from "https://github.com/pklaus/filedict/blob/threadsafe/filedict.py" '
                  'and put it into the folder of this script. Exiting now.')
        KEEPER = URLKeeper(container=FileDict(filename=args.plugin.replace('filedict://','')))
    
    elif args.plugin.lower().startswith('redis://'):
        try:
            from plugins.redis_plugin import RedisContainer
        except ImportError:
            parser.error('You need redis-py to use this plugin. Get it with `pip install redis`.')
        KEEPER = URLKeeper(container=RedisContainer.from_url(args.plugin))

    run(server=args.server_adapter, host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main()

