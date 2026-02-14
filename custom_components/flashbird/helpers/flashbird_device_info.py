"""Class wraps the JSON structure returned by the API."""

from datetime import UTC, datetime


class FlashbirdDeviceInfo:
    """Class wraps the JSON structure returned by the API."""

    def __init__(self, data: dict, refresh_rate: float | None = None) -> None:
        """Create the class."""
        self._data = data or {}
        self.timestamp = datetime.now(UTC)
        self._refresh_rate = refresh_rate
        self._mileage_increment: int = 0

    def set_refresh_rate(self, rate: float) -> None:
        """Set the refresh rate in Hz (updates per second)."""
        self._refresh_rate = rate

    def set_mileage_increment(self, increment: int) -> None:
        """Set the increment."""
        self._mileage_increment = increment

    def get_id(self) -> str:
        """Return device.id."""
        return self._data.get("id")

    def get_soft_version(self) -> str:
        """Return device.softVersion."""
        return self._data.get("softVersion")

    def get_latitude(self) -> float:
        """Return device.latitude."""
        return self._data.get("latitude")

    def get_longitude(self) -> float:
        """Return device.longitude."""
        return self._data.get("longitude")

    def is_lock_enabled(self) -> bool:
        """Return device.lockEnabled."""
        return self._data.get("lockEnabled")

    def get_device_type(self) -> str:
        """Return device.deviceType."""
        return self._data.get("deviceType")

    def get_serial_number(self) -> str:
        """Return device.serialNumber."""
        return self._data.get("serialNumber")

    def get_battery_percentage(self) -> int:
        """Return device.batteryPercentage."""
        return self._data.get("batteryPercentage")

    def is_connected_to_gsm(self) -> bool:
        """Return device.status.isConnectedToGSM."""
        return self._data.get("status", {}).get("isConnectedToGSM")

    def get_motorcycle_brand(self) -> str:
        """Return device.motorcycle.brand.label."""
        return self._data.get("motorcycle", {}).get("brand", {}).get("label")

    def get_motorcycle_model(self) -> str:
        """Return device.motorcycle.model.label."""
        return self._data.get("motorcycle", {}).get("model", {}).get("label")

    def get_motorcycle_battery_voltage(self) -> int:
        """Return device.motorcycle.batteryVoltageInMillivolt."""
        return self._data.get("motorcycle", {}).get("batteryVoltageInMillivolt")

    def get_total_distance(self) -> int:
        """Return device.statistics.totalDistance in meter."""
        return self._data.get("statistics", {}).get("totalDistance")

    def get_total_time(self) -> int:
        """Return device.statistics.totalTime."""
        return self._data.get("statistics", {}).get("totalTime")

    def get_smart_keys(self) -> list | None:
        """Return device.smartKeys."""
        return self._data.get("smartKeys", {})

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

    def get_mileage_increment(self) -> int:
        """Return the computed mileage increment in meter since last update."""
        return self._mileage_increment or 0

    def get_refresh_rate(self) -> float | None:
        """Return the refresh rate in Hz (updates per second)."""
        return self._refresh_rate

    def get_current_alert_timestamp(self) -> datetime | None:
        """Return the timestamp as datetime of the last alert or None if no alert is on going."""
        timestamp = self._data.get("lockEventTimestamp")
        return (
            datetime.fromtimestamp(timestamp / 1000, UTC)
            if timestamp is not None
            else None
        )

    def get_current_alert_level(self) -> int | None:
        """Return the level of the current alert (1 = shake detected, 2 = repeated shake detected, 3 = movement detected)."""
        timestamp = self._data.get("lockEventTimestamp")
        if timestamp is not None:
            edges = self._data.get("lockEventConnection", {}).get("edges")
            if edges is not None and isinstance(edges, list):
                alert = next(
                    (x for x in edges if x.get("node").get("timestamp") == timestamp),
                    None,
                )
                if alert is not None:
                    return alert.get("node").get("level")
        return None
