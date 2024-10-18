from homeassistant.const import Platform

DOMAIN = "flashbird"
PLATFORMS: list[Platform] = [Platform.SENSOR]
SERVICE_RAZ_COMPTEUR = "raz_compteur"
CONF_NAME = "name"
CONF_DEVICE_ID = "device_id"
DEVICE_MANUFACTURER = 'smt'

API_URL = "https://pegase.api-smt.ovh/graphql"