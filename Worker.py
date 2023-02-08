import aiohttp
import asyncio
from aiohttp import web
import re
import string
import random

routes = web.RouteTableDef()

@routes.get("/worker_ready")
async def worker_ready(request):
    return web.Response(status=200)

@routes.post("/receive_data")
async def receive_data(request):

    # Simulate a random delay in receiving the file
    await asyncio.sleep(random.uniform(0.1, 0.3))

    # Receive the 10 lines from server 2
    data = await request.json()

    # Print the lines
    print(data)

    # Count the number of words in the file
    async def count_words(text: str) -> int:
        await asyncio.sleep(0)  # Simulate an async operation
        words = re.sub("[" + string.punctuation + "]", "", str(text)).split()
        return len(words)

    word_count = await count_words(data)
    print(f"Word count: {word_count}")

    # Send the word count back to server 2
    async with aiohttp.ClientSession() as session:
        await asyncio.sleep(random.uniform(0.1, 0.3))  # Simulate a random delay in sending the results back
        await session.post("http://localhost:8081/receive_word_count", json={"word_count": word_count})

    return web.Response(status=200)

app = web.Application()
app.add_routes(routes)
web.run_app(app, port=8083)  
