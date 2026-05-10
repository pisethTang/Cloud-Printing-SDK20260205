import asyncio
import logging
import time

from amqtt.broker import Broker

from mqtt_config_noauth import BROKER_CONFIG

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    # Clean plugin config
    for plugin_key in list(BROKER_CONFIG["plugins"].keys()):
        if plugin_key.startswith("server_plugin.") or plugin_key.startswith("__main__."):
            del BROKER_CONFIG["plugins"][plugin_key]
    
    broker = Broker(BROKER_CONFIG)
    connected_clients = set()
    
    logger.info("MQTT Server (no auth) starting...")
    await broker.start()
    logger.info("MQTT Server started, listening on 0.0.0.0:9883 (NO AUTHENTICATION)")
    
    async def monitor():
        while True:
            await asyncio.sleep(2)
            current_sessions = getattr(broker, '_sessions', {})
            for client_id in current_sessions:
                if client_id not in connected_clients:
                    connected_clients.add(client_id)
                    logger.info(f">>> PRINTER CONNECTED: {client_id}")
            to_remove = []
            for client_id in connected_clients:
                if client_id not in current_sessions:
                    to_remove.append(client_id)
            for client_id in to_remove:
                connected_clients.remove(client_id)
                logger.info(f"<<< PRINTER DISCONNECTED: {client_id}")
    
    monitor_task = asyncio.create_task(monitor())
    
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("Shutdown signal received")
    finally:
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass
        await broker.shutdown()
        logger.info("MQTT Server shutdown")


if __name__ == "__main__":
    asyncio.run(main())
