from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HyprlandCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: HyprlandCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        HyprlandWorkspaceSensor(coordinator, entry),
        HyprlandActiveAppSensor(coordinator, entry),
    ])


class HyprlandWorkspaceSensor(
    CoordinatorEntity[HyprlandCoordinator],
    SensorEntity,
):
    _attr_has_entity_name = True
    _attr_name = "Workspace"
    _attr_icon = "mdi:view-grid"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_workspace"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
        }

    @property
    def native_value(self):
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("workspace")


class HyprlandActiveAppSensor(
    CoordinatorEntity[HyprlandCoordinator],
    SensorEntity,
):
    _attr_has_entity_name = True
    _attr_name = "Active application"
    _attr_icon = "mdi:application"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_active_app"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
        }

    @property
    def native_value(self):
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get("app")

    @property
    def extra_state_attributes(self):
        if not self.coordinator.data:
            return {}
        return {
            "title": self.coordinator.data.get("title"),
        }
