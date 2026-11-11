from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
class FriskoEntity(CoordinatorEntity):
    _attr_has_entity_name = True
    def __init__(self, coordinator, device):
        super().__init__(coordinator)
        self.slave = device["slave"]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{coordinator.entry.entry_id}_{self.slave}")},
            name=device["name"], manufacturer="Frisko", model="BHT-1000-M",
            configuration_url=None,
        )
    @property
    def available(self):
        return super().available and self.slave in (self.coordinator.data or {})
    @property
    def d(self): return self.coordinator.data[self.slave]
