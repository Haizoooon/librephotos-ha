from homeassistant.const import CONF_PASSWORD, CONF_URL, CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.exceptions import ConfigEntryNotReady
from datetime import timedelta
import logging
from .const import DOMAIN, PLATFORMS, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class LibrePhotosClient:
    def __init__(self, hass, entry):
        self.hass = hass
        self.session = async_get_clientsession(hass)
        self.url = entry.data[CONF_URL].rstrip("/")
        self.username = entry.data[CONF_USERNAME]
        self.password = entry.data[CONF_PASSWORD]
        self.access = None
        self.refresh = None
        self.current_photo = None
        self.photo_bytes = None
        self.photo_count = 0

    async def _json(self, method, path, **kwargs):
        headers = kwargs.pop("headers", {})
        if self.access:
            headers["Authorization"] = f"Bearer {self.access}"
        async with self.session.request(method, self.url + path, headers=headers, timeout=30, **kwargs) as r:
            if r.status == 401 and self.refresh:
                await self._refresh_token()
                headers["Authorization"] = f"Bearer {self.access}"
                async with self.session.request(method, self.url + path, headers=headers, timeout=30, **kwargs) as retry:
                    retry.raise_for_status()
                    return await retry.json()
            r.raise_for_status()
            return await r.json()

    async def _login(self):
        data = await self._json("POST", "/api/auth/token/obtain/",
            json={"username": self.username, "password": self.password}, headers={})
        self.access, self.refresh = data["access"], data["refresh"]

    async def _refresh_token(self):
        async with self.session.post(self.url + "/api/auth/token/refresh/",
            json={"refresh": self.refresh}, timeout=20) as r:
            if r.status != 200:
                self.access = None
                await self._login()
                return
            data = await r.json()
            self.access = data["access"]

    async def _get_json(self, path):
        if not self.access:
            await self._login()
        return await self._json("GET", path)

    async def choose_random_photo(self):
        import random
        days_data = await self._get_json("/api/albums/date/list/")
        days = days_data if isinstance(days_data, list) else days_data.get("results", [])
        if not days:
            self.current_photo = None
            self.photo_bytes = None
            self.photo_count = 0
            return
        self.photo_count = sum(int(d.get("numberOfItems", d.get("count", 0)) or 0) for d in days)
        # Weight days by their photo count so each photo has approximately equal odds.
        weighted = []
        for day in days:
            count = int(day.get("numberOfItems", day.get("count", 0)) or 0)
            if count > 0:
                weighted.extend([day] * min(count, 100))
        day = random.choice(weighted or days)
        day_id = day.get("id", day.get("date"))
        if day_id is None:
            raise ValueError("LibrePhotos date-list response has no day id")
        album = await self._get_json(f"/api/albums/date/{day_id}?page_size=1000")
        items = album.get("items", album.get("results", [])) if isinstance(album, dict) else []
        if isinstance(items, dict):
            items = items.get("items", [])
        if not items:
            raise ValueError("LibrePhotos returned no photos for the selected day")
        photo = random.choice(items)
        self.current_photo = photo
        image_hash = next((photo.get(k) for k in ("image_hash", "hash", "photo_hash") if photo.get(k)), None)
        if not image_hash:
            raise ValueError("Could not identify image hash in LibrePhotos photo response")
        headers = {"Authorization": f"Bearer {self.access}"}
        async with self.session.get(self.url + f"/media/thumbnails_big/{image_hash}", headers=headers, timeout=60) as r:
            if r.status == 401:
                await self._refresh_token()
                headers["Authorization"] = f"Bearer {self.access}"
                async with self.session.get(self.url + f"/media/thumbnails_big/{image_hash}", headers=headers, timeout=60) as retry:
                    retry.raise_for_status()
                    self.photo_bytes = await retry.read()
            else:
                r.raise_for_status()
                self.photo_bytes = await r.read()

    async def async_image(self):
        return self.photo_bytes

async def async_setup_entry(hass, entry):
    client = LibrePhotosClient(hass, entry)
    async def update():
        try:
            await client.choose_random_photo()
            return {"photo": client.current_photo, "count": client.photo_count}
        except Exception as err:
            _LOGGER.exception("LibrePhotos update failed")
            raise err
    coordinator = DataUpdateCoordinator(
        hass, _LOGGER, name="LibrePhotos",
        update_method=update, update_interval=None
    )
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        raise ConfigEntryNotReady from err
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {"client": client, "coordinator": coordinator}
    async def next_photo(call):
        await client.choose_random_photo()
        coordinator.async_set_updated_data({"photo": client.current_photo, "count": client.photo_count})
    hass.services.async_register(DOMAIN, "next_random_photo", next_photo)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
