import requests
from requests.api import get
from requests.api import post
from requests.api import request


class Requests:
    def __init__(self, uri, isGet):
        self._uri = uri
        self._isGet = isGet

    def _requests(self, addr) -> request:
        if self._isGet:
            return get(self._uri + addr)
        else:
            return post(self._uri + addr)
