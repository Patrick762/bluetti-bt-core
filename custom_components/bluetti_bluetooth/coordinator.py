"""Coordinator for Bluetti BT integration."""

import asyncio
from datetime import timedelta
from enum import Enum
import logging
from typing import override

from bluetti_bt_lib import DeviceReader, DeviceReaderConfig
from bluetti_bt_lib.utils import build_device

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS, CONF_API_VERSION, CONF_MODEL
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady, HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_ENCRYPTION, DOMAIN

type BluettiBtConfigEntry = ConfigEntry[BluettiBluetoothCoordinator]


class BluettiBluetoothCoordinator(DataUpdateCoordinator):
    """Polling coordinator."""

    config_entry: BluettiBtConfigEntry

    def __init__(self, hass: HomeAssistant, config_entry: BluettiBtConfigEntry) -> None:
        """Initialize coordinator."""

        self.mac = config_entry.data.get(CONF_ADDRESS)
        self.mac_str = str(self.mac).replace(":", "")

        super().__init__(
            hass,
            logging.getLogger(f"{__name__}.{self.mac_str}"),
            config_entry=config_entry,
            name=f"{DOMAIN}.{self.mac_str}",
            update_interval=timedelta(seconds=60),
        )

        self.device = build_device(config_entry.data.get(CONF_MODEL))

        if self.device is None:
            raise HomeAssistantError("Unknown device")

    @override
    async def _async_update_data(
        self,
    ) -> dict[str, bool | int | float | Enum | str | bytes]:
        """Fetch data from bluetooth device."""

        ble_device = bluetooth.async_ble_device_from_address(
            self.hass, str(self.mac), connectable=True
        )

        if ble_device is None:
            raise ConfigEntryNotReady(f"Cannot connect to {self.mac}")

        reader = DeviceReader(
            self.mac,
            self.device,
            self.hass.loop.create_future,
            DeviceReaderConfig(
                use_encryption=self.config_entry.data.get(CONF_ENCRYPTION),
            ),
            ble_device=ble_device,
            lock=asyncio.Lock(),
        )

        if (
            bluetooth.async_address_present(self.hass, str(self.mac), connectable=True)
            is False
        ):
            raise UpdateFailed("Device not connected")

        data: dict[str, bool | int | float | Enum | str | bytes] | None = (
            await reader.read()
        )

        if not data:
            raise UpdateFailed("Device returned no data")

        self.logger.debug("Device data: %s", data)

        return data
