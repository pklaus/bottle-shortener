from string import ascii_letters, digits
from random import choice
from plugins import DictContainer

class URLKeeper(object):
    CHARS = ascii_letters + digits
    MAX_TENTATIVE = 1000

    def __init__(self, container = DictContainer()):
        self._container = container

    def _random_id(self, length=10):
        return ''.join([choice(self.CHARS) for i in range(length)])
    
    def create_short_url(self, long_url, short_url_id_request=None, context={}):
        """Creates and store a short url."""
        if self.long_url_exists(long_url):
            return self.get_long_url(short_url_id)
        if short_url_id_request and self.key_exists(short_url_id_request):
            raise NameError('Requested short URL exists already.')
        for tentative in range(self.MAX_TENTATIVE):
            key = short_url_id_request if short_url_id_request else self._random_id()
            key = str(key)
            entry = {'long_url': long_url, 'context': context, 'hits': 0}
            if not self.key_exists(key):
                self._container[key] = entry
                #_Rcontainer[long_url] = key
                return key
        raise NameError('Could not create short URL.')
    
    def increment_hits(self, short_url_id):
        key = str(short_url_id)
        try:
            entry = self._container[key]
            entry['hits'] += 1
            self._container[key] = entry
            return entry['hits']
        except KeyError:
            return None

    def get_long_url(self, short_url_id):
        """Returns a long url corresponding to the short one"""
        key = str(short_url_id)
        try:
            return self._container[key]['long_url']
        except KeyError:
            return None
    
    def key_exists(self, key):
        return key in self._container
    
    def long_url_exists(self, long_url):
        # At the moment I don't care if the URL already exists:
        return False

    def num_entries(self):
        return len(self._container)
    
    def get_all_urls(self):
        urls = dict()
        for key in self._container:
            urls[key] = self._container[key]['long_url']
        return urls

    def get_all_entries(self):
        urls = dict()
        for key in self._container:
            urls[key] = self._container[key]
        return urls

    @staticmethod
    def valid_long_url(long_url):
        return long_url.startswith('http://') or long_url.startswith('https://')

