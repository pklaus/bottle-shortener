This is a very primitive URL shortening service.
It runs on Python3 and can use any collection that looks
like a Python dictionary to store its data ('backend').

#### Backends

Currently it ships with the following backends:

* Python dictionary  
  All shortened URLs are lost when restarting the service.
* SQlite-Dictionary [FileDict](http://github.com/pklaus/filedict) for Python 3  
  Persistant storage in a database file.
* redis Plugin  
  Fast storage in memory; persistance possible via AOF (journal)

Other ideas for backends:

* memcached & pylibmc
  no persistance!
* any of [these](http://en.wikipedia.org/wiki/NoSQL)

#### Resources

* This code is loosly based on the shortener contained in [urltotwit](https://bitbucket.org/tarek/urltotwit).
