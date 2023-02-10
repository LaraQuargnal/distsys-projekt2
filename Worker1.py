import asyncio
import aiohttp
from aiohttp import web
import re
import string
import random
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MASTER = "http://localhost:8081/receive_worker_word_count"

routes = web.RouteTableDef()


@routes.get("/worker_ready")
async def worker_ready(request):
    return web.Response(status=200)


@routes.post("/receive_data")
async def receive_data(request):

    # Simulate a random delay in receiving the file
    await asyncio.sleep(random.uniform(0.1, 0.3))

    # Receive the lines from Master
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Failed to receive data: {e}")
        return web.Response(status=400, text="Error")

    # print(data)

    # Count the number of words in the file
    async def count_words(text: str) -> int:
        await asyncio.sleep(0)  # Simulate an async operation
        words = re.sub("[" + string.punctuation + "]", "", str(text)).split()
        return len(words)

    word_count = await count_words(data)
    logging.info(f"Word count: {word_count}")

    # Send the word_count back to Master
    async with aiohttp.ClientSession() as session:
        await asyncio.sleep(random.uniform(0.1, 0.3))  # Simulate a random delay in sending the results back
        try:
            await session.post(MASTER,
                               json={"worker_port": "worker" + str(request.transport.get_extra_info("sockname")[1]),
                                     "word_count": word_count})
        except aiohttp.ClientError as e:
            logger.error(f"Failed to send word count: {e}")
            return web.Response(status=500, text="Failed to send word count")

    return web.Response(status=200)

app = web.Application(client_max_size=1024 * 1024 * 200)
app.add_routes(routes)
web.run_app(app, port=8083)  # For worker 1
# web.run_app(app, port=8084)  # For worker 2
# web.run_app(app, port=8085)  # For worker 3
# web.run_app(app, port=8086)  # For worker 4
# web.run_app(app, port=8087)  # For worker 5
