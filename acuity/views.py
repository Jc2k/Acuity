import os
import urllib
from django.http import HttpResponse

LIST_AT_TOP = ['syslog']

def dir_order(d):
   '''
   Order the directory listing, putting any special items at the top
   '''
   s = sorted(d)
   
   for f in LIST_AT_TOP:
      if f in s:
         s.insert(0, s.pop(s.index(f)))
   return s

def dirlist(request):
   '''
   jQuery view for presenting files
   '''
   r=['<ul class="jqueryFileTree" style="display: none;">']
   try:
       r=['<ul class="jqueryFileTree" style="display: none;">']
       d=urllib.unquote(request.POST.get('dir','/var/log/'))
       for f in dir_order(os.listdir(d)):
           ff=os.path.join(d,f)
           extra_class = f in LIST_AT_TOP and "special " or ""
           if os.path.isdir(ff):
               r.append('<li class="%sdirectory collapsed"><a href="#" rel="%s/">%s</a></li>' % (extra_class, ff,f))
           else:
               e=os.path.splitext(f)[1][1:] # get .ext and remove dot
               r.append('<li class="%sfile ext_%s"><a href="#" rel="%s">%s</a></li>' % (extra_class, e,ff,f))
       r.append('</ul>')
   except Exception,e:
       r.append('Could not load directory: %s' % str(e))
   r.append('</ul>')
   return HttpResponse(''.join(r))
