from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from .entity import FriskoEntity
async def async_setup_entry(hass, entry, async_add_entities):
    c=entry.runtime_data; async_add_entities([FriskoHeating(c,d) for d in c.devices])
class FriskoHeating(FriskoEntity, BinarySensorEntity):
    _attr_name="Ogrzewanie"; _attr_device_class=BinarySensorDeviceClass.HEAT
    def __init__(self,c,d): super().__init__(c,d); self._attr_unique_id=f"{c.entry.entry_id}_{self.slave}_heating"
    @property
    def is_on(self): return self.d["heating"]
