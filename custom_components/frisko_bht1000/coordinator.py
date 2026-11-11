from __future__ import annotations
import asyncio
from datetime import timedelta
import logging
from pymodbus.client import ModbusSerialClient
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_BAUDRATE, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import *
_LOGGER = logging.getLogger(__name__)

class FriskoCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        self.devices = entry.data[CONF_DEVICES]
        self._lock = asyncio.Lock()
        self.client = ModbusSerialClient(
            port=entry.data[CONF_PORT], baudrate=entry.data[CONF_BAUDRATE],
            bytesize=entry.data["bytesize"], parity=entry.data["parity"],
            stopbits=entry.data["stopbits"], timeout=2,
        )
        super().__init__(hass, _LOGGER, name=DOMAIN,
            update_interval=timedelta(seconds=entry.data[CONF_SCAN_INTERVAL]))

    def _read(self, address, count, slave):
        try:
            return self.client.read_holding_registers(address=address, count=count, device_id=slave)
        except TypeError:
            return self.client.read_holding_registers(address=address, count=count, slave=slave)

    def _write(self, address, value, slave):
        try:
            return self.client.write_register(address=address, value=value, device_id=slave)
        except TypeError:
            return self.client.write_register(address=address, value=value, slave=slave)

    def _poll_sync(self):
        if not self.client.connected and not self.client.connect():
            raise ConnectionError("Nie można otworzyć portu RS485")
        output = {}
        for device in self.devices:
            slave = device["slave"]
            response = self._read(0, 10, slave)
            if response.isError():
                raise ConnectionError(f"Brak odpowiedzi slave {slave}: {response}")
            r = response.registers
            output[slave] = {
                "name": device["name"], "power_raw": r[REG_POWER],
                "current_temperature": r[REG_CURRENT_TEMP] * TEMP_SCALE,
                "heating": bool(r[REG_HEATING]), "mode_raw": r[REG_MODE],
                "target_temperature": r[REG_TARGET_TEMP] * TEMP_SCALE,
            }
        return output

    async def _async_update_data(self):
        async with self._lock:
            try:
                return await self.hass.async_add_executor_job(self._poll_sync)
            except Exception as err:
                raise UpdateFailed(str(err)) from err

    async def async_write(self, slave: int, address: int, value: int) -> None:
        async with self._lock:
            def job():
                if not self.client.connected and not self.client.connect():
                    raise ConnectionError("Brak połączenia Modbus")
                response = self._write(address, value, slave)
                if response.isError():
                    raise ConnectionError(str(response))
            await self.hass.async_add_executor_job(job)
        await self.async_request_refresh()

    async def async_close(self):
        await self.hass.async_add_executor_job(self.client.close)
