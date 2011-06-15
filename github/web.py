import datetime, requests
try:
    import simplejson as json
except ImportError:
    import json

from errors import APIError

BASE_URL = 'https://api.github.com'


class JSONModel(object):

    _fetched = set()
    _ext = set()

    def __init__(self, data):
        for field in self._fields:
            if field in data:
                value = data[field]
                if field in ('created_at', 'updated_at', 'committed_at'):
                    value = self._create_datetime(value)
                setattr(self, field, value)
                self._fetched.add(field)
        if hasattr(self, '_extend'):
            self._extend(data)
        self._fetched.update(self._ext)

    def _create_datetime(self, v):
        _date, _time = v[:-1].split('T')
        date = datetime.date(*map(int, _date.split('-')))
        time = datetime.time(*map(int, _time.split(':')))
        return datetime.datetime.combine(date, time)

    def __str__(self):
        return self.__repr__()

    def __unicode__(self):
        return self.__str__()


class WebManager(object):

    def __getattr__(self, attr):
        if attr.lower() == 'patch':
            raise NotImplementedError('patch method not supported yet')
        elif attr.lower() in ('get', 'post', 'put', 'head'):
            return self._http_verb(attr)
        return super(WebManager, self).__getattribute__(attr)

    def _http_verb(self, method):
        def _verb(url):
            if not url.startswith('/'):
                url = '/' + url
            if not url.startswith('http'):
                url = BASE_URL + url
            func = getattr(requests, method)
            return self._loads(func(url))
        return _verb

    def _loads(self, response):
        data = json.loads(response.content)
        if response.status_code == 404:
            raise APIError('%s at %s' % (str(data['message']), response.url))
        return data