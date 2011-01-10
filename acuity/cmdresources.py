from twisted.internet import protocol
from twisted.internet import reactor
from twisted.web import resource
from twisted.web.server import NOT_DONE_YET
import re
import os
import cgi

from jinja2 import Environment, PackageLoader

class ShellHTTP(protocol.ProcessProtocol):
    def __init__(self, request):
        self.request = request
        self.data = ""
        self.css = "<style>body pre {margin: 10px; padding-top: 10px; font-family: 'Monaco', 'Deja Vu Sans Mono', 'Inconsolata' ,'Consolas',monospace; background:#111 none repeat scroll 0 0; color:#fff; font-size:10px;}</style>"
    def connectionMade(self):
        print "connectionMade!"
    def outReceived(self, data):
        # Write stdout data from process to HTTP request
        self.request.write(data)
    def errReceived(self, data):
        print "errReceived! with %d bytes!" % len(data)
    def inConnectionLost(self):
        print "inConnectionLost! stdin is closed! (we probably did it)"
    def outConnectionLost(self):
        print "outConnectionLost! The child closed their stdout!"
        self.request.write('\nDone\n')
        self.request.finish()
    def errConnectionLost(self):
        print "errConnectionLost! The child closed their stderr."
    def processExited(self, reason):
        print "processExited, status %d" % (reason.value.exitCode,)
    def processEnded(self, reason):
        print "processEnded, status %d" % (reason.value.exitCode,)
        print "quitting"

class ShellResource(resource.Resource):
    def _responseFailed(self, err, process):
        process.signalProcess('KILL')

    def render_POST(self, request):
        request.setHeader("content-type", "text/plain")
        cmd = cgi.escape(request.args["tool"][0])
        filename = cgi.escape(request.args["file"][0])
        term = cgi.escape(request.args["term"][0])
        shell = ShellHTTP(request)
	
	if os.path.exists(os.path.realpath(filename)):
	    if cmd == 'tail':
		process = reactor.spawnProcess(shell, "tail", ["tail", "-f", filename], {})
	    if cmd == 'grep':
		if filename and os.path.splitext(filename)[1].lower() in ['.gz']:
		    process = reactor.spawnProcess(shell, "zgrep", ["zgrep", term, filename], {})
		else:
		    process = reactor.spawnProcess(shell, "grep", ["grep", term, filename], {})

        request.notifyFinish().addErrback(self._responseFailed, process)
        return NOT_DONE_YET

class Jinja(resource.Resource):

    def render_template(self, template, **kwargs):
        env = Environment(loader=PackageLoader("acuity", "templates"))
        template = env.get_template(template)
        return template.render(kwargs).encode("UTF-8")

class Root(Jinja):

    def render_GET(self, request):
        return self.render_template("index.html")

