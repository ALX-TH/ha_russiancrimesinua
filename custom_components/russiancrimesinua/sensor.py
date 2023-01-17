"""Platform for sensor integration."""
from __future__ import annotations
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
    SensorEntityDescription,
)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle


import logging
import json
from datetime import timedelta
from .api import Communications
from .const import (
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=600)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup sensor platform."""
    _LOGGER.debug("custom_components.{}: async_setup_platform".format(DOMAIN))
    async_add_entities([RussiancrimesinUaSensor(hass, 'aircraft')], update_before_add=True)
    async_add_entities([RussiancrimesinUaSensor(hass, 'artillery')], update_before_add=True)
    async_add_entities([RussiancrimesinUaSensor(hass, 'helicopters')], update_before_add=True)
    async_add_entities([RussiancrimesinUaSensor(hass, 'killed')], update_before_add=True)
    async_add_entities([RussiancrimesinUaSensor(hass, 'shipsBoats')], update_before_add=True)
    async_add_entities([RussiancrimesinUaSensor(hass, 'tanks')], update_before_add=True)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup sensor entry."""
    _LOGGER.debug("custom_components.{}: async_setup_entry".format(DOMAIN))
    hass.data.setdefault(DOMAIN, {})
    entry_id = config_entry.entry_id
    unique_id = config_entry.unique_id

    _LOGGER.debug('custom_components.%s: setup config entry: %s', DOMAIN, {
        'entry_id': entry_id,
        'unique_id': unique_id
    })

    await async_setup_platform(hass, config_entry, async_add_entities)
    return True

class RussiancrimesinUaSensor(Entity):

    def __init__(self, hass, name) -> None:
        """Initialize the data object."""
        self.hass = hass

        self._name = "{}_{}".format(DOMAIN, name.lower())
        self._state = None
        self._unique_id = "{}_{}".format(DOMAIN, name.lower())

        self.property_name = name
        _LOGGER.debug("{} sensor initialization".format(self._name))

    async def async_update(self) -> None:
        """Get the latest sensor information."""
        _LOGGER.debug("{} starting updating sensor dataset".format(self._name))

        clk = Communications()
        response = await clk.async_request()
        if response:
            self._state = response[self.property_name]
            _LOGGER.debug("server responded with: {}".format(response))

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self) -> str | None:
        """Return a unique ID."""
        return self._unique_id

    @property
    def icon(self):
        """Return a ICON."""

        if self.property_name == 'aircraft':
            return 'mdi:airplane'
        elif self.property_name == 'artillery':
            return 'mdi:train-car-flatbed-tank'
        elif self.property_name == 'helicopters':
            return 'mdi:helicopter'
        elif self.property_name == 'killed':
            return 'mdi:account'
        elif self.property_name == 'shipsBoats':
            return 'mdi:ferry'
        elif self.property_name == 'tanks':
            return 'mdi:tank'

        else:
            return 'mdi:code-not-equal'
