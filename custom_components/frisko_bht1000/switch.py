from homeassistant.components.switch import SwitchEntity
from .const import *
from .entity import FriskoEntity
async def async_setup_entry(hass, entry, async_add_entities):
    c=entry.runtime_data; async_add_entities([x(c,d) for d in c.devices for x in (FriskoAuto,FriskoPower)])
class FriskoAuto(FriskoEntity, SwitchEntity):
    _attr_name="Tryb automatyczny"; _attr_icon="mdi:calendar-clock"
    def __init__(self,c,d): super().__init__(c,d); self._attr_unique_id=f"{c.entry.entry_id}_{self.slave}_auto"
    @property
    def is_on(self): return self.d["mode_raw"]==MODE_AUTO
    async def async_turn_on(self, **kwargs): await self.coordinator.async_write(self.slave,REG_MODE,MODE_AUTO)
    async def async_turn_off(self, **kwargs): await self.coordinator.async_write(self.slave,REG_MODE,MODE_MANUAL)
class FriskoPower(FriskoEntity, SwitchEntity):
    _attr_name="Zasilanie"; _attr_icon="mdi:power"
    def __init__(self,c,d): super().__init__(c,d); self._attr_unique_id=f"{c.entry.entry_id}_{self.slave}_power"
    @property
    def is_on(self): return self.d["power_raw"]==POWER_ON
    async def async_turn_on(self, **kwargs): await self.coordinator.async_write(self.slave,REG_POWER,POWER_ON)
    async def async_turn_off(self, **kwargs): await self.coordinator.async_write(self.slave,REG_POWER,POWER_OFF)
