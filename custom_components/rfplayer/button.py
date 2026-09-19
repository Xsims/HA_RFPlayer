"""Support for RfPlayer button entities."""

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity_registry import EntityCategory

from custom_components.rfplayer.const import DOMAIN
from custom_components.rfplayer.number import JAMMING_DEVICE_IDENTIFIERS
from custom_components.rfplayer.runtime import RfPlayerConfigEntry

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: RfPlayerConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the jamming simulate button entity."""
    gateway = config_entry.runtime_data.gateway
    async_add_entities([RfplayerJammingSimulateButton(gateway)])


class RfplayerJammingSimulateButton(ButtonEntity):
    """Button to simulate RF jamming on the RfPlayer."""

    _attr_has_entity_name = True
    _attr_name = "Jamming simulate"
    _attr_unique_id = "rfplayer_jamming_simulate"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_device_info = {"identifiers": JAMMING_DEVICE_IDENTIFIERS}

    def __init__(self, gateway) -> None:
        """Initialize the jamming simulate button."""
        self._gateway = gateway

    async def async_press(self) -> None:
        """Send the JAMMING SIMULATE command."""
        _LOGGER.debug("Press jamming simulate")
        await self._gateway.client.send_raw_command("JAMMING SIMULATE")
