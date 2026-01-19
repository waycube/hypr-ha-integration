import aiohttp
import async_timeout

class HyprApiClient:
    def __init__(self, host: str, port: int, session: aiohttp.ClientSession):
        self._base = f"http://{host}:{port}"
        self._session = session

    async def status(self) -> dict:
        async with async_timeout.timeout(5):
            async with self._session.get(f"{self._base}/status") as resp:
                resp.raise_for_status()
                return await resp.json()

    async def set_workspace(self, workspace: int):
        async with self._session.post(f"{self._base}/workspace/{workspace}"):
            pass

    async def exec(self, command: str):
        async with self._session.post(
            f"{self._base}/exec", params={"command": command}
        ):
            pass

    async def notify(self, message: str):
        async with self._session.post(
            f"{self._base}/notify", params={"message": message}
        ):
            pass
