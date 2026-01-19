from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import HyprlandCoordinator
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: HyprlandCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        HyprlandOnlineSensor(coordinator, entry),
    ])

class HyprlandOnlineSensor(
    CoordinatorEntity[HyprlandCoordinator],
    BinarySensorEntity,
):
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_online"
        self._attr_name = "Online"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
        }

    @property
    def is_on(self) -> bool:
        # coordinator.data is None als de update faalt
        return self.coordinator.last_update_success
