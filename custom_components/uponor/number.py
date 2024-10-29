import logging


from homeassistant.components.number import NumberEntity, NumberMode


from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from homeassistant.const import CONF_NAME
from .const import (
    DOMAIN,
    MIN_ECO_OFFSET,
    MAX_ECO_OFFSET
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):    

    state_proxy = hass.data[DOMAIN]["state_proxy"]
    async_add_entities([EcoOffsetTemp(entry.data[CONF_NAME], MIN_ECO_OFFSET, MAX_ECO_OFFSET, state_proxy)])

class EcoOffsetTemp(NumberEntity):
    def __init__(self, name, min_value, max_value, state_proxy):
        self._name = name
        self._attr_min_value = min_value
        self._attr_max_value = max_value

        self._attr_native_min_value = min_value  
        self._attr_native_max_value = max_value  
        self._attr_native_step = 0.5
        self._attr_value = 4        
        self._state_proxy = state_proxy
        self._attr_mode = NumberMode.BOX 

    
    @property
    def name(self) -> str:
        return self._name + " General Eco Offset"
   
    @property
    def min_value(self) -> float:
        return self._attr_min_value

    @property
    def max_value(self) -> float:
        return self._attr_max_value    
    
    @property
    def value(self):        
        _LOGGER.debug("Get Value: %s", self._state_proxy.get_eco_offset_temperature())
        return self._state_proxy.get_eco_offset_temperature()
       

    async def async_set_value(self, value):
    
        _LOGGER.debug("async_set_value :: Set Value: %s", value)
        
        if (value >= self._attr_min_value and value <= self._attr_max_value):
            self._attr_value = value
            await self._state_proxy.async_set_eco_offset_temperature(value)          
        

    @property
    def icon(self):
        return "mdi:temperature-celsius"

    @property
    def should_poll(self):
        return True    

    @property
    def unique_id(self):
        return self.name    