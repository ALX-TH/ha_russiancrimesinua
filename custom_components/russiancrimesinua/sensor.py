"""Platform for sensor integration."""
from __future__ import annotations
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
    SensorEntityDescription,
)
from homeassistant.const import (
    ATTR_DEVICE_CLASS,
    ATTR_ENTITY_ID,
    ATTR_UNIT_OF_MEASUREMENT,
    EVENT_HOMEASSISTANT_START,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    TEMP_CELSIUS,
)

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.util import Throttle, dt

try:
    from homeassistant.components.binary_sensor import BinarySensorEntity
except ImportError:
    from homeassistant.components.binary_sensor import (
        BinarySensorDevice as BinarySensorEntity,
    )

import logging
import json
import asyncio
from datetime import timedelta
from .api import Communications
from .const import (
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=60)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup sensor platform."""
    _LOGGER.debug("custom_components.{}: setting up integration".format(DOMAIN))
    sensor = SensorData()
    async_add_entities([RussiancrimesinUaSensor(sensor, 'aircraft')], True)
    async_add_entities([RussiancrimesinUaSensor(sensor, 'artillery')], True)
    async_add_entities([RussiancrimesinUaSensor(sensor, 'helicopters')], True)
    async_add_entities([RussiancrimesinUaSensor(sensor, 'killed')], True)
    async_add_entities([RussiancrimesinUaSensor(sensor, 'shipsBoats')], True)
    async_add_entities([RussiancrimesinUaSensor(sensor, 'tanks')], True)

class SensorData():
    def __init__(self) -> None:
        self.response = None

    def get_update(self):
        return self.response

    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the latest data and update the states."""
        _LOGGER.info("custom_components.{} sensor starting update".format(DOMAIN))
        clk = Communications()
        if self.response is None:
            self.response = clk.sync_request()
            _LOGGER.info("custom_components.{} sensor update result: {}".format(DOMAIN, self.response))

class RussiancrimesinUaSensor(Entity):

    def __init__(self, client: SensorData, name: str):
        """Initialize the data object."""
        self.client = client
        self._name = "{}_{}".format(DOMAIN, name)
        self._state = None
        self.response = None
        self.property_name = name
        _LOGGER.debug("custom_components. sensor initialization".format(DOMAIN))

    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the latest sensor information."""
        _LOGGER.debug("custom_components. updating sensor dataset".format(DOMAIN))
        self.client.update()
        self.response = self.client.get_update()

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return the unique id of the sensor."""
        _LOGGER.debug("custom_components.{} unique id: {}".format(DOMAIN, self._name))
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        self._state = self.response[self.property_name]
        _LOGGER.debug("custom_components.{} state: {}".format(DOMAIN, self._state))
        return self._state
