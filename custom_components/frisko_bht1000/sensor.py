from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import UnitOfTemperature
from .entity import FriskoEntity
async def async_setup_entry(hass, entry, async_add_entities):
    c=entry.runtime_data; async_add_entities([FriskoTemperature(c,d) for d in c.devices])
class FriskoTemperature(FriskoEntity, SensorEntity):
    _attr_name="Temperatura"; _attr_device_class=SensorDeviceClass.TEMPERATURE
    _attr_state_class=SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement=UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision=1
    def __init__(self,c,d): super().__init__(c,d); self._attr_unique_id=f"{c.entry.entry_id}_{self.slave}_temperature"
    @property
    def native_value(self): return self.d["current_temperature"]
