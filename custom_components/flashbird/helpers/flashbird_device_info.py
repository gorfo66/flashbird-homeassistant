from datetime import UTC, datetime


class FlashbirdDeviceInfo:
    """Class wraps the JSON structure returned by the API."""

    def __init__(self, data: dict) -> None:
        """Creates the class."""
        self.data = data or {}
        self.timestamp = datetime.now(UTC)

    def get_id(self) -> str:
        """Return device.id."""
        return self.data.get("id")

    def get_soft_version(self) -> str:
        """Return device.softVersion."""
        return self.data.get("softVersion")

    def get_latitude(self) -> float:
        """Return device.latitude."""
        return self.data.get("latitude")

    def get_longitude(self) -> float:
        """Return device.longitude."""
        return self.data.get("longitude")

    def is_lock_enabled(self) -> bool:
        """Return device.lockEnabled."""
        return self.data.get("lockEnabled")

    def get_device_type(self) -> str:
        """Return device.deviceType."""
        return self.data.get("deviceType")

    def get_serial_number(self) -> str:
        """Return device.serialNumber."""
        return self.data.get("serialNumber")

    def get_battery_percentage(self) -> int:
        """Return device.batteryPercentage."""
        return self.data.get("batteryPercentage")

    def is_connected_to_gsm(self) -> bool:
        """Return device.status.isConnectedToGSM."""
        return self.data.get("status", {}).get("isConnectedToGSM")

    def get_motorcycle_brand(self) -> str:
        """Return device.motorcycle.brand.label."""
        return self.data.get("motorcycle", {}).get("brand", {}).get("label")

    def get_motorcycle_model(self) -> str:
        """Return device.motorcycle.model.label."""
        return self.data.get("motorcycle", {}).get("model", {}).get("label")

    def get_motorcycle_battery_voltage(self) -> int:
        """Return device.motorcycle.batteryVoltageInMillivolt."""
        return self.data.get("motorcycle", {}).get("batteryVoltageInMillivolt")

    def get_total_distance(self) -> int:
        """Return device.statistics.totalDistance."""
        return self.data.get("statistics", {}).get("totalDistance")

    def get_total_time(self) -> int:
        """Return device.statistics.totalTime."""
        return self.data.get("statistics", {}).get("totalTime")

    def get_smart_keys(self):
        """Return device.smartKeys."""
        return self.data.get("smartKeys", {})

    def get_first_smartkey_serial(self) -> str:
        """Return device.smartKeys.serialNumber."""
        smart_keys = self.get_smart_keys()
        if smart_keys and isinstance(smart_keys, list):
            return smart_keys[0].get("serialNumber")
        return None

    def get_first_smartkey_battery(self) -> int:
        """Return device.smartKeys.batteryPercentage."""
        smart_keys = self.get_smart_keys()
        if smart_keys and isinstance(smart_keys, list):
            return smart_keys[0].get("batteryPercentage")
        return None

    def get_last_refresh(self) -> datetime:
        """Return last refresh timestamp (instantiated when creating this object)."""
        return self.timestamp
