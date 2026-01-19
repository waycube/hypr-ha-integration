from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import device_registry as dr

from .api import HyprApiClient
from .coordinator import HyprlandCoordinator
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry):
    session = async_get_clientsession(hass)
    client = HyprApiClient(
        entry.data["host"],
        entry.data["port"],
        session,
    )

    coordinator = HyprlandCoordinator(
        hass, client, entry.data["name"]
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # 👇 DEVICE REGISTRATIE
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        name=entry.data["name"],
        manufacturer="Hyprland",
        model="Wayland Desktop",
    )

    async def handle_set_workspace(call: ServiceCall):
        await coordinator.client.set_workspace(call.data["workspace"])

    async def handle_exec(call: ServiceCall):
        await coordinator.client.exec(call.data["command"])

    async def handle_notify(call: ServiceCall):
        await coordinator.client.notify(call.data["message"])

    hass.services.async_register(DOMAIN, "set_workspace", handle_set_workspace)
    hass.services.async_register(DOMAIN, "exec", handle_exec)
    hass.services.async_register(DOMAIN, "notify", handle_notify)

    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
