import sys
import os

from twisted.application import internet, service
from twisted.web import server, resource, wsgi, static
from twisted.python import threadpool
from twisted.internet import reactor

import cmdresources

PORT = 8000

# Environment setup for your Django project files:
sys.path.append("acuity")
os.environ['DJANGO_SETTINGS_MODULE'] = 'acuity.settings'
from django.core.handlers.wsgi import WSGIHandler

def wsgi_resource():
    pool = threadpool.ThreadPool()
    pool.start()
    # Allow Ctrl-C to get you out cleanly:
    reactor.addSystemEventTrigger('after', 'shutdown', pool.stop)
    wsgi_resource = wsgi.WSGIResource(reactor, pool, WSGIHandler())
    return wsgi_resource


# Twisted Application Framework setup:
application = service.Application('twisted-django')

# WSGI container for Django, combine it with twisted.web.Resource:
wsgi_root = wsgi_resource()
root = cmdresources.Root(wsgi_root)

# Servce Django media files off of /media:
staticrsrc = static.File(os.path.join(os.path.abspath("."), "acuity/media"))
root.putChild("media", staticrsrc)

# The cool part! Add in pure Twisted Web Resouce in the mix
# This 'pure twisted' code could be using twisted's XMPP functionality, etc:
root.putChild("perform", cmdresources.ShellResource())

# Serve it up:
main_site = server.Site(root)
internet.TCPServer(PORT, main_site).setServiceParent(application)
