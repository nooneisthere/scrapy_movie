import re

class urlHelper:
    def makeURL(url, domain):
        if (url.startswith('http')):
            return url;
        elif (url.startswith('/')):
            return domain + url
        elif (url.startswith('javascript')):
            return ''
        else:
            return ''

    def validSource(url):
        valid = ('ed2k', 'magnet' ,'thunder')
        for st in valid:
            if url.startswith(st): return st

        for st in ('http://pan.', 'https://pan.'):
            if url.startswith(st): return 'pan'

    def getURI(url):
        match=re.match(r'^http[s]?://.+?/(.+)$',url)
        if match:
            return match.group(1)

