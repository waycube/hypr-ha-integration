from homeassistant.components.select import SelectEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HyprlandCoordinator


WORKSPACES = [f"Workspace {i}" for i in range(1, 11)]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator: HyprlandCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        HyprlandWorkspaceSelect(coordinator, entry),
    ])


class HyprlandWorkspaceSelect(
    CoordinatorEntity[HyprlandCoordinator],
    SelectEntity,
):
    _attr_has_entity_name = True
    _attr_name = "Workspace"
    _attr_icon = "mdi:view-grid"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_workspace_select"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
        }
        self._attr_options = WORKSPACES

    @property
    def current_option(self):
        if not self.coordinator.data:
            return None

        workspace = self.coordinator.data.get("workspace")
        if workspace is None:
            return None

        return f"Workspace {workspace}"

    async def async_select_option(self, option: str):
        # option = "Workspace X"
        workspace = int(option.split(" ")[1])
        await self.coordinator.client.set_workspace(workspace)

        # Forceer directe refresh zodat UI meteen klopt
        await self.coordinator.async_request_refresh()
