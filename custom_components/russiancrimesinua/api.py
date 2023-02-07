import asyncio
import json
import logging
import aiohttp
import os
import requests
from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)

CACHE_TTL_MINUTES=15

HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

class Cache(object):
    """ Custom caching implementation """
    def __init__(self) -> None:
        self.path = self._get_cache_location()
        self.ttl = timedelta(minutes=CACHE_TTL_MINUTES)
        self._create_cache()

    def _create_cache(self) -> None:
        """ create cache file at filesystem """
        if not os.path.exists(self.path):
            with open(self.path, 'w'): pass
            
    def _get_cache_location(self) -> str:
        """ get cache absolete path """
        cwd = os.path.realpath(__file__)
        dir = os.path.dirname(cwd)
        path = os.path.join(dir,'http.cache.json')
        return path

    def _is_file_older_than(self) -> bool:
        """  chech if file older that time """
        offset = datetime.utcnow() - self.ttl
        mtime = datetime.utcfromtimestamp(os.path.getmtime(self.path))
        if mtime < offset:
            return True
        return False
    
    def _is_empty_file(self) -> bool:
        """ check if file is empty """
        try:
            with open(self.path, 'r') as file:
                if file.read():
                    return False
                else:
                    return True
        except FileNotFoundError:
            return False
        
    def write(self, content) -> None:
        """ write json dict to a file """
        with open(self.path, mode="w", encoding="utf-8") as file:
            json.dump(content, file)
            file.close()
            
    def read(self) -> None:
        """ read json dict from a file """
        with open(self.path, mode="r", encoding="utf-8") as file:
            return json.load(file)
            
    def expired(self) -> bool:
        """ check cache for expire """
        if self._is_empty_file():
            return True
        
        if self._is_file_older_than():
            _LOGGER.debug("Cache is expired. Needs to be revalidated")
            return True
        else:
            _LOGGER.debug("Cache is not older thant ttl configured.")
            return False


class Communications(object):

    def __init__(self) -> None:
        self.API_URL = "https://www.russiancrimes.in.ua/stats.json"
        self.response = None
        self.cache = Cache()

    async def _async_request(self):
        
        """ check cache """
        expired = self.cache.expired()

        if expired:
            """ send async request to upstream """
            _LOGGER.debug("[ASYNC] Cache expired. Fetching latest data from resource {}".format(self.API_URL))
            try:
                timeout = aiohttp.ClientTimeout(total=30)
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.API_URL, headers=HTTP_HEADERS, timeout=timeout) as response:
                        if response.status == 401:
                            _LOGGER.error("[ASYNC] Could not get info from %s: 401".format(self.API_URL))
                            return None
                        self.response = await response.json()
                        _LOGGER.debug("[ASYNC] custom_components.russiancrimesinua: got response from upstream: {}".format(self.response))
                    #session.close()
                    self.cache.write(self.response)
                    return self.response
            except (asyncio.TimeoutError, aiohttp.ClientError) as error:
                _LOGGER.error("[ASYNC] Could not get info from {}: {}".format(self.API_URL, error))
        else:
            """ read cached response """
            _LOGGER.debug("[ASYNC] Cache was not expired. Reading data from cache.")
            return self.cache.read()

    def _request(self, method="get", data=None):
        session = requests.Session()
        try:
            response = session.get(self.API_URL, verify=True, timeout=self.API_TIMEOUT)
            if response.status_code == 401:
                _LOGGER.error("[N_ASYNC] Could not get info from {}: 401".format(self.API_URL))
                return None

            _LOGGER.debug("[N_ASYNC] custom_components.russiancrimesinua: got response from upstream: {}".format(response.json()))
            session.close()
            return response.json()
        except Exception as error:
            _LOGGER.error("[N_ASYNC] Could not get info from {}: {}".format(self.API_URL, error))

    async def async_request(self) -> any:
        self.response = await self._async_request()
        return self.response

    def request(self) -> any:
        self.response = self._request()
        return self.response
