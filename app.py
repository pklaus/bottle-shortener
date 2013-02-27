#!/usr/bin/env python3

"""Bottle-based URL Shortener service"""
from shortener import URLKeeper

#keeper = URLKeeper()
## FileDict from https://raw.github.com/pklaus/filedict/threadsafe/filedict.py
from filedict import FileDict
keeper = URLKeeper(container=FileDict(filename='db.shorturls.sqlite3'))

from bottle import route, run, request, redirect, abort

@route('/')
def index():
    return 'I am the URL Shortener! I currently have %i shortened URLs in my books.' % keeper.num_entries()

@route('/stats')
def index():
    data = keeper.get_all_urls()
    return {'num_entries': len(data), 'data': data}

@route('/go/:id')
def urls(id):
    """Redirects to the original URL"""
    original_url = keeper.get_long_url(id)
    if original_url is None:
        abort(404, "Sorry, unkown URL.")

    redirect(original_url)

@route('/shorten', method='GET')
def shorten_url():
    url = request.GET.get('url', '').strip()
    if url == '':
        return {'error': 'Need an url', 'result': ''}

    if not keeper.valid_long_url(url):
        return {'error': 'The URL needs to start with http:// or https://', 'result': ''}

    # let's create (and store) the shortened url
    short_url = keeper.create_short_url(url)
    return {'error': '', 'result': request.urlparts[1] + '/go/' + short_url}


if __name__ == '__main__':
    #run(host='localhost', port=8080)
    #run(host='0.0.0.0', port=8080)
    run( server='cherrypy', host="::", port=8080)

