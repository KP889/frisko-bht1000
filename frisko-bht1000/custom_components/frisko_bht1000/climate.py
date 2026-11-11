from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import ClimateEntityFeature, HVACAction, HVACMode
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from .const import *
from .entity import FriskoEntity
async def async_setup_entry(hass, entry, async_add_entities):
    c=entry.runtime_data; async_add_entities([FriskoClimate(c,d) for d in c.devices])
class FriskoClimate(FriskoEntity, ClimateEntity):
    _attr_name=None; _attr_temperature_unit=UnitOfTemperature.CELSIUS
    _attr_hvac_modes=[HVACMode.HEAT,HVACMode.OFF]
    _attr_supported_features=ClimateEntityFeature.TARGET_TEMPERATURE
    _attr_target_temperature_step=0.5; _attr_min_temp=17; _attr_max_temp=24
    def __init__(self,c,d): super().__init__(c,d); self._attr_unique_id=f"{c.entry.entry_id}_{self.slave}_climate"
    @property
    def current_temperature(self): return self.d["current_temperature"]
    @property
    def target_temperature(self): return self.d["target_temperature"]
    @property
    def hvac_mode(self): return HVACMode.OFF if self.d["power_raw"]==POWER_OFF else HVACMode.HEAT
    @property
    def hvac_action(self):
        if self.hvac_mode==HVACMode.OFF: return HVACAction.OFF
        return HVACAction.HEATING if self.d["heating"] else HVACAction.IDLE
    async def async_set_temperature(self, **kwargs):
        if (temp:=kwargs.get(ATTR_TEMPERATURE)) is not None:
            await self.coordinator.async_write(self.slave,REG_TARGET_TEMP,round(float(temp)/TEMP_SCALE))
    async def async_set_hvac_mode(self, mode):
        await self.coordinator.async_write(self.slave,REG_POWER,POWER_OFF if mode==HVACMode.OFF else POWER_ON)
