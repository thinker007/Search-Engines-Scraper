from curl_cffi import requests
from collections import namedtuple

from .config import TIMEOUT, PROXY, USER_AGENT
from . import utils as utl
from fake_useragent import UserAgent

class HttpClient(object):
    '''Performs HTTP requests. A `requests` wrapper, essentialy'''
    def __init__(self, timeout=TIMEOUT, proxy=PROXY):
        self.session = requests.Session(impersonate="chrome110")
        self.session.proxies = self._set_proxy(proxy)
        self.timeout = timeout
        self.response = namedtuple('response', ['http', 'html','req'])

    def get(self, page):
        '''Submits a HTTP GET request.'''
        page = self._quote(page)
        try:
            req = self.session.get(page, timeout=self.timeout)
            self.session.headers['Referer'] = page
        except requests.exceptions.RequestException as e:
            return self.response(http=0, html=e.__doc__,req=None)
        return self.response(http=req.status_code, html=req.text,req=req)
    
    def post(self, page, data):
        '''Submits a HTTP POST request.'''
        page = self._quote(page)
        try:
            req = self.session.post(page, data, timeout=self.timeout)
            self.session.headers['Referer'] = page
        except requests.exceptions.RequestException as e:
            return self.response(http=0, html=e.__doc__,req=None)
        return self.response(http=req.status_code, html=req.text,req=req)
    
    def _quote(self, url):
        '''URL-encodes URLs.'''
        if utl.decode_bytes(utl.unquote_url(url)) == utl.decode_bytes(url):
            url = utl.quote_url(url)
        return url
    
    def _set_proxy(self, proxy):
        '''Returns HTTP or SOCKS proxies dictionary.'''
        if proxy:
            if not utl.is_url(proxy):
                raise ValueError('Invalid proxy format!')
            proxy = {'http':proxy, 'https':proxy}
        return proxy

