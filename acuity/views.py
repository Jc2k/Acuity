import os
import urllib

from twisted.web.http import parse_qs

from acuity.cmdresources import Jinja

class DirList(Jinja):

    LIST_AT_TOP = ['syslog']

    def dir_order(self, d):
        '''
        Order the directory listing, putting any special items at the top
        '''
        s = sorted(d)
        for f in self.LIST_AT_TOP:
           if f in s:
               s.insert(0, f)
        return s

    def render_POST(self, request):
        '''
        jQuery view for presenting files
        '''
        # FIXME: I should probably be a template
        args = parse_qs(request.content.getvalue())
        r=['<ul class="jqueryFileTree" style="display: none;">']
        try:
            r=['<ul class="jqueryFileTree" style="display: none;">']
            print request.content.getvalue()
            d=urllib.unquote(args.get('dir', ['/var/log/'])[0])
            print request.args
            for f in self.dir_order(os.listdir(d)):
                ff=os.path.join(d,f)
                extra_class = f in self.LIST_AT_TOP and "special " or ""
                if os.path.isdir(ff):
                    r.append('<li class="%sdirectory collapsed"><a href="#" rel="%s/">%s</a></li>' % (extra_class, ff,f))
                else:
                    e=os.path.splitext(f)[1][1:] # get .ext and remove dot
                    r.append('<li class="%sfile ext_%s"><a href="#" rel="%s">%s</a></li>' % (extra_class, e,ff,f))
            r.append('</ul>')
        except Exception,e:
            r.append('Could not load directory: %s' % str(e))
        r.append('</ul>')

        return (''.join(r)).encode("UTF-8")
