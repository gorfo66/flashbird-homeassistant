"""Helper file that contains all the needful code to register the websocket stream."""

import asyncio
import logging
import ssl
from collections.abc import Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED, EVENT_HOMEASSISTANT_STOP
from homeassistant.core import HomeAssistant

from custom_components.flashbird.const import CONF_TOKEN, CONF_TRACKER_ID
from custom_components.flashbird.helpers.flashbird_device_info import (
    FlashbirdDeviceInfo,
)
from custom_components.flashbird.helpers.graphql_ws_client import (
    GraphQLTransportWSClient,
)

_LOGGER = logging.getLogger(__name__)
API_URL = "wss://pegase.api-smt.ovh/graphql"
THROTTLE_INTERVAL = 5  # seconds
FREQUENCY_PERIOD = 600.0  # seconds


def flashbird_ws_register(
    hass: HomeAssistant, config_entry: ConfigEntry, callback: Callable
) -> None:
    """
    Register the websocket and stream the data.

    The websocket client is initiated in its own async task, registered only when
    Homeassistant finished loading, thanks to implementation of events. Similarly
    the client is closed when Home assistant closed

    Each time a message comes from the websocket subscription, we filter-it out and
    send it back to the callback method. Updates are throttled to a maximum of once
    per 5 seconds to prevent excessive updates.
    """
    _LOGGER.debug("Registering Flashbird websocket")

    client_holder = {"client": None}
    task_holder = {"task": None}
    device_id = config_entry.data[CONF_TRACKER_ID]
    last_update_time = 0.0
    pending_device_info = None

    # Refresh rate tracking (Hz - updates per second)
    update_times = []  # List of timestamps of actual updates received

    async def run_ws() -> None:
        nonlocal last_update_time, pending_device_info, update_times

        ssl_context = await hass.async_add_executor_job(ssl.create_default_context)
        current_token = config_entry.data[CONF_TOKEN]
        client = GraphQLTransportWSClient(API_URL, current_token, ssl_context)
        client_holder["client"] = client

        await client.connect()

        subscribe_query = """
        subscription Device {
            deviceUpdated {
                device {
                    id softVersion latitude longitude lockEnabled
                    deviceType serialNumber batteryPercentage
                    status { isConnectedToGSM lastPollingTimestamp }
                    motorcycle {
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
            async for event in client.subscribe(subscribe_query):
                _LOGGER.debug("WS event received: %s", event)
                device_info = FlashbirdDeviceInfo(
                    event["data"]["deviceUpdated"]["device"]
                )

                if device_info.get_id() == device_id:
                    current_loop_time = asyncio.get_event_loop().time()

                    # Track update timestamp for refresh rate calculation
                    update_times.append(current_loop_time)
                    # Keep only updates from the last 10 minutes (600 seconds) for Hz
                    update_times[:] = [
                        t
                        for t in update_times
                        if current_loop_time - t < FREQUENCY_PERIOD
                    ]
                    # Calculate refresh rate in Hz (updates per second)
                    # With ~1 update per 5 min: 1-2 updates / 600 sec = 0.00167-0.00333 Hz
                    refresh_rate = (
                        len(update_times) / FREQUENCY_PERIOD if update_times else 0.0
                    )
                    device_info.set_refresh_rate(refresh_rate)

                    # If throttle window has passed, send immediately
                    if current_loop_time - last_update_time >= THROTTLE_INTERVAL:
                        await callback(device_info)
                        last_update_time = current_loop_time
                        pending_device_info = None
                    else:
                        # Store latest device info to send on next throttle window
                        pending_device_info = device_info
        except asyncio.CancelledError:
            await client.close()
            raise

    async def start_ws(_: object) -> None:
        _LOGGER.debug("start websocket task")

        # Create a background task for the websocket
        task = hass.async_create_task(run_ws())
        task_holder["task"] = task

    async def stop_ws(_: object) -> None:
        _LOGGER.debug("stop websocket task")
        task = task_holder.get("task")
        if task:
            _LOGGER.debug("Cancelling WebSocket task")
            task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            _LOGGER.debug("WebSocket task cancelled")

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, start_ws)
    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, stop_ws)
