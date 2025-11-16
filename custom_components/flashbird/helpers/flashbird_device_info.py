from datetime import datetime, timezone

class FlashbirdDeviceInfo:
    """Class that wraps the JSON structure returned by the API and provide safe accessors"""

    def __init__(self, data: dict) -> None:
        self.data = data or {}
        self.timestamp = datetime.now(timezone.utc)

    def get_id(self) -> str:
        return self.data.get("id")

    def get_soft_version(self) -> str:
        return self.data.get("softVersion")

    def is_activated(self) -> bool:
        return self.data.get("activated")

    def get_latitude(self) -> float:
        return self.data.get("latitude")

    def get_longitude(self) -> float:
        return self.data.get("longitude")

    def is_lock_enabled(self) -> bool:
        return self.data.get("lockEnabled")

    def get_device_type(self) -> str:
        return self.data.get("deviceType")

    def get_serial_number(self) -> str:
        return self.data.get("serialNumber")

    def get_battery_percentage(self) -> int:
        return self.data.get("batteryPercentage")

    def is_connected_to_gsm(self) -> bool:
        return self.data.get("status", {}).get("isConnectedToGSM")

    def get_motorcycle_id(self) -> str:
        return self.data.get("motorcycle", {}).get("id")

    def get_motorcycle_brand(self) -> str:
        return self.data.get("motorcycle", {}).get("brand", {}).get("label")

    def get_motorcycle_model(self) -> str:
        return self.data.get("motorcycle", {}).get("model", {}).get("label")

    def get_motorcycle_battery_voltage(self) -> int:
        return self.data.get("motorcycle", {}).get("batteryVoltageInMillivolt")

    def get_total_distance(self) -> int:
        return self.data.get("statistics", {}).get("totalDistance")

    def get_total_time(self) -> int:
        return self.data.get("statistics", {}).get("totalTime")

    def get_smart_keys(self):
        return self.data.get("smartKeys", {})

    def get_first_smartkey_serial(self) -> str:
        smart_keys = self.get_smart_keys()
        if smart_keys and isinstance(smart_keys, list):
            return smart_keys[0].get("serialNumber")
        return None

    def get_first_smartkey_battery(self) -> int:
        smart_keys = self.get_smart_keys()
        if smart_keys and isinstance(smart_keys, list):
            return smart_keys[0].get("batteryPercentage")
        return None

    def get_last_refresh(self) -> datetime:
        return self.timestamp