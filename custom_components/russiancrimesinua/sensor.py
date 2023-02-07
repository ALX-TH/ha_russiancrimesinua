"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
    SensorEntityDescription,
)
from homeassistant.const import (
    ATTR_ATTRIBUTION,
)

import logging
import time
from typing import Any
from datetime import timedelta
from .api import Communications
from .const import (
    DOMAIN,
    UPDATE_INTERVAL,
    ATTR_IMG_EN,
    ATTR_IMG_UA
)

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=UPDATE_INTERVAL)

SENSOR_METADATA = "updater"
SENSORS_LIST = {
    SENSOR_METADATA : [SENSOR_METADATA, "mdi:clock-check-outline", None],
    "killed" : ["killed", "mdi:face-man", None],
    "aircraft" : ["aircraft", "mdi:airplane", None],
    "artillery": ["artillery", "mdi:train-car-flatbed-tank", None],
    "helicopters": ["helicopters", "mdi:helicopter", None],
    "ships" : ["shipsBoats", "mdi:ferry", None],
    "tanks" : ["tanks", "mdi:tank", None],
    "vehicles" : ["armoredCombatVehicles", "mdi:car-estate", None]
}


async def async_setup_platform(hass: HomeAssistant, 
                               config_entry: ConfigType, 
                               async_add_entities: AddEntitiesCallback,
                               discovery_info: DiscoveryInfoType | None = None) -> None:
    """Setup sensor platform."""
    _LOGGER.debug("{} async_setup_platform".format(DOMAIN))
    
    coordinator = SensorCoordinator(hass)
    entities = []
    for sensor in SENSORS_LIST:
        entities.append(RussiancrimesinUaSensor(hass, coordinator, sensor))
    async_add_entities(entities, update_before_add=True)
    
    
async def async_setup_entry(hass: HomeAssistant, 
                            config_entry: ConfigType, 
                            async_add_entities: AddEntitiesCallback):
    """Setup sensor entry."""
    _LOGGER.debug("{} async_setup_entry".format(DOMAIN))
    return True


class SensorCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=timedelta(minutes=UPDATE_INTERVAL))
        self.clk = Communications()
        _LOGGER.debug("Registering SensorCoordinator")
        
    async def _async_update_data(self):
        response = await self.clk.async_request()
        _LOGGER.debug("SensorCoordinator received data: {}".format(response))
        return response
        

class RussiancrimesinUaSensor(CoordinatorEntity, SensorEntity):

    def __init__(self, hass, coordinator, sensor) -> None:
        super().__init__(coordinator, context=sensor)
        
        """Initialize the sensor object."""
        self.hass = hass
        self.coordinator = coordinator
        self.sensor = sensor
        self.key = SENSORS_LIST[sensor][0]
        
        self._name = "{}_{}".format(DOMAIN, sensor)
        self._state = None
        self._icon = SENSORS_LIST[sensor][1]
        self._unit_of_measurement = SENSORS_LIST[sensor][2]
        self._unique_id = "{}_{}".format(DOMAIN, self.key.lower())
        self._attr_extra_state_attributes = {}
        self._device_class = None
        self._state_class = None
        self._data = None
        _LOGGER.debug("{} sensor initialization".format(self._name))

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._data = self.coordinator.data
        
        """update custom sensor for handeling metadata"""
        if self.sensor == SENSOR_METADATA:
            if self._data:
                self._state = "on"
                self._attr_extra_state_attributes.update({
                        ATTR_IMG_EN: self._data[ATTR_IMG_EN],
                        ATTR_IMG_UA: self._data[ATTR_IMG_UA]
                })
                self._state_class = 'measurement'
                self._device_class = 'update'
        
        else:
            """update confirured sensors for handeling states""" 
            self._state = self.coordinator.data[self.key]
            
        self.async_write_ha_state()
        _LOGGER.debug("handle_coordinator_update for sensor {} with uuid {}. value: {}".format(self._name, self._unique_id, self._state))



    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name


    @property
    def state(self) -> int | None:
        """Return the state of the sensor."""
        return self._state


    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._unique_id
    
    
    @property
    def unit_of_measurement(self) -> str | None:
        """Return a unit of measurement"""
        return self._unit_of_measurement
    
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return a extra attributes"""
        return self._attr_extra_state_attributes
    
    
    @property
    def device_class(self) -> str | None:
        """Return a device class"""    
        return self._device_class


    @property
    def icon(self) -> str | None:
        """Return a ICON."""
        return self._icon
