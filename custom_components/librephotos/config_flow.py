import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_URL, CONF_USERNAME
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN

class LibrePhotosConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            url = user_input[CONF_URL].rstrip("/")
            session = async_get_clientsession(self.hass)
            try:
                async with session.post(
                    f"{url}/api/auth/token/obtain/",
                    json={"username": user_input[CONF_USERNAME], "password": user_input[CONF_PASSWORD]},
                    timeout=20,
                ) as response:
                    if response.status != 200:
                        errors["base"] = "invalid_auth"
                    else:
                        data = await response.json()
                        if not data.get("access") or not data.get("refresh"):
                            errors["base"] = "invalid_auth"
                        else:
                            await self.async_set_unique_id(url.lower())
                            self._abort_if_unique_id_configured()
                            return self.async_create_entry(
                                title="LibrePhotos",
                                data={**user_input, CONF_URL: url},
                            )
            except Exception:
                errors["base"] = "cannot_connect"

        schema = vol.Schema({
            vol.Required(CONF_URL, default="https://photos.evoxy.de"): str,
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str,
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
