import asyncio
import logging
import time

from amqtt.broker import Broker

from mqtt_config import BROKER_CONFIG, generate_password_file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    generate_password_file()
    
    # 清理插件配置
    for plugin_key in list(BROKER_CONFIG["plugins"].keys()):
        if plugin_key.startswith("server_plugin.") or plugin_key.startswith("__main__."):
            del BROKER_CONFIG["plugins"][plugin_key]
    
    broker = Broker(BROKER_CONFIG)
    connected_clients = set()
    pending_tasks = {}
    
    logger.info("MQTT Server starting...")
    await broker.start()
    logger.info("MQTT Server started, listening on 0.0.0.0:9883")
    
    # 延迟发送欢迎消息的任务
    async def send_welcome_task(client_id):
        try:
            # 等待 2 秒，确保客户端有时间订阅
            await asyncio.sleep(2.0)
            welcome_topic = f"/sys/{client_id}/user/data"
            welcome_msg = (f"Welcome to MQTT Server!\n"
                          f"Client ID: {client_id}\n"
                          f"Subscribe topic: /sys/{client_id}/user/data\n"
                          f"Publish topic: /sys/{client_id}/user/status\n"
                          f"Device-to-device: Send to /sys/targetID/user/data\n"
                          f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                          f"b'\x1d\x56\x42\x00'")
            
            # 发送两次，提高成功率
            for _ in range(1):
                await broker.internal_message_broadcast(
                    welcome_topic,
                    welcome_msg.encode("utf-8"),
                    qos=1
                )
                await asyncio.sleep(0.2)
            
            logger.info(f"✓ Welcome message sent to {client_id} on {welcome_topic}")
        except Exception as e:
            logger.debug(f"Failed to send: {e}")
        finally:
            if client_id in pending_tasks:
                del pending_tasks[client_id]
    
    # 监控任务
    async def monitor():
        while True:
            await asyncio.sleep(0.2)
            
            current_sessions = getattr(broker, '_sessions', {})
            
            # 检查新连接
            for client_id in current_sessions:
                if client_id not in connected_clients and client_id not in pending_tasks:
                    connected_clients.add(client_id)
                    pending_tasks[client_id] = True
                    logger.info(f"New client connected: {client_id}")
                    # 启动延迟发送
                    # asyncio.create_task(send_welcome_task(client_id))
            
            # 清理断开连接
            to_remove = []
            for client_id in connected_clients:
                if client_id not in current_sessions:
                    to_remove.append(client_id)
            for client_id in to_remove:
                connected_clients.remove(client_id)
                logger.info(f"Client disconnected: {client_id}")
    
    monitor_task = asyncio.create_task(monitor())
    
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("Shutdown signal received")
    finally:
        monitor_task.cancel()
        # Cancel all pending tasks
        for task in pending_tasks.values():
            if isinstance(task, asyncio.Task):
                task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass
        await broker.shutdown()
        logger.info("MQTT Server shutdown")


if __name__ == "__main__":
    asyncio.run(main())
