from datetime import datetime, timezone

from homeassistant.components.image import ImageEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [LibrePhotosImage(hass, data["client"], data["coordinator"])]
    )


class LibrePhotosImage(CoordinatorEntity, ImageEntity):
    """Expose the currently selected LibrePhotos photo as an HA image entity."""

    _attr_has_entity_name = True
    _attr_name = "Tagesfoto"
    _attr_unique_id = "librephotos_daily_photo"
    _attr_content_type = "image/jpeg"

    def __init__(self, hass: HomeAssistant, client, coordinator) -> None:
        CoordinatorEntity.__init__(self, coordinator)
        ImageEntity.__init__(self, hass)
        self.client = client
        self._attr_image_last_updated = (
            datetime.now(timezone.utc) if client.photo_bytes else None
        )

    @property
    def image_last_updated(self):
        """Return the last time the selected image changed."""
        return self._attr_image_last_updated

    @callback
    def _handle_coordinator_update(self) -> None:
        """Notify Home Assistant that the image has changed."""
        if self.client.photo_bytes:
            self._attr_image_last_updated = datetime.now(timezone.utc)
        super()._handle_coordinator_update()

    async def async_image(self) -> bytes | None:
        """Return the cached image bytes."""
        return self.client.photo_bytes

    @property
    def extra_state_attributes(self):
        photo = self.client.current_photo or {}
        return {
            "photo_hash": photo.get("image_hash", photo.get("hash")),
            "photo_data": photo,
        }
