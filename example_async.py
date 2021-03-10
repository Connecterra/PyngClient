from pyngclient import GenericPingClient
import asyncio
import logging

client = GenericPingClient()
logging.basicConfig(level=logging.INFO)


async def main(loop):
    loop.create_task(client.run_async("testMonitor", "PT5M", "PT1H"))

    while True:
        logging.info("Running...")
        await asyncio.sleep(10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))