import asyncio
import json
import logging
import random
import re
import aiohttp
import async_timeout
import os
import requests

_LOGGER = logging.getLogger(__name__)

HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

class Communications(object):

    def __init__(self) -> None:
        self.API_URL = "https://www.russiancrimes.in.ua/stats.json"
        self.response = None

    async def _async_request(self, method="get", data=None):
        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession() as session:
                async with session.get(self.API_URL, headers=HTTP_HEADERS, timeout=timeout) as response:
                    if response.status == 401:
                        _LOGGER.error("[ASYNC] Could not get info from %s: 401".format(self.API_URL))
                        return None
                    self.response = await response.json()
                    _LOGGER.debug("[ASYNC] custom_components.russiancrimesinua: got response from upstream: {}".format(self.response))
                session.close()
                return self.response
        except (asyncio.TimeoutError, aiohttp.ClientError) as error:
            _LOGGER.error("[ASYNC] Could not get info from {}: {}".format(self.API_URL, error))

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
