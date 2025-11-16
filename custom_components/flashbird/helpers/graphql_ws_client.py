import logging
import asyncio
import json
import uuid
import websockets
from websockets.exceptions import ConnectionClosed

_LOGGER = logging.getLogger(__name__)

class GraphQLTransportWSClient:
    def __init__(self, url: str, token: str, ssl_context, reconnect_delay=5, ping_interval=300):
        self.url = url
        self.token = token
        self.ssl_context = ssl_context
        self.reconnect_delay = reconnect_delay
        self.ping_interval = ping_interval

        self.ws = None
        self.connected = False
        self.listener_task = None
        self.ping_task = None

        self._closed = False

        # op_id → asyncio.Queue
        self.pending = {}
        # op_id → {query, variables, queue}
        self.subscriptions = {}

    async def connect(self):
        """Connect with automatic reconnect."""
        _LOGGER.debug('connect')
        while not self._closed:
            try:
                self.ws = await websockets.connect(
                    self.url,
                    ssl=self.ssl_context,
                    subprotocols=["graphql-transport-ws"]
                )

                payload = {"Authorization": f"Bearer {self.token}"} if self.token else {}

                await self.ws.send(json.dumps({
                    "type": "connection_init",
                    "payload": payload
                }))

                raw = await self.ws.recv()
                msg = json.loads(raw)
                if msg.get("type") != "connection_ack":
                    raise RuntimeError(f"Unexpected handshake message: {msg}")

                self.connected = True

                # Start listener and ping tasks
                self.listener_task = asyncio.create_task(self._listener())
                self.ping_task = asyncio.create_task(self._ping_loop())

                # Re-subscribe active subscriptions
                await self._restore_subscriptions()

                return  # Successfully connected

            except Exception as e:
                _LOGGER.debug(f"[WS] Cannot connect: {e}. Retrying in {self.reconnect_delay}s")
                await asyncio.sleep(self.reconnect_delay)

    async def _ping_loop(self):
        """Send periodic pings and trigger reconnection on failure."""
        try:
            while True:
                await asyncio.sleep(self.ping_interval)
                if self.ws is None or not self.connected:
                    continue
                try:
                    _LOGGER.debug('ping')
                    await self.ws.ping()
                except Exception as e:
                    _LOGGER.debug(f"[WS] Ping failed, triggering reconnection: {e}")
                    return  # exit ping loop
        except asyncio.CancelledError:
            pass

    async def _trigger_reconnect(self):
        """Close current connection and trigger reconnect."""
        _LOGGER.debug('trigger reconnect')
        try:
            if self.ws:
                await self.ws.close()
        finally:
            self.connected = False
            if not self._closed:
                # reconnect automatically
                _LOGGER.debug('reconnect')
                await self.connect()

    async def _listener(self):
        """Receive messages and dispatch to queues."""
        _LOGGER.debug('listener')
        try:
            while True:
                raw = await self.ws.recv()
                msg = json.loads(raw)

                op_id = msg.get("id")
                msg_type = msg.get("type")

                if msg_type == "next":
                    queue = self.pending.get(op_id)
                    if queue:
                        await queue.put(msg["payload"])
                elif msg_type == "complete":
                    queue = self.pending.get(op_id)
                    if queue:
                        await queue.put(None)

        except ConnectionClosed:
            pass
        finally:
            self.connected = False
            if self.ping_task:
                self.ping_task.cancel()
                self.ping_task = None
            if not self._closed:
                _LOGGER.debug('reconnect')
                await self.connect()


    async def _restore_subscriptions(self):
        """Re-send all active subscriptions after reconnect."""
        if not self.ws:
            return

        for op_id, sub in self.subscriptions.items():
            await self.ws.send(json.dumps({
                "id": op_id,
                "type": "subscribe",
                "payload": {
                    "query": sub["query"],
                    "variables": sub["variables"] or {}
                }
            }))

            
    async def subscribe(self, query: str, variables=None):
        """Async generator for subscriptions with auto re-subscribe."""
        _LOGGER.debug('subscribe')
        if not self.connected:
            await self.connect()

        op_id = str(uuid.uuid4())
        queue = asyncio.Queue()

        self.pending[op_id] = queue
        self.subscriptions[op_id] = {
            "query": query,
            "variables": variables,
            "queue": queue
        }

        await self.ws.send(json.dumps({
            "id": op_id,
            "type": "subscribe",
            "payload": {"query": query, "variables": variables or {}}
        }))

        try:
            while True:
                msg = await queue.get()
                if msg is None:
                    break
                yield msg

        finally:
            # Cleanup after generator exits
            self.pending.pop(op_id, None)
            self.subscriptions.pop(op_id, None)

            if self.connected:
                await self.ws.send(json.dumps({
                    "id": op_id,
                    "type": "complete"
                }))

    async def close(self):
        """Stop reconnect loop and close the WebSocket."""
        _LOGGER.debug('close')
        self._closed = True
        if self.ws:
            try:
                await self.ws.close()
            except:
                pass
        self.connected = False


 