"""The Bluetti BT integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant


PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]

type BluettiBtConfigEntry = ConfigEntry[dict[str, str]]


async def async_setup_entry(hass: HomeAssistant, entry: BluettiBtConfigEntry) -> bool:
    """Set up Bluetti BT from a config entry."""

    # entry.runtime_data.setdefault({})

    return True


async def async_unload_entry(hass: HomeAssistant, entry: BluettiBtConfigEntry) -> bool:
    """Unload Bluetti BT config entry."""

    # TODO stop coordinator

    return True
