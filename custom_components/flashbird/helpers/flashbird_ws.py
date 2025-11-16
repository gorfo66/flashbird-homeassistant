import logging
import ssl
import asyncio

from homeassistant.core import HomeAssistant
from homeassistant.const import EVENT_HOMEASSISTANT_STOP, EVENT_HOMEASSISTANT_STARTED
from .graphql_ws_client import GraphQLTransportWSClient
from .flashbird_device_info import FlashbirdDeviceInfo

_LOGGER = logging.getLogger(__name__)
API_URL = "wss://pegase.api-smt.ovh/graphql"

def flashbird_ws_register(hass: HomeAssistant, token: str, device_id: str, callback):
    _LOGGER.debug("Registering Flashbird websocket")

    client_holder = {"client": None}
    task_holder = {"task": None}

    async def run_ws():
        ssl_context = await hass.async_add_executor_job(ssl.create_default_context)
        client = GraphQLTransportWSClient(API_URL, token, ssl_context)
        client_holder["client"] = client

        await client.connect()

        SUB_QUERY = """
        subscription Device {
            deviceUpdated {
                device {
                    id softVersion activated latitude longitude lockEnabled
                    deviceType serialNumber batteryPercentage
                    status { isConnectedToGSM lastPollingTimestamp }
                    motorcycle {
                        id
                        brand { label }
                        model { label }
                        batteryVoltageInMillivolt
                    }
                    statistics { totalDistance totalTime }
                    smartKeys { serialNumber batteryPercentage }
                }
            }
        }
        """

        try:
            async for event in client.subscribe(SUB_QUERY):
                _LOGGER.debug("WS event received: %s", event)
                device_info = FlashbirdDeviceInfo(event["data"]["deviceUpdated"]["device"])

                if device_info.get_id() == device_id:
                    await callback(device_info)
        except asyncio.CancelledError:
            await client.close()
            raise

    
    async def start_ws(event):
        # Create a background task for the websocket
        task = hass.async_create_task(run_ws())
        task_holder["task"] = task

    
    async def stop_ws(event):
        task = task_holder.get("task")
        if task:
            _LOGGER.debug("Cancelling WebSocket task")
            task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            _LOGGER.debug("WebSocket task cancelled")
            pass
   

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, start_ws)
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, stop_ws)

    return True

    