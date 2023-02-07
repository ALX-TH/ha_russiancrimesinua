""" Fetching data from russiancrimes.in.ua component """

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True