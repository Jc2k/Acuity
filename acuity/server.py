import os

from twisted.application import internet, service
from twisted.web import resource, server, static
from twisted.python import usage

from acuity import cmdresources, views

PORT = 8000


class Options(usage.Options):
    optParameters = [
        ]

def makeService(config):
    root = resource.Resource()

    root.putChild("", cmdresources.Root())

    # Servce Django media files off of /media:
    staticrsrc = static.File(os.path.join(os.path.dirname(__file__), "media"))
    root.putChild("static", staticrsrc)

    root.putChild("browse", views.DirList())

    # The cool part! Add in pure Twisted Web Resouce in the mix
    # This 'pure twisted' code could be using twisted's XMPP functionality, etc:
    root.putChild("perform", cmdresources.ShellResource())

    # Serve it up:
    main_site = server.Site(root)
    return internet.TCPServer(PORT, main_site)
