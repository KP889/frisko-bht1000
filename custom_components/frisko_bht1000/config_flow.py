from __future__ import annotations
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_PORT
CONF_BAUDRATE = "baudrate"
from homeassistant.config_entries import ConfigFlowResult
from .const import CONF_DEVICES, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN

CONF_BYTESIZE = "bytesize"
CONF_PARITY = "parity"
CONF_STOPBITS = "stopbits"
CONF_SLAVE = "slave"
CONF_ADD_ANOTHER = "add_another"

class FriskoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self) -> None:
        self._hub: dict[str, Any] = {}
        self._devices: list[dict[str, Any]] = []

    async def async_step_user(
        self,
        user_input=None) -> ConfigFlowResult:
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_PORT])
            self._abort_if_unique_id_configured()
            self._hub = dict(user_input)
            return await self.async_step_device()
        schema = vol.Schema({
            vol.Required(CONF_NAME, default="hub1"): str,
            vol.Required(CONF_PORT, default="/dev/ttyUSB0"): str,
            vol.Required(CONF_BAUDRATE, default=9600): vol.In([1200,2400,4800,9600,19200,38400,57600,115200]),
            vol.Required(CONF_BYTESIZE, default=8): vol.In([7,8]),
            vol.Required(CONF_PARITY, default="N"): vol.In(["N","E","O"]),
            vol.Required(CONF_STOPBITS, default=1): vol.In([1,2]),
            vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(int, vol.Range(min=5,max=300)),
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    async def async_step_device(self, user_input=None) -> ConfigFlowResult:
        errors = {}
        if user_input is not None:
            slave = int(user_input[CONF_SLAVE])
            if any(d[CONF_SLAVE] == slave for d in self._devices):
                errors["base"] = "duplicate_slave"
            else:
                self._devices.append({CONF_NAME: user_input[CONF_NAME], CONF_SLAVE: slave})
                if user_input[CONF_ADD_ANOTHER]:
                    return await self.async_step_device()
                data = dict(self._hub)
                data[CONF_DEVICES] = self._devices
                return self.async_create_entry(title=self._hub[CONF_NAME], data=data)
        schema = vol.Schema({
            vol.Required(CONF_NAME): str,
            vol.Required(CONF_SLAVE): vol.All(int, vol.Range(min=1,max=247)),
            vol.Required(CONF_ADD_ANOTHER, default=False): bool,
        })
        return self.async_show_form(step_id="device", data_schema=schema, errors=errors)
