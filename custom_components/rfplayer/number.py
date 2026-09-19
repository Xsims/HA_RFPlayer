"""Support for RfPlayer number entities."""

import logging

from custom_components.rfplayer.const import DOMAIN
from custom_components.rfplayer.runtime import RfPlayerConfigEntry
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity_registry import EntityCategory
from homeassistant.helpers.restore_state import RestoreEntity

_LOGGER = logging.getLogger(__name__)

JAMMING_DEVICE_ID = "JAMMING-0"
JAMMING_DEVICE_IDENTIFIERS = {(DOMAIN, JAMMING_DEVICE_ID)}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: RfPlayerConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the jamming number entity."""
    gateway = config_entry.runtime_data.gateway
    async_add_entities([RfplayerJammingNumber(gateway)])


class RfplayerJammingNumber(RestoreEntity, NumberEntity):
    """Slider to configure the RfPlayer jamming detection level."""

    _attr_has_entity_name = True
    _attr_name = "Jamming detection level"
    _attr_unique_id = "rfplayer_jamming_detection_level"
    _attr_native_min_value = 0
    _attr_native_max_value = 10
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER
    _attr_entity_category = EntityCategory.CONFIG
    _attr_device_info = {"identifiers": JAMMING_DEVICE_IDENTIFIERS}

    def __init__(self, gateway) -> None:
        """Initialize the jamming level entity."""
        self._gateway = gateway
        self._value: float | None = None

    async def async_added_to_hass(self) -> None:
        """Restore the last known jamming level."""
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) and last_state.state not in (
            STATE_UNKNOWN,
            STATE_UNAVAILABLE,
        ):
            try:
                self._value = float(last_state.state)
            except ValueError:
                _LOGGER.warning("Could not restore jamming level from %s", last_state.state)

    @property
    def native_value(self) -> float | None:
        """Return the current jamming level."""
        return self._value

    async def async_set_native_value(self, value: float) -> None:
        """Send the JAMMING command with the new level."""
        await self._gateway.client.send_raw_command(f"JAMMING {int(value)}")
        self._value = int(value)
        self.async_write_ha_state()
