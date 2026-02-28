from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HyprlandCoordinator


PROGRAMS = {
    "Firefox": "firefox",
    "Terminal": "kitty",
    "VS Code": "code",
}


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: HyprlandCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        HyprlandLaunchButton(coordinator, entry, name, command)
        for name, command in PROGRAMS.items()
    ]

    async_add_entities(entities)


class HyprlandLaunchButton(
    CoordinatorEntity[HyprlandCoordinator],
    ButtonEntity,
):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, name, command):
        super().__init__(coordinator)
        self._command = command
        self._attr_name = f"Open {name}"
        self._attr_unique_id = f"{entry.entry_id}_launch_{command}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
        }
        self._attr_icon = "mdi:application"

    async def async_press(self):
        await self.coordinator.client.exec(self._command)