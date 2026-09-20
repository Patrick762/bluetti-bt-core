"""Sensor for Bluetti BT integration."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import BluettiBtConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BluettiBtConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Setup sensor entities."""

    device = entry.runtime_data.device

    sensor_fields = device.get_sensor_fields()

    for field in sensor_fields:
        pass

    # TODO


class BluettiSensor(CoordinatorEntity, SensorEntity):
    """Bluetti universal sensor."""

    # TODO

    pass
