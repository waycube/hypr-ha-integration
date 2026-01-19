from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant

from .api import HyprApiClient

_LOGGER = logging.getLogger(__name__)

class HyprlandCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass: HomeAssistant,
        client: HyprApiClient,
        name: str,
    ):
        super().__init__(
            hass=hass,
            logger=_LOGGER,  # ✅ VERPLICHT
            name=name,
            update_interval=timedelta(seconds=30),
        )
        self.client = client

    async def _async_update_data(self):
        return await self.client.status()
