from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, DEFAULT_PORT

DOMAIN = "hyprland_control"

class HyprlandControlConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input:
            return self.async_create_entry(
                title=user_input["name"],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("host"): str,
                vol.Optional("port", default=DEFAULT_PORT): int,
            }),
        )
