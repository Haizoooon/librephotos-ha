from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import EntityCategory
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        LibrePhotosCount(data["coordinator"]),
        LibrePhotosDate(data["client"], data["coordinator"]),
    ])

class LibrePhotosCount(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Fotoanzahl"
    _attr_unique_id = "librephotos_photo_count"
    _attr_native_unit_of_measurement = "Fotos"

    @property
    def native_value(self):
        return self.coordinator.data.get("count", 0)

class LibrePhotosDate(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_name = "Aufnahmedatum"
    _attr_unique_id = "librephotos_photo_date"

    def __init__(self, client, coordinator):
        super().__init__(coordinator)
        self.client = client

    @property
    def native_value(self):
        p = self.client.current_photo or {}
        return p.get("撮影日") or p.get("date") or p.get("exif_timestamp") or p.get("timestamp") or "Unbekannt"
