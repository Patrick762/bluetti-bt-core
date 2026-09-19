import logging
import json

from habluetooth import BluetoothServiceInfoBleak
from homeassistant import config_entries
from homeassistant.const import CONF_ADDRESS, CONF_MODEL, CONF_API_VERSION
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

from .const import DOMAIN, CONF_ENCRYPTION

_LOGGER = logging.getLogger(__name__)


class BluettiConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow for Bluetti BT devices."""

    def __init__(self) -> None:
        """Initialize config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_devices: dict[str, BluetoothServiceInfoBleak] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> FlowResult:
        """Handle bluetooth discovery."""
        _LOGGER.debug(f"Discovered matching device {discovery_info.name}")
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()

        discovery_info.manufacturer_data = {}

        self._discovery_info = discovery_info
        self.context["title_placeholders"] = {"name": discovery_info.name}
        return await self.async_step_user()

    async def async_step_user(
        self, user_input: dict[str, any] | None = None
    ) -> FlowResult:
        """Handle user input."""

        # Handle discovery proceed setup
        if user_input is not None:
            await self.async_set_unique_id(self._discovery_info.address, raise_on_progress=False)
            self._abort_if_unique_id_configured()

            # Run model detection
            # TODO

            # Save entry
            return self.async_create_entry(
                title=self._discovery_info.name,
                data={
                    CONF_ADDRESS: self._discovery_info.address,
                    CONF_MODEL: "Dummy",
                    CONF_API_VERSION: 1,
                    CONF_ENCRYPTION: False,
                },
            )

        if not self._discovery_info:
            return self.async_abort(reason="no_unconfigured_devices")

        # We don't have manual configs, only via discovery
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
        )
